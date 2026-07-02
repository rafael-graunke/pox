from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr
import struct
import socket

log = core.getLogger()

IGMP_PROTOCOL        = 2
MEMBERSHIP_REPORT_V2 = 0x16
LEAVE_GROUP_V2       = 0x17


def parse_igmp (raw):
  """
  Manually deserialize an IGMPv2 header from raw bytes.

  Wire format (8 bytes):
    offset 0: type          (1 byte, unsigned)
    offset 1: max_resp_time (1 byte, unsigned)
    offset 2: checksum      (2 bytes, big-endian unsigned)
    offset 4: group_address (4 bytes, IPv4)

  Returns a dict or None if the data is too short.
  """
  if len(raw) < 8:
    return None
  type_, max_resp, checksum, group_bytes = struct.unpack("!BBH4s", raw[:8])
  return {
    'type':     type_,
    'max_resp': max_resp,
    'checksum': checksum,
    'group':    socket.inet_ntoa(group_bytes),
  }


class IGMPSnooping (object):

  def __init__ (self):
    # group_table[dpid][group_ip_str] = set of port numbers
    self.group_table = {}
    core.openflow.addListeners(self)

  def _handle_ConnectionUp (self, event):
    self.group_table[event.dpid] = {}
    log.info("Switch %s connected, group table initialized", dpid_to_str(event.dpid))

  def _handle_PacketIn (self, event):
    packet = event.parsed
    if not packet.parsed:
      return

    ipv4_pkt = packet.find('ipv4')

    if ipv4_pkt is not None and ipv4_pkt.protocol == IGMP_PROTOCOL:
      payload = ipv4_pkt.payload
      igmp_raw = payload.raw if hasattr(payload, 'raw') else None
      if igmp_raw is None:
        return
      igmp = parse_igmp(igmp_raw)
      if igmp is None:
        return
      log.debug("IGMP type=0x%02x group=%s port=%d",
                igmp['type'], igmp['group'], event.port)
      self._process_igmp(event, igmp)

    elif packet.dst.is_multicast:
      self._forward_multicast(event, ipv4_pkt)

    else:
      self._flood(event)

  def _process_igmp (self, event, igmp):
    dpid  = event.dpid
    port  = event.port
    group = igmp['group']

    if dpid not in self.group_table:
      self.group_table[dpid] = {}

    if igmp['type'] == MEMBERSHIP_REPORT_V2:
      self.group_table[dpid].setdefault(group, set()).add(port)
      log.info("Join  switch=%s group=%s port=%d", dpid_to_str(dpid), group, port)
      self._install_multicast_flow(event, group)

    elif igmp['type'] == LEAVE_GROUP_V2:
      if group in self.group_table[dpid]:
        self.group_table[dpid][group].discard(port)
        log.info("Leave switch=%s group=%s port=%d", dpid_to_str(dpid), group, port)
        if self.group_table[dpid][group]:
          self._install_multicast_flow(event, group)
        else:
          self._install_drop_flow(event, group)

  def _install_multicast_flow (self, event, group):
    ports = self.group_table.get(event.dpid, {}).get(group, set())
    if not ports:
      return
    msg = of.ofp_flow_mod()
    msg.match.dl_type  = 0x0800
    msg.match.nw_dst   = IPAddr(group)
    msg.idle_timeout   = 30
    msg.hard_timeout   = 60
    for port in ports:
      msg.actions.append(of.ofp_action_output(port=port))
    event.connection.send(msg)
    log.info("Flow installed group=%s ports=%s", group, sorted(ports))

  def _install_drop_flow (self, event, group):
    msg = of.ofp_flow_mod()
    msg.match.dl_type  = 0x0800
    msg.match.nw_dst   = IPAddr(group)
    msg.idle_timeout   = 10
    msg.hard_timeout   = 30
    event.connection.send(msg)
    log.info("Drop flow installed group=%s (no subscribers)", group)

  def _forward_multicast (self, event, ipv4_pkt):
    if ipv4_pkt is None:
      self._flood(event)
      return
    group = str(ipv4_pkt.dstip)
    ports = self.group_table.get(event.dpid, {}).get(group, set())
    if not ports:
      self._flood(event)
      return
    msg = of.ofp_flow_mod()
    msg.match.dl_type = 0x0800
    msg.match.nw_dst  = IPAddr(group)
    msg.idle_timeout  = 30
    msg.hard_timeout  = 60
    msg.data          = event.ofp
    msg.in_port       = event.port
    for port in ports:
      msg.actions.append(of.ofp_action_output(port=port))
    event.connection.send(msg)

  def _flood (self, event):
    msg = of.ofp_packet_out()
    msg.data    = event.ofp
    msg.in_port = event.port
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)


def launch ():
  core.registerNew(IGMPSnooping)

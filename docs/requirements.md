
I) Escolha do software + definição/aprovação da funcionalidade (20%)

Para obter esta pontuação, as definições devem ser apresentadas até 11/05/2026 e incluir: justificativa do software, escopo do recurso, protocolos/cabeçalhos que serão interpretados e plano de integração.

II) Publicação na comunidade de software livre (5%)

Avalia-se a publicação do código em repositório público e a conformidade mínima de disponibilização (README, instruções e licença quando necessário).

III) Documentação da funcionalidade acrescida (30%)

A documentação deverá ser entregue em PDF (e também disponível no repositório, se aplicável) e conter, obrigatoriamente:

1) Descrição da funcionalidade implementada

objetivo do recurso, motivação e benefícios para o software escolhido;
requisitos atendidos e limitações.
2) Integração com o software original

onde a funcionalidade foi adicionada (módulos/arquivos);
quais partes do software original foram modificadas e por quê.
3) Detalhamento técnico da implementação

descrição detalhada de como a funcionalidade foi desenvolvida
funções, classes e/ou módulos criados e alterados (com explicação do papel de cada um)
fluxo de execução do recurso (entrada → processamento → saída)
evidência de que houve manipulação/interpretação de cabeçalhos de protocolos (campos interpretados, regras e exemplos)
4) Diagramas obrigatórios

diagramas apropriados que representem o desenvolvimento realizado e sua ligação com o programa original (ex.: diagrama de módulos, classes, sequência e/ou fluxo).
5) Procedimentos de execução e validação

como compilar/instalar/executar
como reproduzir a demonstração
testes realizados (mínimo: casos de teste e resultados esperados)
Caso tenha sido utilizada qualquer ferramenta de IA generativa (ex.: ChatGPT, Copilot, Gemini, etc.), é obrigatório incluir na documentação uma seção específica intitulada "Uso de IA Generativa (GPT)", contendo todos os itens abaixo:

a) Ferramenta(s) utilizada(s) (nome e ambiente; se aplicável, modelo/versão).

b) Objetivo do uso (ex.: gerar esboço de código, refatorar, revisar documentação, gerar testes, explicar protocolo).

c) Registro dos prompts e respostas relevantes, incluindo:

prompts principais utilizados (os que influenciaram decisões técnicas);
resumo do conteúdo retornado;
o que foi aproveitado e o que foi descartado.
d) Rastreabilidade no código: indicar explicitamente quais arquivos/trechos do projeto foram impactados pelo uso de IA (ex.: lista de arquivos, commits ou seções).

e) Validação técnica obrigatória: descrever como o grupo verificou a correção do que foi sugerido pela IA, incluindo ao menos uma das evidências:

testes com PCAP/captura real;
conferência com RFCs/Documentação do protocolo;
comparação com ferramentas (ex.: Wireshark/tshark) para validar campos interpretados.
Se a IA foi utilizada e esta seção não estiver completa, haverá desconto direto no item Documentação (20%), podendo chegar a zero neste item em caso de ausência total de registro (por falta de rastreabilidade e verificação).

O grupo permanece integralmente responsável pelo conteúdo técnico e poderá ser arguido na apresentação sobre qualquer trecho implementado/documentado.

IV) Implementação e funcionamento (45%)

Avalia-se:

funcionamento correto do software com a funcionalidade implementada
aderência ao requisito de interpretação de cabeçalhos
estabilidade/qualidade do código (organização, consistência, testes básicos quando possível).


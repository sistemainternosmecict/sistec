# Introdução

## Propósito do documento

Este documento visa especificar o comportamento externo do Sistema Interno de Suporte Tecnológico. Nele estão contidos a descrição de requisitos funcionais e não funcionais, restrições de design e outros fatores tomados como base para a construção de um sistema de software. Este documento permite também um melhor entendimento por parte dos gestores, por usar uma linguagem menos técnica e mais natural.

## Escopo do documento

Este documento descreve os processos da empresa, casos de uso do sistema, modelos variados que representam visões diferentes do sistema e servirá como documento principal para o desenvolvimento saudável do projeto. Todos os artefatos produzidos antes e durante o desenvolvimento serão anexados a este documento, para que todas as informações necessárias, sejam encontradas em um só lugar. A partir da análise desta documentação, serão construídos modelos (na etapa de projeto) que serão convertidos em código-fonte (na etapa de construção).

## Definições, abreviações e termos do negócio

- Stakeholders - Pessoas interessadas ou envolvidas no projeto.
- Colaborador - Um usuario interno do sistema.
- Solicitante - Um usuario externo do sistema.
- Demanda - Uma necessidade, um pedido.
- Protocolo - Número único identificador da demanda.
- Estação de trabalho - Um computador de mesa usado por um usuario.
- Inventario - Setor de gerenciamento de dispositivos.
- Unidade Escolar - Uma escola da rede.

## Contexto do problema / solução

O problema de processos manuais lentos, alto acúmulo de documentação física e dados dispersos sem relação, impede os setores de analisarem esses dados críticos com precisão, e isso afeta a organização como um todo, cujo impacto é o aumento de tempo de execução de atividades, custos maiores com menor retorno e carga de trabalho desnecessária em operações manuais que fazem parte de alguns processos. 

Uma solução viável é:

* Criar um sistema de controle interno.

Acreditamos que um sistema de suporte interno é essencial. O presente sistema vem a ser um software personalizado que será responsável pela disponibilização de uma interface de usuário interativa e dinâmica para gerenciamento e registro de operações diversas realizadas pelo setor de Suporte de Tecnologia. Ao invés de precisar usar software de terceiros, nosso software permitirá uma organização planejada e adequada aos processos internos.

## Usuários

- **Colaborador** - Um funcionário ou estagiário envolvido no atendimento de suporte de TI. Este tipo de usuário, terá acesso à área interna do sistema, por meio de suas credenciais cadastradas. Somente um colaborador cadastrado, poderá registrar um colaborador novo.
- 
- **Solicitante** - Um funcionário que irá solicitar um Serviço de Suporte por meio do sistema. Somente colaboradores registrados poderão cadastrar um Solicitante.

## Benefícios

- Controle visual e lógico do fluxo de atendimento do suporte de tecnologia;
- Aumento na agilidade no atendimento de pedidos de suporte de tecnologia;
- Acesso restrito a informações críticas do setor através de relatórios precisos para tomada de decisão mais assertiva;
- Sistema em rede local e pode ser acessado por qualquer dispositivo no wifi ou rede cabeada do prédio, mesmo sem internet;
- O sistema interno não poderá ser acessado “de fora” (através da internet) sem autorização interna. Portanto, isso conta como benefício, se tivermos em vista, ataques e roubo de dados;
- Sistema personalizado, construído internamente. O que significa que pode ser modificado, melhorado e reparado mais facilmente que um sistema de terceiros;

## Restrições / limitações do projeto

* A princípio, os processos não estão devidamente mapeados e o entendimento dos processos internos (processos, pessoas e dados) é essencial para o desenvolvimento correto do sistema. Portanto um tempo inicial foi tomado para entender os fluxos de processos internos.
* O sistema inicialmente usará uma planilha google como armazenamento de dados e futuramente será totalmente migrado para um banco de dados de fato.
* Este projeto piloto rodará em fase de testes somente entre as 3 salas da TI (Sala 15b, Sala 21 e Sala 24) e futuramente será expandido aos outros setores.
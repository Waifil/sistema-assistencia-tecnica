# Sistema de Assistência Técnica

## Sobre o projeto

Este projeto consiste no desenvolvimento de um sistema web para auxiliar na organização de uma assistência técnica.

O objetivo é facilitar o cadastro de clientes, o registro de serviços e o acompanhamento dos consertos, substituindo as anotações feitas manualmente em papéis.

## Funcionalidades

- Cadastro de usuários e acesso ao sistema.
- Cadastro de clientes com nome e telefone.
- Busca de clientes pelo nome ou número de telefone.
- Exibição dos últimos 5 clientes cadastrados, mantendo todos os registros armazenados.
- Registro de serviços e descrição dos problemas.
- Acompanhamento dos serviços por status:
  - Pendente
  - Em andamento
  - Concluído
  - Entregue
- Atualização do status dos serviços.
- Consulta dos serviços cadastrados.
- Painel inicial com resumo dos serviços.
- Recurso de acessibilidade com alto contraste.

## Tecnologias utilizadas

- Python 3.12
- Flask
- HTML5
- CSS3
- JavaScript
- SQLite

## Estrutura do projeto

```text
├── README.md
│
└── Assistencia Tecnica/
    ├── start.bat
    │
    └── sistema/
        ├── app.py
        ├── database.py
        ├── requirements.txt
        │
        ├── __pycache__/
        │
        ├── templates/
        │   ├── login.html
        │   ├── index.html
        │   ├── clientes.html
        │   └── servicos.html
        │
        └── static/
            ├── style.css
            └── acessibilidade.js
```

## Objetivo

O sistema busca melhorar a organização da assistência técnica, facilitando o controle dos clientes e dos serviços realizados. Dessa forma, pretende reduzir a dependência de anotações em papel e tornar a consulta das informações mais prática.

## Status do projeto

Em desenvolvimento. Este projeto faz parte de uma atividade acadêmica de criação de um Produto Mínimo Viável (MVP).

# Sistema de Assistência Técnica

## Sobre o projeto

Este projeto consiste no desenvolvimento de um sistema web para auxiliar na organização de uma assistência técnica.

O objetivo é facilitar o cadastro de clientes, o registro de serviços e o acompanhamento dos consertos, substituindo as anotações feitas manualmente em papéis.

## Funcionalidades

- Cadastro de clientes com nome e telefone.
- Busca de clientes pelo número de telefone.
- Registro de serviços e descrição dos problemas.
- Acompanhamento dos serviços por status:
  - Pendente
  - Em andamento
  - Concluído
  - Entregue
- Consulta dos serviços cadastrados.

## Tecnologias utilizadas

- Python 3.12
- Flask
- HTML5
- CSS3
- JavaScript
- SQLite

## Estrutura do projeto

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
        ├── templates/
        │   ├── login.html
        │   ├── index.html
        │   ├── clientes.html
        │   └── servicos.html
        │
        └── static/
            ├── style.css
            └── acessibilidade.js
## Objetivo

O sistema busca melhorar a organização da assistência técnica, facilitando o controle dos clientes e dos serviços realizados.

## Status do projeto

Em desenvolvimento. Este projeto faz parte de uma atividade acadêmica de criação de um Produto Mínimo Viável (MVP).

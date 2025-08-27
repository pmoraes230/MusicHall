# SENAC MUSIC HALL
O senac music hall é um sistema de gerenciamento de eventos, vendas e cadastros de funcionários de uma casa de show de mesmo nome em brasilia DF. O sistema tem  a função de facilitar o dia a dia deixando o fluxo de trabalho mais ágil com ele tendo sua hierárquia interna, assim subdividindo.

## Função dos perfis
- Administrador (Tem a responsabilidade de gerenciar o sistema como um todo, tem acesso a todos as telas e funcionalidades, podendo tanto cadastrar um novo usuário e eventos com setores até apagar)
- Vendedor (Perfil responsável de apenas vender os ingressos aos clientes final e também podendo somente cadastrar um novo cliente no sistema)
- Validador (Perfil responsável de validar o ingressos no dia do show)

## Técnologias usadas
Abaixo a lista de tecnologias usadas neste sistema
- Python como linguagem de programação.
- Django como framework para apps web.
- MySql como banco de dados para armazenamento de informações.
- Python-dotenv para leitura de arquivos `.env`.
- Bootstrap 5 para layout de telas.

## Requitos para rodar em ambientes locais
Para esse sistema rodar em sua máquina local é necessário seguir o passo a passo abaixo:

Instalar o python mais recente em sua máquina (link abaixo para instalação):
``` bash
    https://www.python.org/downloads/
```

Na pasta criada do projeto, criar ambiente virtual python em sua máquina (Via CMD ou terminal do vscode):
```bash
    virtualenv venv
```

Na pasta criada do projeto, ativar o ambiente virtual em sua máquina (Via CMD ou terminal do vscode):
```bash
    .\venv\Scripts\activate
```

Na pasta criada do projeto, instalar arquivo requirements.txt no ambiente virtual (Via CMD ou terminal do vscode):
```bash
    pip install -r requirements.txt
```

## Variáveis de ambiente
Variáveis de ambiente necessárias para se colocar num arquivo `.env`

`SECRET_KEY` [link para um gerador de chave secreta django](https://django-secret-key-generator.netlify.app/)

`DATABASE_NAME` (Nome do banco de dados)

`DATABASE_USER` (Usuário do banco de dados)

`DATABASE_PASSWORD` (Senha do banco de dados)

`DATABASE_HOST` (Host do banco de dados)

`DATABASE_PORT` (Posta do banco de dados)

## Figma
[Protótipo](https://www.figma.com/proto/akRDlAvVWuKGKvRvDFvoGb/music-hall?node-id=24-1311&t=aeDivQclMouuKIVF-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=24%3A1311)
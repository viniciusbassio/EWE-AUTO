# EWE Auto

Sistema desktop para gerenciamento de ordens de serviço desenvolvido para uma oficina mecânica.

O objetivo desta primeira versão é substituir o controle manual de ordens de serviço, permitindo o cadastro de clientes, veículos, serviços e peças, além da criação e impressão de ordens de serviço.

O projeto foi desenvolvido pensando em ser uma aplicação leve, simples e eficiente, capaz de funcionar em computadores com hardware limitado.

---

# Tecnologias utilizadas

* Python 3.14
* PySide6 (Interface gráfica)
* Qt Designer (Construção das telas)
* SQLite (Banco de dados)
* Git (Controle de versão)
* VS Code (Ambiente de desenvolvimento)

---

# Estrutura do Projeto

```text
EWE-AUTO/
│
├── assets/
├── config/
├── controllers/
├── database/
├── models/
├── reports/
├── services/
├── ui/
├── utils/
├── views/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Arquitetura

O projeto segue uma organização baseada no padrão MVC, separando responsabilidades:

## Models

Responsável pela representação das entidades do sistema.

Exemplos:

* Cliente
* Veículo
* Serviço
* Peça
* Ordem de Serviço

---

## Views

Responsável pelas interfaces gráficas desenvolvidas utilizando PySide6 e Qt Designer.

---

## Controllers

Responsável por intermediar as ações realizadas na interface com as regras da aplicação.

---

## Services

Responsável pelas regras de negócio do sistema.

---

## Database

Responsável pela comunicação com o banco de dados SQLite.

---

# Funcionalidades da Versão 1.0

## Estrutura inicial

* [x] Criação da estrutura de pastas
* [x] Configuração do ambiente virtual
* [x] Configuração do projeto no VS Code
* [x] Configuração do Git
* [x] Criação do arquivo requirements.txt

---

## Banco de Dados

* [x] Criação do banco SQLite
* [x] Modelagem inicial das tabelas
* [x] Criação do schema do banco
* [x] Configuração da conexão com banco de dados
* [x] Inicialização automática do banco

---

## Interface

* [x] Criação da janela principal
* [x] Integração do PySide6 com arquivos `.ui`
* [x] Menu principal do sistema

---

# Módulos da Versão 1.0

## Clientes

* [ ] Cadastro de clientes
* [ ] Busca de clientes
* [ ] Edição de clientes
* [ ] Exclusão de clientes

---

## Veículos

* [ ] Cadastro de veículos
* [ ] Associação entre cliente e veículo
* [ ] Consulta de veículos cadastrados

---

## Serviços

* [ ] Cadastro de serviços realizados pela oficina
* [ ] Definição de valores padrão

---

## Peças

* [ ] Cadastro de peças utilizadas
* [ ] Controle básico de valores

---

## Ordens de Serviço

* [ ] Criação de ordem de serviço
* [ ] Seleção de cliente
* [ ] Seleção de veículo
* [ ] Adição de serviços
* [ ] Adição de peças
* [ ] Cálculo dos valores
* [ ] Alteração de status da ordem
* [ ] Impressão da ordem de serviço

---

## Configurações

* [ ] Cadastro dos dados da oficina
* [ ] Informações utilizadas na impressão das ordens de serviço

---

# Objetivos da Versão 1.0

* Criar um sistema funcional para gerenciamento básico de uma oficina.
* Reduzir o uso de controles manuais em papel.
* Centralizar informações de clientes, veículos e serviços.
* Criar uma base sólida para futuras evoluções.

---

# Como executar o projeto

## Criar ambiente virtual

```bash
python -m venv .venv
```

## Ativar ambiente virtual

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar aplicação

```bash
python main.py
```

---

# Status do Projeto

🚧 Em desenvolvimento - Versão 1.0 (MVP)

---

# Autor

Vinicius dos Santos Bassio

Projeto desenvolvido para fins de estudo, portfólio e aplicação em ambiente real.

# EWE Auto

Sistema desktop para gerenciamento de oficinas mecânicas desenvolvido em Python.

O objetivo da primeira versão é substituir o controle manual de ordens de serviço, permitindo o gerenciamento de clientes, veículos, serviços, peças e ordens de serviço de forma simples, rápida e eficiente.

O projeto foi desenvolvido priorizando baixo consumo de recursos, visando funcionar em computadores com hardware limitado, comuns em pequenas oficinas.

---

# Tecnologias utilizadas

- Python 3.14
- PySide6
- Qt Designer
- SQLite
- Git
- VS Code

---

# Estrutura do Projeto

```text
EWE-AUTO/
│
├── assets/
├── config/
├── database/
├── models/
├── repositories/
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

O projeto utiliza uma arquitetura em camadas (**Layered Architecture**) com aplicação do **Repository Pattern**, separando responsabilidades entre interface, acesso aos dados e regras de negócio.

## Views

Responsáveis pelas interfaces gráficas desenvolvidas com PySide6 e Qt Designer.

Exemplos:

- Tela Principal
- Cadastro de Clientes
- Cadastro de Veículos

---

## Models

Representam as entidades do sistema.

Exemplos:

- Cliente
- Veículo
- Serviço
- Peça
- Ordem de Serviço

---

## Repositories

Responsáveis pelo acesso ao banco de dados.

Centralizam todas as operações de persistência, como:

- Inserção
- Consulta
- Atualização
- Exclusão

---

## Services

Camada destinada às regras de negócio da aplicação.

Na versão atual possui pouca utilização, porém será expandida conforme o crescimento do sistema.

---

## Database

Responsável pela criação da conexão SQLite e inicialização automática do banco de dados.

---

# Funcionalidades da Versão 1.0

## Estrutura inicial

- [x] Estrutura do projeto
- [x] Ambiente virtual
- [x] Configuração do Git
- [x] Requirements
- [x] Organização em camadas

---

## Banco de Dados

- [x] Modelagem inicial
- [x] Schema SQLite
- [x] Inicialização automática
- [x] Conexão com banco

---

## Interface

- [x] Janela principal
- [x] Integração com arquivos `.ui`
- [x] Menu principal do sistema

---

# Módulos da Versão 1.0

## Clientes

- [x] Cadastro de clientes
- [x] Pesquisa de clientes
- [x] Edição de clientes
- [x] Exclusão de clientes

---

## Veículos

- [ ] Cadastro
- [ ] Associação Cliente x Veículo
- [ ] Pesquisa
- [ ] Edição
- [ ] Exclusão

---

## Serviços

- [ ] Cadastro de serviços realizados pela oficina
- [ ] Pesquisa
- [ ] Edição
- [ ] Exclusão

---

## Peças

- [ ] Cadastro de peças utilizadas
- [ ] Pesquisa
- [ ] Edição
- [ ] Exclusão

---

## Ordens de Serviço

- [ ] Criação de ordem de serviço
- [ ] Seleção de cliente
- [ ] Seleção de veículo
- [ ] Inclusão de serviços
- [ ] Inclusão de peças
- [ ] Cálculo automático
- [ ] Alteração de status
- [ ] Impressão

---

## Configurações

- [ ] Dados da oficina
- [ ] Logo
- [ ] Informações para impressão

---

# Objetivos da Versão 1.0

- Desenvolver um sistema funcional para gerenciamento básico de uma oficina.
- Reduzir o controle manual em papel.
- Centralizar informações de clientes e veículos.
- Facilitar a emissão de ordens de serviço.
- Servir como base para futuras evoluções.

---

# Como executar

## Criar ambiente virtual

```bash
python -m venv .venv
```

## Ativar ambiente virtual

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar

```bash
python main.py
```

---

# Status do Projeto

🚧 Em desenvolvimento — MVP (Versão 1.0)

### Progresso atual

- ✅ Estrutura do projeto
- ✅ Banco de dados
- ✅ CRUD de Clientes
- 🚧 CRUD de Veículos
- ⏳ Demais módulos em desenvolvimento

---

# Autor

**Vinicius dos Santos Bassio**

Projeto desenvolvido para estudo, portfólio e utilização em ambiente real.
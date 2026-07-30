# EWE-AUTO

Sistema desktop para gerenciamento de oficinas mecânicas desenvolvido em Python.

O EWE-AUTO foi desenvolvido para informatizar pequenas oficinas mecânicas, substituindo o controle manual em papel por um sistema simples, rápido e de baixo consumo de recursos.

A aplicação permite gerenciar clientes, veículos, peças, serviços e ordens de serviço, além de gerar e imprimir documentos em PDF.

---

# Tecnologias utilizadas

- Python
- PySide6
- Qt Designer
- SQLite
- ReportLab
- PyInstaller
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

O projeto utiliza uma arquitetura em camadas (Layered Architecture) com aplicação do Repository Pattern.

As responsabilidades são separadas entre:

- Interface gráfica (Views)
- Modelos de domínio (Models)
- Persistência de dados (Repositories)
- Regras de negócio (Services)
- Inicialização do banco (Database)

---

# Funcionalidades

## Clientes

- ✅ Cadastro
- ✅ Pesquisa
- ✅ Alteração
- ✅ Exclusão

---

## Veículos

- ✅ Cadastro
- ✅ Associação ao cliente
- ✅ Pesquisa
- ✅ Alteração
- ✅ Exclusão

---

## Serviços

- ✅ Cadastro
- ✅ Pesquisa
- ✅ Alteração
- ✅ Exclusão

---

## Peças

- ✅ Cadastro
- ✅ Pesquisa
- ✅ Alteração
- ✅ Exclusão

---

## Ordens de Serviço

- ✅ Criação
- ✅ Numeração automática
- ✅ Associação Cliente / Veículo
- ✅ Inclusão de peças
- ✅ Inclusão de serviços
- ✅ Cálculo automático dos valores
- ✅ Alteração de status
- ✅ Geração de PDF
- ✅ Impressão

---

## Configurações

- ✅ Dados da oficina
- ✅ Logo da empresa
- ✅ Informações utilizadas nos PDFs

---

# Banco de Dados

- SQLite
- Criação automática do banco
- Inicialização automática do Schema

---

# Distribuição

O sistema pode ser distribuído através de executável gerado pelo PyInstaller, não sendo necessária a instalação do Python na máquina do cliente.

---

# Compatibilidade

- Windows 10
- Windows 11

> Compatibilidade com Windows 7 em processo de validação.

---

# Como executar

## Ambiente virtual

```bash
python -m venv .venv
```

### Ativar

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar

```bash
python main.py
```

---

# Roadmap

## v1.1

- Backup automático
- Dashboard
- Controle de estoque
- Relatórios
- Pesquisa global

---

# Status do Projeto

✅ **Versão 1.0.0 concluída**

Sistema funcional, utilizado em ambiente real e em evolução contínua.

---

# Autor

**Vinicius dos Santos Bassio**

Projeto desenvolvido para estudo, portfólio e utilização em ambiente real.
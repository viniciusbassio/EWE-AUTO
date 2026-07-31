# EWE-AUTO

Sistema desktop para gerenciamento de oficinas mecânicas desenvolvido em Python.

O **EWE-AUTO** foi criado para informatizar pequenas oficinas mecânicas, substituindo o controle manual em papel por um sistema simples, rápido, leve e totalmente offline.

O sistema permite gerenciar clientes, veículos, peças, serviços e ordens de serviço, além de gerar documentos em PDF para impressão.

Atualmente o sistema encontra-se em utilização em ambiente real.

---

# Objetivos do Projeto

- Desenvolver um sistema desktop leve para pequenas oficinas.
- Compatibilidade com hardware antigo.
- Funcionamento totalmente offline.
- Baixo consumo de memória.
- Fácil implantação e manutenção.
---

# Tecnologias utilizadas

- Python 3.8
- PySide2
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

O projeto utiliza uma arquitetura em camadas (Layered Architecture), aplicando o Repository Pattern para desacoplamento da camada de persistência.

As responsabilidades são divididas entre:

- Interface gráfica (Views)
- Modelos de domínio (Models)
- Persistência de dados (Repositories)
- Regras de negócio (Services)
- Inicialização do banco (Database)

---

# Funcionalidades

## Clientes

- Cadastro
- Pesquisa
- Alteração
- Exclusão

## Veículos

- Cadastro
- Associação ao cliente
- Pesquisa
- Alteração
- Exclusão
- Validação de placa duplicada

## Serviços

- Cadastro
- Pesquisa
- Alteração
- Exclusão

## Peças

- Cadastro
- Pesquisa
- Alteração
- Exclusão

## Ordens de Serviço

- Criação
- Numeração automática
- Associação entre cliente e veículo
- Inclusão de peças
- Inclusão de serviços
- Cálculo automático dos valores
- Alteração de status
- Geração de PDF
- Impressão

## Configurações

- Dados da oficina
- Logotipo da empresa
- Informações utilizadas nos PDFs

---

# Banco de Dados

- SQLite
- Criação automática do banco
- Inicialização automática do schema

---

# Distribuição

O sistema é distribuído através de executável gerado com PyInstaller.

Não é necessária a instalação do Python na máquina do cliente.

---

# Compatibilidade

O sistema foi homologado em:

- Windows 7 SP1 (64 bits)
- Windows 10
- Windows 11

---

# Como executar

## Criar ambiente virtual

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

# Build

Gerar o executável:

```powershell
pyinstaller .\EWE-AUTO.spec --clean --noconfirm
```

O executável será gerado na pasta:

```text
dist/
```

---

# Roadmap

## v1.1

- Instalador (Inno Setup)
- Melhorias visuais
- Manual do usuário
- Backup automático
- Melhorias de usabilidade

## Futuro

- Dashboard
- Controle de estoque
- Relatórios gerenciais
- Pesquisa global
- Atualizador do sistema

---

# Status do Projeto

**Versão atual:** 1.0.0

✅ Sistema implantado e em utilização em ambiente real.

O projeto encontra-se em evolução contínua, recebendo melhorias com base no uso da oficina.

---

# Licença

Projeto desenvolvido para fins de estudo, portfólio e utilização em ambiente real.

---

# Autor

**Vinicius dos Santos Bassio**
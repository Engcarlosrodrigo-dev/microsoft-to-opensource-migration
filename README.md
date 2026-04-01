[README.md](https://github.com/user-attachments/files/26392188/README.md)
# 🔄 Microsoft Stack → Modern Open Source
## Redução de 65% nos custos de dados para empresa de 200 funcionários

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Anthropic-black?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

---

## 📋 Sobre o Projeto

Este projeto demonstra a migração completa de uma empresa de **200 funcionários** de uma stack Microsoft cara para uma arquitetura moderna, open source e orientada a IA — com **redução de 65% nos custos mensais**.

> 💡 **Contexto real:** Empresa do setor administrativo, 200 colaboradores, utilizando Power BI Pro, Azure SQL, Azure Data Factory e Microsoft 365 Business Standard.

---

## 💸 Análise de Custos — Antes vs Depois

### ANTES — Stack Microsoft

| Produto | Custo Unit. | Usuários | Total/mês (USD) | Total/mês (BRL) |
|---|---|---|---|---|
| Power BI Pro | $14/usuário | 50 | $700 | R$ 4.060 |
| Microsoft 365 Business Standard | $14/usuário | 200 | $2.800 | R$ 16.240 |
| Azure SQL Database | $300/mês | 1 instância | $300 | R$ 1.740 |
| Azure Data Factory | $500/mês | — | $500 | R$ 2.900 |
| **TOTAL** | | | **$4.300/mês** | **R$ 24.940/mês** |

### DEPOIS — Stack Open Source + IA

| Produto | Custo/mês (USD) | Custo/mês (BRL) |
|---|---|---|
| PostgreSQL (self-hosted) | $0 | R$ 0 |
| Python + Pandas + Plotly + Streamlit | $0 | R$ 0 |
| Claude API (insights automáticos) | $50 | R$ 290 |
| VPS Cloud (servidor) | $30 | R$ 174 |
| Microsoft 365 Business Basic (só e-mail) | $7/usuário × 200 | R$ 8.120 |
| **TOTAL** | **~$1.480/mês** | **~R$ 8.584/mês** |

### 📊 Resultado

| Métrica | Valor |
|---|---|
| 💰 Economia mensal | **R$ 16.356** |
| 💰 Economia anual | **R$ 196.272** |
| 📉 Redução percentual | **~65%** |
| ⏱️ Tempo de migração estimado | **60-90 dias** |
| 🔄 ROI do projeto | **Payback em < 1 mês** |

---

## 🏗️ Arquitetura

### ANTES
```
[Fontes de Dados]
      ↓
[Azure Data Factory] → ETL pago por execução
      ↓
[Azure SQL Database] → licença cara
      ↓
[Power BI Pro] → $14/usuário/mês
      ↓
[Usuários] → todos precisam de licença paga
```

### DEPOIS
```
[Fontes de Dados]
      ↓
[Python ETL Pipeline] → open source, gratuito
      ↓
[PostgreSQL] → open source, gratuito
      ↓
[Streamlit + Plotly Dashboards] → gratuito
      ↓              ↓
[Usuários]    [Claude API] → insights automáticos
              análises em linguagem natural
```

---

## 📂 Estrutura do Projeto

```
microsoft-to-opensource-migration/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   └── cost_analysis.md          # Análise detalhada de custos
├── database/
│   ├── schema.sql                # Schema PostgreSQL
│   └── migration_script.py      # Migração SQL Server → PostgreSQL
├── pipelines/
│   ├── ingestion.py              # Substituição do Azure Data Factory
│   ├── transformation.py         # Transformações em Python
│   └── scheduler.py              # Agendamento de pipelines
├── dashboards/
│   ├── dashboard_vendas.py       # Dashboard de vendas (substitui Power BI)
│   ├── dashboard_financeiro.py   # Dashboard financeiro
│   └── app.py                    # Servidor Streamlit principal
└── ai_insights/
    └── claude_analyst.py         # Análises automáticas com Claude API
```

---

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/Engcarlosrodrigo-dev/microsoft-to-opensource-migration.git
cd microsoft-to-opensource-migration
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

### 4. Execute a migração do banco
```bash
python database/migration_script.py
```

### 5. Execute o pipeline ETL
```bash
python pipelines/ingestion.py
```

### 6. Inicie os dashboards
```bash
streamlit run dashboards/app.py
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Substitui | Economia |
|---|---|---|
| PostgreSQL | Azure SQL Database | ~R$ 1.740/mês |
| Python + Pandas | Azure Data Factory | ~R$ 2.900/mês |
| Streamlit + Plotly | Power BI Pro | ~R$ 4.060/mês |
| Claude API | Análises manuais | Horas de trabalho |
| Microsoft 365 Basic | M365 Business Standard | ~R$ 8.120/mês |

---

## 👨‍💻 Autor

**Carlos Rodrigo** — AI Engineer | Data Engineer | GenAI Specialist

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/Engcarlosrodrigo-dev)

---

## 📜 Licença

MIT License — veja [LICENSE](LICENSE) para detalhes.

# FinTrack - Gestão Financeira Inteligente

> Sistema web Full-Stack de controle financeiro pessoal, focado em inteligência de dados, automação de despesas e visualização clara do seu patrimônio.

[![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)](https://github.com/DataGusIT/FinTrack)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20)](https://www.djangoproject.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

## 🎯 Sobre o Projeto

O **FinTrack** é uma plataforma desenvolvida para transformar a forma como as pessoas lidam com o dinheiro. Mais do que um simples rastreador de gastos, o sistema atua como um consultor financeiro digital, oferecendo **insights preditivos**, **KPIs de performance** e **automação de rotinas**.

O projeto utiliza uma arquitetura robusta em Django, garantindo total isolamento de dados entre usuários (Multi-tenancy) e uma interface de nível premium, inspirada nos melhores softwares SaaS de gestão bancária moderna.

## 🖼️ Demonstração Visual (UI Premium)

| Dashboard Analítico | Gestão de Orçamentos | Extrato Avançado |
| :---: | :---: | :---: |
| <img alt="Dashboard" src="https://via.placeholder.com/600x400?text=Dashboard+FinTrack" /> | <img alt="Metas" src="https://via.placeholder.com/600x400?text=Gestão+de+Metas" /> | <img alt="Extrato" src="https://via.placeholder.com/600x400?text=Extrato+com+Filtros" /> |
| **Interface de Login** | **Controle de Categorias** | **Relatórios em CSV** |
| <img alt="Login" src="https://via.placeholder.com/600x400?text=Login+Split-Screen" /> | <img alt="Categorias" src="https://via.placeholder.com/600x400?text=Categorias+Coloridas" /> | <img alt="Relatórios" src="https://via.placeholder.com/600x400?text=Exportação+Excel" /> |

## ✨ Funcionalidades Principais

### 📊 Inteligência Analítica e BI
-   **Dashboard 360°:** Visualização instantânea de Saldo, Receitas e Despesas com indicadores de "Consumo de Renda".
-   **KPIs Preditivos:** Cálculo em tempo real da **Taxa de Poupança**, **Média Diária de Gastos** e **Projeção de Saldo** para o fim do mês.
-   **Gráficos Interativos:** Distribuição de gastos por categoria (Doughnut Chart) e Evolução Mensal Histórica (Bar Chart) via Chart.js.

### ⚙️ Automação e Gestão
-   **Transações Recorrentes:** Motor de automação para geração automática de contas fixas (Netflix, Aluguel, Academia) com status pendente para conciliação manual.
-   **Sistema de Metas (Budgets):** Definição de limites mensais por categoria com barras de progresso que emitem alertas visuais e pulsam ao atingir 100%.
-   **Busca Avançada:** Filtros dinâmicos por descrição, categoria, tipo, status de pagamento e intervalo de datas.

### 👤 Personalização e Segurança
-   **Perfil Multi-Usuário:** Isolamento total de dados e suporte a upload de foto de perfil.
-   **Preferências Globais:** Escolha de moeda preferida (BRL, USD, EUR) com adaptação automática de símbolos em todo o sistema.
-   **Status de Transação:** Controle granular de fluxos financeiros (Pago, Pendente, Cancelado).

### 🚀 Experiência do Usuário (UX/UI)
-   **Design Premium:** Interface com Sidebar colapsável, layouts "Split-Screen" para autenticação e fundos dinâmicos em Mesh Gradient.
-   **Feedback em Toasts:** Sistema de notificações animadas para ações de sucesso, erro e alertas de validação.
-   **Portabilidade:** Exportação completa de extratos filtrados para formato CSV (Excel/Google Sheets).

## 🛠️ Tecnologias Utilizadas

### Backend & Core
-   **Python 3.12**
-   **Django 5.0** (Framework Web)
-   **Python-Decouple** (Gestão de variáveis de ambiente)
-   **Python-Dateutil** (Lógica complexa de recorrências)

### Frontend
-   **Tailwind CSS** (Estilização Moderna e Responsiva)
-   **JavaScript** (Interatividade e Gestão de Toasts)
-   **Chart.js** (Renderização de Gráficos Analíticos)
-   **FontAwesome** (Iconografia Profissional)

### Infraestrutura & Deploy
-   **PostgreSQL** (Banco de dados de produção via Supabase)
-   **Render** (Hosting da aplicação)
-   **WhiteNoise** (Serviço otimizado de arquivos estáticos e mídia)

## 🚀 Instalação e Uso Local

1.  **Clone o repositório**
    ```bash
    git clone https://github.com/DataGusIT/FinTrack.git
    cd FinTrack
    ```

2.  **Configuração do Ambiente**
    ```bash
    python -m venv venv
    # Ative o venv (Windows: venv\Scripts\activate | Linux: source venv/bin/activate)
    pip install -r requirements.txt
    ```

3.  **Variáveis de Ambiente**
    Crie um arquivo `.env` na raiz e configure sua `SECRET_KEY` e `DATABASE_URL`.

4.  **Banco de Dados e Superuser**
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5.  **Popular Dados de Teste (Opcional)**
    ```bash
    python manage.py populate_data seu_usuario
    ```

6.  **Rodar o Servidor**
    ```bash
    python manage.py runserver
    ```

## 📬 Contato

-   **Desenvolvedor**: [Gustavo Moreno](https://www.linkedin.com/in/gustavo-moreno-8a925b26a/)
-   **E-mail**: [g.moreno.souza05@gmail.com](mailto:g.moreno.souza05@gmail.com)
-   **GitHub**: [@DataGusIT](https://github.com/DataGusIT)

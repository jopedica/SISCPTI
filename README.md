# SisCPTI — Sistema de Gestão do Caderno de Projetos de TI (UniCEUB)

Protótipo funcional de sistema web desenvolvido em Flask (Python), com o objetivo de centralizar, acompanhar e documentar os Projetos Integradores (PI/PF) dos cursos de Tecnologia da Informação do Centro Universitário de Brasília — UniCEUB.

A proposta é demonstrar a arquitetura, a interface e o fluxo de funcionamento de uma aplicação que, futuramente, poderá ser expandida para um sistema completo com banco de dados e autenticação avançada.
---


##  **Objetivos do Projeto**

> “Centralizar, acompanhar e documentar os Projetos Integradores de TI, promovendo transparência, integração e inovação.”

O SisCPTI foi criado para:
- Reunir todos os projetos de TI desenvolvidos pelos cursos do UniCEUB.
- Facilitar a gestão e acompanhamento de iniciativas por professores e alunos.
- Permitir a sugestão de novos projetos por meio de submissões diretas.
- Tornar o processo de alocação e acompanhamento mais ágil e acessível.

---

## **Funcionalidades Principais**

### **Usuários**
- Login e cadastro de novos usuários.
- Perfis diferenciados: **admin** e **usuário comum**.

### **Área Pública**
- Exibição de todos os projetos de TI, separados por categoria:
  - Responsabilidade Social
  - Projetos do CEUB
  - Projetos de Empresas do Setor Privado
- Página de detalhes de cada projeto.
- Botão **“Tenho Interesse”** (visível apenas para usuários logados).

### **Área Administrativa (CRUD)**
- Adição, edição e exclusão de projetos.
- Visualização de todos os projetos no painel `/admin`.
- Proteção por autenticação (`role = admin`).

### **Submissão de Projetos**
- Formulário para docentes e parceiros proporem novas ideias.
- Armazenamento das submissões em `submissoes.json`.

---

## **Tecnologias Utilizadas**

| Tecnologia | Função |
|-------------|--------|
| **Python 3.11+** | Linguagem principal |
| **Flask** | Framework web |
| **Jinja2** | Templates dinâmicos |
| **HTML5 + CSS3** | Estrutura e design |
| **JSON Files** | Armazenamento simples de dados |
| **VS Code / Git** | Ambiente de desenvolvimento e controle de versão |

---

# 🦇 E.D.I.T.H. (Personal AI Assistant)

Assistente virtual de alta performance desenvolvida em Python, integrando **Visão Computacional Local**, **LLMs** e **Análise de Dados em Tempo Real**.

Projeto criado para demonstrar arquitetura de software moderna, integração de APIs e engenharia de dados.

## 🧠 Arquitetura & Tecnologias

- **Cérebro (Core):** LangChain + Ollama (Modelos: Qwen 2.5 & LLaVA).
- **Interface (GUI):** CustomTkinter (Modo HUD Transparente/Fantasma).
- **Banco de Dados:** Neon Tech (PostgreSQL) - Monitoramento de Preços na Nuvem.
- **Visão:** Pipeline de captura e análise de tela em tempo real via LMM (Large Multimodal Model).
- **Automação:** Controle total do SO via PyAutoGUI.

## 🚀 Funcionalidades Chave

1.  **Vigilante de Preços:** Monitora e grava preços de produtos no banco Neon PostgreSQL.
2.  **Analista de Mercado:** Calcula tendências (Desvio Padrão/Média) para recomendar compras ("Está barato?").
3.  **Visão Heimdall:** "Olha" para a tela do usuário e descreve/analisa o conteúdo visualmente.
4.  **Memória Persistente:** Lembra de conversas passadas e preferências do usuário.

## 🛠️ Instalação

1.  Clone o repositório.
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure o arquivo `.env` com suas chaves (Neon DB, etc).
4.  Certifique-se de ter o [Ollama](https://ollama.com/) rodando com os modelos:
    ```bash
    ollama pull qwen2.5:7b
    ollama pull llava
    ```

## 🦇 Como usar

Execute o comando principal para iniciar o HUD:

```bash
python interface.py
```

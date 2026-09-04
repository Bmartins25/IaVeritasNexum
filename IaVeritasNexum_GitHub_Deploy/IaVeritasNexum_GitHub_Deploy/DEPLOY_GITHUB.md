# Veritas Nexum — pacote para deploy

Arquivos essenciais para publicar o MVP Streamlit.

Estrutura:

- `app.py` — aplicação principal
- `criteria.json` — critérios do FAC-IA
- `requirements.txt` — dependências Python
- `.streamlit/config.toml` — configuração do Streamlit
- `assets/` — imagens usadas pela aplicação
- `.gitignore` — impede publicação de banco local, cache e segredos

O arquivo `veritas_nexum.db` não foi incluído. A própria aplicação cria o banco SQLite quando executada.

Para o Streamlit Community Cloud, use `app.py` como Main file path.

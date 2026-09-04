# Veritas Nexum — MVP de Governança e IA Responsável

Versão reestruturada da Veritas para seguir a mesma arquitetura operacional do FAC-IA Saúde: aplicação Streamlit com navegação lateral, cadastro, avaliações, critérios, evidências, score, maturidade, riscos, plano de ação e relatório.

## O que mudou
- A antiga arquitetura de site institucional foi preservada em `legacy_site/` para referência.
- A nova interface usa o mesmo padrão visual e de navegação do FAC-IA Saúde.
- Cadastro de organizações e sistemas de IA.
- Avaliações independentes por sistema.
- 45 critérios em 5 domínios adaptados para uso organizacional geral.
- Evidências, justificativas e recomendações por critério.
- Score ponderado por peso e criticidade.
- Nível de maturidade, lacunas críticas e dashboard por domínio.
- Plano de ação consolidado.
- Relatório em Markdown para download.
- Banco SQLite local, criado automaticamente.

## Como executar no Windows
Dê dois cliques em `INICIAR_WINDOWS.bat`.

Ou, no terminal:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Escala de avaliação
- 0 — Não atendido
- 1 — Inicial / evidência insuficiente
- 2 — Parcialmente atendido
- 3 — Atendido
- 4 — Atendido e evidenciado

> MVP para teste e validação. A parametrização dos critérios, pesos, criticidades e faixas de maturidade deve ser validada antes de uso comercial ou decisório definitivo.

**Desenvolvido por Bruno Bartolomeu • 2026**

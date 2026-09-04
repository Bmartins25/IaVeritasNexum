import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DB = APP_DIR / "veritas_nexum.db"
CRITERIA_FILE = APP_DIR / "criteria.json"
LOGO = APP_DIR / "assets" / "veritas_logo.jpeg"
FOUNDER_PHOTO = APP_DIR / "assets" / "fundador.jpg"

st.set_page_config(
    page_title="Veritas Nexum | IA Responsável",
    page_icon="VN",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root {
  --vx-navy:#103B60; --vx-deep:#0A2C4A; --vx-teal:#0B8F87; --vx-aqua:#22B7AF;
  --vx-green:#3B9B76; --vx-mint:#DFF4EF; --vx-pale:#F1FAF8; --vx-blue:#2476A8;
  --vx-text:#173D4B; --vx-muted:#607985; --vx-amber:#D89A2B; --vx-red:#C95353; --vx-border:#CFE5E2;
}
html, body, [class*="css"] {font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;}
.stApp {background:linear-gradient(180deg,#F7FBFB 0%,#FFFFFF 46%); color:var(--vx-text);}
.block-container {padding-top:1.1rem; padding-bottom:3.2rem; max-width:1320px;}
header[data-testid="stHeader"] {background:#F7FBFB !important; height:2.4rem;}
[data-testid="stToolbar"] {right:1rem;}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#103B60 0%,#0C6975 54%,#0B8F87 100%); border-right:0;}
[data-testid="stSidebar"] * {color:#F7FFFF !important;}
[data-testid="stSidebar"] [role="radiogroup"] label {border-radius:10px; padding:.42rem .55rem;}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {background:rgba(255,255,255,.10);}
[data-testid="stSidebar"] hr {border-color:rgba(255,255,255,.20);}
.sidebar-logo {background:#FFFFFF; border-radius:14px; padding:8px; margin:0 0 12px 0; box-shadow:0 6px 20px rgba(0,0,0,.12);}
h1,h2,h3 {color:var(--vx-navy); letter-spacing:-.02em;}
h1 {border-bottom:3px solid var(--vx-aqua); padding-bottom:.35rem;}
[data-testid="stMetric"] {background:#FFFFFF; border:1px solid var(--vx-border); border-top:4px solid var(--vx-teal); border-radius:14px; padding:14px 16px; box-shadow:0 4px 16px rgba(23,61,75,.06);}
[data-testid="stMetricValue"] {color:var(--vx-navy);}
.stButton > button, .stDownloadButton > button {border-radius:10px; border:1px solid var(--vx-teal); font-weight:650;}
button[kind="primary"], .stButton > button[kind="primary"] {background:var(--vx-teal) !important; border-color:var(--vx-teal) !important; color:white !important;}
.stButton > button:hover, .stDownloadButton > button:hover {border-color:var(--vx-green) !important; color:var(--vx-green) !important;}
[data-testid="stExpander"] {border:1px solid var(--vx-border); border-radius:12px; background:#FFFFFF;}
[data-testid="stAlert"] {border-radius:12px;}
[data-testid="stDataFrame"] {border:1px solid var(--vx-border); border-radius:12px; overflow:hidden;}
.stTextInput input, .stNumberInput input, .stTextArea textarea,
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
  background:#FFFFFF !important; color:var(--vx-text) !important;
  -webkit-text-fill-color:var(--vx-text) !important; border:1px solid #B9DAD6 !important; border-radius:9px !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
  border-color:var(--vx-teal) !important; box-shadow:0 0 0 1px var(--vx-teal) !important;
}
[data-baseweb="select"] > div {background:#FFFFFF !important; color:var(--vx-text) !important; border-color:#B9DAD6 !important;}
[data-baseweb="select"] * {color:var(--vx-text) !important;}
label, [data-testid="stWidgetLabel"] p {color:var(--vx-text) !important; font-weight:600;}
.stForm {background:#FFFFFF; border:1px solid var(--vx-border); border-radius:16px; padding:1.0rem 1.1rem 1.1rem; box-shadow:0 5px 18px rgba(23,61,75,.05);}
.vx-card {border:1px solid var(--vx-border); border-radius:14px; padding:16px 18px; margin-bottom:12px; background:#fff; box-shadow:0 4px 16px rgba(23,61,75,.05);}
.vx-hero {padding:22px 24px;border-radius:18px;background:linear-gradient(120deg,#E3F6F1,#EEF7FB);border:1px solid #CBE7E3;margin-bottom:18px;}
.vx-hero-title {font-size:1.25rem;font-weight:800;color:#173D4B;margin-bottom:5px;}
.vx-hero-sub {color:#42636C;font-size:.96rem;}
.vx-empty {padding:22px;border:1px dashed #A9D6D0;border-radius:16px;background:#F8FCFB;margin:10px 0 16px;}
.vx-step {border-left:4px solid var(--vx-aqua); padding:10px 14px; background:#F6FBFA; border-radius:8px; margin:8px 0;}
.vx-badge {display:inline-block;padding:5px 10px;border-radius:999px;background:var(--vx-mint);color:var(--vx-navy);font-size:.82rem;font-weight:700;}
.vx-risk {border-left:4px solid var(--vx-red); padding:12px 14px; background:#FFF7F7; border-radius:8px; margin:8px 0;}
.vx-ok {border-left:4px solid var(--vx-green); padding:12px 14px; background:#F5FBF8; border-radius:8px; margin:8px 0;}
.vx-footer {text-align:center;color:#607985;font-size:.86rem;padding-top:.5rem;}
/* Sidebar: keep the navigation heading and options high-contrast. */
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p {color:#FFFFFF !important;}
[data-testid="stSidebar"] [role="radiogroup"] {gap:.15rem;}
[data-testid="stSidebar"] [role="radiogroup"] label {color:#FFFFFF !important;}
[data-testid="stSidebar"] [role="radiogroup"] label p {color:#FFFFFF !important;font-weight:650;}

/* Institutional home: intentionally restrained and editorial. */
.vx-home {min-height:68vh;display:flex;flex-direction:column;justify-content:center;padding:3.8rem 1.2rem 5rem;}
.vx-home-kicker {font-size:.82rem;letter-spacing:.19em;text-transform:uppercase;font-weight:750;color:var(--vx-teal);margin-bottom:1.15rem;}
.vx-home-title {max-width:980px;font-size:clamp(2.6rem,5.4vw,5.4rem);line-height:.98;letter-spacing:-.055em;font-weight:850;color:var(--vx-deep);margin:0 0 1.5rem;}
.vx-home-title span {color:var(--vx-teal);}
.vx-home-line {width:96px;height:4px;border-radius:99px;background:var(--vx-aqua);margin:0 0 1.6rem;}
.vx-home-sub {max-width:790px;font-size:clamp(1.05rem,1.55vw,1.35rem);line-height:1.65;color:#46636E;margin-bottom:2.2rem;}
.vx-home-values {display:flex;flex-wrap:wrap;gap:.65rem;}
.vx-home-values span {border:1px solid #BFDCD8;background:rgba(255,255,255,.72);border-radius:999px;padding:.55rem .9rem;font-size:.88rem;font-weight:700;color:var(--vx-navy);}
.vx-home-signature {margin-top:3.2rem;color:#70858D;font-size:.9rem;letter-spacing:.02em;}

.vx-reality {margin:1.5rem 1.2rem 4.5rem;padding-top:2.8rem;border-top:1px solid #DCE8E7;display:grid;grid-template-columns:1.05fr .95fr;gap:3rem;align-items:center;}
.vx-reality-copy h2 {font-size:clamp(1.7rem,2.7vw,2.65rem);line-height:1.12;letter-spacing:-.035em;color:var(--vx-deep);margin:0 0 1rem;}
.vx-reality-copy p {font-size:1.03rem;line-height:1.75;color:#49636D;margin:0 0 1rem;max-width:720px;}
.vx-reality-note {font-size:.92rem!important;color:#6B8088!important;border-left:3px solid var(--vx-aqua);padding-left:1rem;}
.vx-ai-scene {position:relative;min-height:330px;border:1px solid #CFE3E0;border-radius:26px;background:linear-gradient(145deg,#F7FBFB 0%,#EAF7F5 100%);overflow:hidden;box-shadow:0 18px 45px rgba(11,52,78,.08);}
.vx-ai-core {position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:112px;height:112px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#fff;border:2px solid var(--vx-aqua);font-size:2.25rem;font-weight:850;color:var(--vx-deep);box-shadow:0 12px 35px rgba(14,148,139,.18);z-index:3;}
.vx-ai-orbit {position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:245px;height:245px;border:1px dashed rgba(14,148,139,.42);border-radius:50%;}
.vx-ai-node {position:absolute;background:#fff;border:1px solid #C6DFDC;border-radius:16px;padding:.65rem .8rem;font-size:.8rem;font-weight:750;color:var(--vx-navy);box-shadow:0 8px 22px rgba(11,52,78,.07);z-index:2;}
.vx-n1{left:7%;top:15%}.vx-n2{right:7%;top:16%}.vx-n3{left:5%;bottom:17%}.vx-n4{right:5%;bottom:17%}.vx-n5{left:50%;bottom:5%;transform:translateX(-50%)}
.vx-ai-line {position:absolute;height:1px;background:linear-gradient(90deg,transparent,var(--vx-aqua),transparent);width:75%;left:12%;top:50%;opacity:.55;}
@media(max-width:850px){.vx-reality{grid-template-columns:1fr;gap:1.5rem}.vx-ai-scene{min-height:300px}.vx-home{min-height:auto;padding-top:2.2rem}.vx-home-title{font-size:clamp(2.4rem,12vw,4.2rem)}}
</style>
""",
    unsafe_allow_html=True,
)


def conn():
    c = sqlite3.connect(DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with conn() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS systems(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                organization TEXT,
                area TEXT,
                purpose TEXT,
                audience TEXT,
                model_version TEXT,
                owner TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS assessments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                system_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Em andamento',
                evaluator TEXT,
                objective TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(system_id) REFERENCES systems(id)
            );
            CREATE TABLE IF NOT EXISTS answers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assessment_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                weight REAL NOT NULL,
                criticality REAL NOT NULL,
                evidence TEXT,
                justification TEXT,
                recommendation TEXT,
                owner_action TEXT,
                deadline TEXT,
                updated_at TEXT NOT NULL,
                UNIQUE(assessment_id, code),
                FOREIGN KEY(assessment_id) REFERENCES assessments(id)
            );
            """
        )
        # Migração defensiva para bancos criados em versões de teste anteriores.
        cols = {r[1] for r in c.execute("PRAGMA table_info(answers)")}
        for col, typ in [("owner_action", "TEXT"), ("deadline", "TEXT")]:
            if col not in cols:
                c.execute(f"ALTER TABLE answers ADD COLUMN {col} {typ}")


def load_criteria():
    return json.loads(CRITERIA_FILE.read_text(encoding="utf-8"))


def ensure_answers(assessment_id):
    crits = load_criteria()
    now = datetime.now().isoformat(timespec="seconds")
    with conn() as c:
        for x in crits:
            c.execute(
                """INSERT OR IGNORE INTO answers
                (assessment_id, code, score, weight, criticality, evidence, justification, recommendation, owner_action, deadline, updated_at)
                VALUES (?, ?, 0, ?, ?, '', '', '', '', '', ?)""",
                (assessment_id, x["codigo"], x["peso"], x["criticidade"], now),
            )


def systems_df():
    with conn() as c:
        return pd.read_sql_query("SELECT * FROM systems ORDER BY id DESC", c)


def assessments_df():
    with conn() as c:
        return pd.read_sql_query(
            """SELECT a.*, s.name AS system_name, s.organization, s.area
            FROM assessments a JOIN systems s ON s.id=a.system_id
            ORDER BY a.id DESC""",
            c,
        )


def assessment_data(aid):
    crits = pd.DataFrame(load_criteria())
    with conn() as c:
        ans = pd.read_sql_query("SELECT * FROM answers WHERE assessment_id=?", c, params=(aid,))
    return crits.merge(ans, left_on="codigo", right_on="code", how="left")


def calc(df):
    d = df.copy()
    d["weighted"] = (d["score"] / 4.0) * d["weight"] * d["criticality"]
    d["max_weighted"] = d["weight"] * d["criticality"]
    domains = d.groupby("dominio", as_index=False).agg(
        weighted=("weighted", "sum"), max_weighted=("max_weighted", "sum")
    )
    domains["score_pct"] = (100 * domains["weighted"] / domains["max_weighted"]).round(1)
    total = d["max_weighted"].sum()
    global_score = round(100 * d["weighted"].sum() / total, 1) if total else 0
    if global_score < 40:
        maturity = "Inicial"
    elif global_score < 60:
        maturity = "Em desenvolvimento"
    elif global_score < 80:
        maturity = "Estruturado"
    else:
        maturity = "Avançado"
    critical_gaps = d[(d["criticality"] >= 4) & (d["score"] <= 1)]
    return global_score, maturity, domains, critical_gaps


def create_system(name, organization, area, purpose, audience, model_version, owner):
    with conn() as c:
        cur = c.execute(
            """INSERT INTO systems(name,organization,area,purpose,audience,model_version,owner,created_at)
               VALUES(?,?,?,?,?,?,?,?)""",
            (name, organization, area, purpose, audience, model_version, owner, datetime.now().isoformat(timespec="seconds")),
        )
        return cur.lastrowid


def create_assessment(sid, title, evaluator, objective):
    now = datetime.now().isoformat(timespec="seconds")
    with conn() as c:
        cur = c.execute(
            """INSERT INTO assessments(system_id,title,status,evaluator,objective,created_at,updated_at)
               VALUES(?,?, 'Em andamento', ?, ?, ?, ?)""",
            (sid, title, evaluator, objective, now, now),
        )
        aid = cur.lastrowid
    ensure_answers(aid)
    st.session_state["aid"] = aid
    return aid


def active_assessment_selector(label="Avaliação"):
    adf = assessments_df()
    if adf.empty:
        return None
    opts = adf.id.astype(int).tolist()
    if st.session_state.get("aid") in opts:
        idx = opts.index(st.session_state["aid"])
    else:
        idx = 0
    aid = st.selectbox(
        label,
        opts,
        index=idx,
        format_func=lambda x: f"#{x} — {adf.loc[adf.id==x, 'title'].iloc[0]}",
    )
    st.session_state["aid"] = int(aid)
    return int(aid)


def empty_intro(title, text, steps):
    st.markdown(
        f"<div class='vx-empty'><div class='vx-hero-title'>{title}</div><div class='vx-hero-sub'>{text}</div></div>",
        unsafe_allow_html=True,
    )
    for s in steps:
        st.markdown(f"<div class='vx-step'>{s}</div>", unsafe_allow_html=True)


def report_markdown(aid):
    adf = assessments_df()
    row = adf[adf.id == aid].iloc[0]
    d = assessment_data(aid)
    score, maturity, domains, gaps = calc(d)
    lines = [
        f"# Relatório Veritas Nexum — {row['title']}", "",
        f"**Sistema de IA:** {row['system_name']}",
        f"**Organização:** {row['organization'] or '-'}",
        f"**Área:** {row['area'] or '-'}",
        f"**Avaliador:** {row['evaluator'] or '-'}",
        f"**Objetivo:** {row['objective'] or '-'}",
        f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}", "",
        "## Resultado global",
        f"- Score Veritas: **{score}%**",
        f"- Nível de maturidade: **{maturity}**",
        f"- Lacunas críticas: **{len(gaps)}**", "",
        "## Scores por domínio",
    ]
    for _, r in domains.iterrows():
        lines.append(f"- {r['dominio']}: **{r['score_pct']}%**")
    lines += ["", "## Não conformidades e recomendações prioritárias"]
    gaps2 = d[d["score"] <= 1].sort_values(["criticidade", "peso"], ascending=False)
    if gaps2.empty:
        lines.append("- Nenhuma lacuna com nota 0 ou 1 foi registrada.")
    else:
        for _, r in gaps2.iterrows():
            rec = str(r.get("recommendation") or "").strip() or "Definir plano de adequação, responsável, evidência esperada e prazo."
            own = str(r.get("owner_action") or "").strip() or "A definir"
            ddl = str(r.get("deadline") or "").strip() or "A definir"
            lines.append(f"- **{r['codigo']} — {r['criterio']}** | nota {int(r['score'])}/4 | recomendação: {rec} | responsável: {own} | prazo: {ddl}")
    lines += [
        "", "## Nota metodológica",
        "O score utiliza regra determinística ponderada: (nota/4) × peso × criticidade. Pesos, criticidades e faixas de maturidade são parametrizáveis e devem ser validados para o contexto de uso.", "",
        "Veritas Nexum — MVP de apoio à governança, avaliação e uso responsável de IA. Não substitui auditoria independente, parecer jurídico, avaliação regulatória ou decisão profissional especializada.",
    ]
    return "\n".join(lines)


init_db()

with st.sidebar:
    if LOGO.exists():
        st.markdown("<div class='sidebar-logo'>", unsafe_allow_html=True)
        st.image(str(LOGO), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("## Veritas Nexum")
    st.caption("Inteligência Artificial • Dados • Governança")
    page = st.radio(
        "NAVEGAÇÃO",
        ["Início", "Sobre a Veritas", "Fundador", "Sistemas avaliados", "Nova avaliação", "Avaliar critérios", "Resultados", "Plano de ação", "Relatório", "Contato"],
    )
    st.divider()
    st.caption("Consultoria em IA Responsável • Capacitação • Governança • Diagnóstico")

if page == "Início":
    st.markdown(
        """
        <section class="vx-home">
          <div class="vx-home-kicker">VERITAS NEXUM · IA RESPONSÁVEL</div>
          <div class="vx-home-title">Inteligência Artificial com <span>consciência, critério e confiança.</span></div>
          <div class="vx-home-line"></div>
          <div class="vx-home-sub">
            Conhecimento para compreender. Critério para decidir. Responsabilidade para aplicar.
          </div>
          <div class="vx-home-values">
            <span>IA Responsável</span>
            <span>Governança</span>
            <span>Capacitação</span>
            <span>Dados</span>
            <span>Confiança</span>
          </div>
          <div class="vx-home-signature">Tecnologia com verdade. Decisões com confiança.</div>
        </section>

        <section class="vx-reality">
          <div class="vx-reality-copy">
            <div class="vx-home-kicker">IA NO MUNDO REAL</div>
            <h2>A Inteligência Artificial já participa de decisões, processos e experiências cotidianas.</h2>
            <p>Ela apoia análises financeiras, atendimento a clientes, saúde, educação, segurança, indústria, criação de conteúdo e produtividade. Quanto maior sua presença, maior também a necessidade de compreender limites, riscos e responsabilidades.</p>
            <p>A questão deixou de ser apenas <strong>“como usar IA?”</strong>. Profissionais e organizações precisam saber <strong>quando usar, por que usar e como usar com responsabilidade</strong>.</p>
            <p class="vx-reality-note">É nesse espaço entre inovação e responsabilidade que a Veritas Nexum atua.</p>
          </div>
          <div class="vx-ai-scene" role="img" aria-label="Ilustração da Inteligência Artificial conectando aplicações do mundo real">
            <div class="vx-ai-line"></div>
            <div class="vx-ai-orbit"></div>
            <div class="vx-ai-core">IA</div>
            <div class="vx-ai-node vx-n1">Saúde</div>
            <div class="vx-ai-node vx-n2">Finanças</div>
            <div class="vx-ai-node vx-n3">Educação</div>
            <div class="vx-ai-node vx-n4">Empresas</div>
            <div class="vx-ai-node vx-n5">Pessoas &amp; Decisões</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

elif page == "Sistemas avaliados":
    st.title("Sistemas avaliados")
    st.caption("Registre sistemas, modelos ou aplicações de IA para apoiar diagnósticos orientativos e atividades de capacitação da Veritas Nexum.")
    with st.expander("➕ Cadastrar novo sistema", expanded=True):
        with st.form("new_system"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Nome do sistema/modelo *", placeholder="Ex.: Assistente de IA para atendimento")
            organization = c2.text_input("Organização", placeholder="Ex.: Empresa / universidade / hospital")
            c3, c4 = st.columns(2)
            area = c3.text_input("Área responsável", placeholder="Ex.: Tecnologia, RH, Compliance")
            owner = c4.text_input("Responsável institucional", placeholder="Nome ou função")
            purpose = st.text_area("Finalidade", placeholder="Descreva a decisão, processo ou atividade apoiada pela IA.")
            audience = st.text_input("Público / contexto-alvo", placeholder="Ex.: Clientes, colaboradores, analistas")
            model_version = st.text_input("Versão", placeholder="Ex.: v1.0")
            ok = st.form_submit_button("Cadastrar sistema", type="primary")
            if ok:
                if not name.strip():
                    st.error("Informe o nome do sistema/modelo.")
                else:
                    create_system(name, organization, area, purpose, audience, model_version, owner)
                    st.success("Sistema cadastrado com sucesso.")
                    st.rerun()
    sdf = systems_df()
    if sdf.empty:
        empty_intro("Nenhum sistema cadastrado", "Preencha o formulário acima para iniciar o diagnóstico.", ["O nome do sistema é o único campo obrigatório.", "Registre contexto e responsável para aumentar a rastreabilidade do relatório."])
    else:
        st.markdown("### Sistemas cadastrados")
        st.dataframe(sdf[["id", "name", "organization", "area", "purpose", "audience", "model_version", "owner"]], use_container_width=True, hide_index=True)

elif page == "Nova avaliação":
    st.title("Nova avaliação Veritas")
    st.caption("Crie uma rodada independente de diagnóstico para um sistema já cadastrado.")
    sdf = systems_df()
    if sdf.empty:
        empty_intro("Primeiro cadastre um sistema", "Nenhuma avaliação pode ser criada sem um sistema de IA associado.", ["Acesse ‘Sistemas avaliados’.", "Cadastre o sistema e retorne a esta página."])
    else:
        labels = {int(r.id): f"{r['name']} — {r['organization'] or 'Sem organização'}" for _, r in sdf.iterrows()}
        with st.form("new_assessment"):
            sid = st.selectbox("Sistema", list(labels.keys()), format_func=lambda x: labels[x])
            c1, c2 = st.columns([2, 1])
            title = c1.text_input("Título da avaliação", value=f"Diagnóstico Veritas — {labels[sid].split(' — ')[0]}")
            evaluator = c2.text_input("Avaliador", placeholder="Nome do avaliador")
            objective = st.text_area("Objetivo / escopo", placeholder="Ex.: Diagnóstico inicial de governança, riscos e conformidade do sistema.")
            ok = st.form_submit_button("Criar avaliação com 45 critérios", type="primary")
            if ok:
                aid = create_assessment(sid, title, evaluator, objective)
                st.success(f"Avaliação #{aid} criada. Vá para ‘Avaliar critérios’.")
        adf = assessments_df()
        if not adf.empty:
            st.markdown("### Avaliações existentes")
            st.dataframe(adf[["id", "system_name", "organization", "title", "status", "evaluator", "updated_at"]], use_container_width=True, hide_index=True)

elif page == "Avaliar critérios":
    st.title("Avaliar critérios")
    st.caption("Escala: 0 = não atendido • 1 = inicial • 2 = parcial • 3 = atendido • 4 = atendido e evidenciado")
    aid = active_assessment_selector()
    if aid is None:
        empty_intro("Nenhuma avaliação disponível", "Crie uma avaliação antes de preencher os critérios.", ["Cadastre um sistema.", "Crie uma rodada em ‘Nova avaliação’. "])
    else:
        ensure_answers(aid)
        d = assessment_data(aid)
        domains = d["dominio"].drop_duplicates().tolist()
        dom = st.selectbox("Domínio", domains)
        sub = d[d["dominio"] == dom].copy()
        st.markdown(f"### {dom}")
        st.progress(float((sub["score"] > 0).mean()), text=f"{int((sub['score'] > 0).sum())} de {len(sub)} critérios com nota acima de zero")
        for _, r in sub.iterrows():
            code = r["codigo"]
            with st.expander(f"{code} — {r['criterio']} | nota atual: {int(r['score'])}/4"):
                st.markdown(f"**Pergunta de verificação:** {r['verificacao']}")
                st.caption(f"Peso: {r['peso']} • Criticidade: {r['criticidade']}")
                with st.form(f"form_{aid}_{code}"):
                    score = st.select_slider("Nota", options=[0, 1, 2, 3, 4], value=int(r["score"]), key=f"score_{aid}_{code}")
                    evidence = st.text_area("Evidência", value=str(r.get("evidence") or ""), placeholder="Documento, política, registro, log, teste, evidência técnica ou processo que sustenta a nota.")
                    justification = st.text_area("Justificativa", value=str(r.get("justification") or ""), placeholder="Explique por que a nota foi atribuída.")
                    recommendation = st.text_area("Recomendação", value=str(r.get("recommendation") or ""), placeholder="Descreva a adequação recomendada quando houver lacuna.")
                    c1, c2 = st.columns(2)
                    owner_action = c1.text_input("Responsável pela ação", value=str(r.get("owner_action") or ""), placeholder="Área ou pessoa")
                    deadline = c2.text_input("Prazo", value=str(r.get("deadline") or ""), placeholder="Ex.: 30 dias / 15-10-2026")
                    save = st.form_submit_button("Salvar critério", type="primary")
                    if save:
                        now = datetime.now().isoformat(timespec="seconds")
                        with conn() as c:
                            c.execute(
                                """UPDATE answers SET score=?, evidence=?, justification=?, recommendation=?, owner_action=?, deadline=?, updated_at=?
                                   WHERE assessment_id=? AND code=?""",
                                (score, evidence, justification, recommendation, owner_action, deadline, now, aid, code),
                            )
                            c.execute("UPDATE assessments SET updated_at=? WHERE id=?", (now, aid))
                        st.success(f"{code} salvo.")
                        st.rerun()

elif page == "Resultados":
    st.title("Resultados")
    aid = active_assessment_selector()
    if aid is None:
        empty_intro("Nenhuma avaliação disponível", "Crie e preencha uma avaliação para visualizar resultados.", ["Nova avaliação → Avaliar critérios → Resultados"])
    else:
        d = assessment_data(aid)
        score, maturity, domains, gaps = calc(d)
        a, b, c, e = st.columns(4)
        a.metric("Score Veritas", f"{score}%")
        b.metric("Maturidade", maturity)
        c.metric("Lacunas críticas", len(gaps))
        e.metric("Critérios avaliados", f"{int((d['score']>0).sum())}/45")
        st.markdown("### Score por domínio")
        st.bar_chart(domains.set_index("dominio")[["score_pct"]], horizontal=True)
        st.dataframe(domains[["dominio", "score_pct"]].rename(columns={"dominio":"Domínio", "score_pct":"Score (%)"}), use_container_width=True, hide_index=True)
        st.markdown("### Lacunas críticas")
        if gaps.empty:
            st.markdown("<div class='vx-ok'>Nenhuma lacuna de alta criticidade com nota 0 ou 1 foi identificada.</div>", unsafe_allow_html=True)
        else:
            for _, r in gaps.sort_values(["criticidade", "peso"], ascending=False).iterrows():
                st.markdown(f"<div class='vx-risk'><b>{r['codigo']} — {r['criterio']}</b><br>Nota {int(r['score'])}/4 • Criticidade {r['criticidade']} • Peso {r['peso']}</div>", unsafe_allow_html=True)

elif page == "Plano de ação":
    st.title("Plano de ação")
    st.caption("Consolide as lacunas em uma lista executiva de adequações, responsáveis e prazos.")
    aid = active_assessment_selector()
    if aid is None:
        empty_intro("Nenhuma avaliação disponível", "O plano de ação é gerado a partir dos critérios avaliados.", ["Preencha os critérios e registre recomendações, responsáveis e prazos."])
    else:
        d = assessment_data(aid)
        action = d[d["score"] <= 2].copy()
        if action.empty:
            st.success("Não há critérios com nota 0, 1 ou 2 para compor o plano de ação.")
        else:
            action["Prioridade"] = action.apply(lambda r: "Crítica" if r["criticidade"] >= 4 and r["score"] <= 1 else ("Alta" if r["criticidade"] >= 4 or r["score"] <= 1 else "Moderada"), axis=1)
            out = action[["codigo", "dominio", "criterio", "score", "Prioridade", "recommendation", "owner_action", "deadline"]].copy()
            out.columns = ["Código", "Domínio", "Critério", "Nota", "Prioridade", "Recomendação", "Responsável", "Prazo"]
            st.dataframe(out, use_container_width=True, hide_index=True)
            csv = out.to_csv(index=False).encode("utf-8-sig")
            st.download_button("Baixar plano de ação (CSV)", data=csv, file_name=f"plano_acao_veritas_{aid}.csv", mime="text/csv")

elif page == "Relatório":
    st.title("Relatório")
    aid = active_assessment_selector()
    if aid is None:
        empty_intro("Nenhuma avaliação disponível", "Crie uma avaliação para gerar o relatório.", ["O relatório consolida score, maturidade, domínios, lacunas e recomendações."])
    else:
        report = report_markdown(aid)
        st.download_button("Baixar relatório (.md)", data=report.encode("utf-8"), file_name=f"relatorio_veritas_{aid}.md", mime="text/markdown", type="primary")
        st.markdown(report)

elif page == "Sobre a Veritas":
    st.title("Sobre a Veritas")
    st.markdown(
        """<div class='vx-hero'><div class='vx-hero-title'>Conhecimento para usar Inteligência Artificial com responsabilidade</div><div class='vx-hero-sub'>A Veritas Nexum é uma consultoria de IA Responsável que capacita profissionais e organizações para compreender oportunidades, limites, riscos e boas práticas no uso da Inteligência Artificial.</div></div>""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Capacitação")
        st.write("Palestras, workshops, treinamentos e programas de letramento para transformar princípios de IA Responsável em prática profissional.")
    with c2:
        st.markdown("### Orientação")
        st.write("Apoio na definição de boas práticas, papéis, responsabilidades e formas seguras e conscientes de incorporar IA ao trabalho.")
    with c3:
        st.markdown("### Diagnóstico")
        st.write("Análise orientativa de maturidade, riscos, dados, transparência, governança e práticas de uso de IA, com recomendações de evolução.")
    st.markdown("### Nossa proposta")
    st.write("A Veritas Nexum aproxima profissionais e organizações dos princípios de IA Responsável por meio de conhecimento aplicado, capacitação e orientação. O objetivo é apoiar decisões mais conscientes sobre como adotar, utilizar e governar Inteligência Artificial no trabalho.")
    st.markdown("### Como trabalhamos")
    st.info("Compreender o contexto → Capacitar pessoas → Identificar riscos → Organizar boas práticas → Definir ações → Acompanhar a evolução")
    st.markdown("### Ambiente de apoio")
    st.write("A Veritas Nexum utiliza recursos digitais próprios como apoio às atividades consultivas e educacionais, permitindo organizar diagnósticos, registrar evidências, identificar oportunidades de melhoria e acompanhar planos de evolução em IA Responsável.")
    st.caption("Os recursos de diagnóstico disponibilizados neste ambiente têm caráter orientativo e de apoio à capacitação e à consultoria.")

elif page == "Fundador":
    st.title("Fundador")
    c1, c2 = st.columns([2.2, 1], vertical_alignment="center")
    with c1:
        st.markdown("## Bruno Bartolomeu")
        st.markdown("**Especialista em Dados, Inteligência Artificial e IA Responsável.**")
        st.write("Profissional com experiência em Ciência e Análise de Dados, Machine Learning, Analytics e Inteligência Artificial, com atuação nos setores financeiro, seguros, indústria e saúde.")
        st.write("Mestre em Inovação Tecnológica pela UFMG, professor universitário e pesquisador em IA Responsável, com foco em governança, riscos, transparência e conformidade.")
        st.write("Fundador da Veritas Nexum – IA Responsável, iniciativa dedicada à capacitação e orientação de profissionais e organizações para o uso consciente, seguro e responsável da Inteligência Artificial.")
        st.info("Bruno Bartolomeu é criador do FAC-IA Saúde, iniciativa acadêmica atualmente em processo de validação e avaliação institucional, incluindo tratativas relacionadas à propriedade intelectual no âmbito da UFMG/CTIT. A Veritas Nexum é apresentada como iniciativa independente e não representa endosso institucional ao serviço de consultoria.")
        st.markdown("[LinkedIn de Bruno Bartolomeu](https://www.linkedin.com/in/bruno-bartolomeu-39628a163/)")
    with c2:
        if FOUNDER_PHOTO.exists():
            st.image(str(FOUNDER_PHOTO), use_container_width=True, caption="Bruno Bartolomeu • Fundador")

elif page == "Contato":
    st.title("Contato")
    st.markdown("### Fale com a Veritas")
    st.write("Solicite uma conversa sobre capacitação, palestra, workshop, diagnóstico orientativo ou estruturação de práticas de IA Responsável.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**📍 Localização**")
        st.write("Belo Horizonte - MG | Atendimento Nacional e Internacional")
        st.markdown("**✉️ E-mail**")
        st.markdown("[bbartolomeu.net@gmail.com](mailto:bbartolomeu.net@gmail.com)")
        st.markdown("**🔗 LinkedIn**")
        st.markdown("[linkedin.com/in/bruno-bartolomeu-39628a163](https://www.linkedin.com/in/bruno-bartolomeu-39628a163/)")
    with c2:
        st.markdown("**Principais frentes**")
        st.write("• Capacitação e letramento em IA\n\n• Palestras e workshops\n\n• Boas práticas de IA Responsável\n\n• Diagnóstico orientativo\n\n• Governança e gestão de riscos\n\n• Apoio à estruturação de políticas e práticas internas")
        st.info("Mensagem sugerida: ‘Olá, Bruno. Gostaria de conversar sobre capacitação e boas práticas para o uso responsável de IA na minha organização.’")

    st.divider()
    st.markdown("### Solicitação de diagnóstico")
    with st.form("contact_form"):
        nome = st.text_input("Nome completo *")
        email = st.text_input("E-mail profissional *")
        telefone = st.text_input("Telefone / WhatsApp")
        cargo = st.text_input("Cargo / função")
        organizacao = st.text_input("Empresa / instituição *")
        setor = st.selectbox("Setor", ["Selecione", "Saúde", "Financeiro", "Seguros", "Indústria", "Educação", "Setor público", "Tecnologia", "Outro"])
        interesse = st.selectbox("Principal interesse *", ["Selecione", "Capacitação / letramento em IA", "Palestra / workshop", "Boas práticas de IA Responsável", "Diagnóstico orientativo", "Governança e gestão de riscos", "Políticas e práticas internas de IA"])
        mensagem = st.text_area("Desafio ou necessidade atual")
        consent = st.checkbox("Autorizo o uso destas informações exclusivamente para contato e análise inicial da solicitação.")
        sent = st.form_submit_button("Preparar contato", type="primary")
        if sent:
            if not nome or not email or not organizacao or interesse == "Selecione" or not consent:
                st.error("Preencha os campos obrigatórios e marque a autorização.")
            else:
                import urllib.parse
                subject = urllib.parse.quote("Contato Veritas Nexum - IA Responsável")
                body = urllib.parse.quote(f"Olá, Bruno.\n\nNome: {nome}\nE-mail: {email}\nTelefone/WhatsApp: {telefone}\nCargo: {cargo}\nEmpresa/Instituição: {organizacao}\nSetor: {setor}\nInteresse: {interesse}\n\nDesafio/necessidade: {mensagem}")
                st.success("Dados preparados. Clique abaixo para abrir seu aplicativo de e-mail.")
                st.markdown(f"[**Enviar solicitação por e-mail**](mailto:bbartolomeu.net@gmail.com?subject={subject}&body={body})")

st.divider()
st.markdown("<div class='vx-footer'>Veritas Nexum – IA Responsável • Capacitação • Consultoria • Governança • Tecnologia com responsabilidade</div>", unsafe_allow_html=True)

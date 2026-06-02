import streamlit as st

from src.database import init_db
from src.case_service import create_case, list_cases
from src.search import search_similar_cases
from src.runbook_generator import save_runbook, can_generate_runbook


init_db()

st.set_page_config(
    page_title="Support Knowledge Finder",
    page_icon="🛠️",
    layout="wide",
)

st.title("Support Knowledge Finder")
st.write("Buscá problemas similares, registrá casos y construí una base de conocimiento de soporte.")

st.markdown("""
<style>
.case-card {
    border: 1px solid #2d3748;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 22px;
    background: #111827;
}

.case-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 12px;
}

.case-title {
    font-size: 1.25rem;
    font-weight: 750;
    color: #f9fafb;
    margin-bottom: 6px;
}

.case-subtitle {
    font-size: 0.88rem;
    color: #9ca3af;
}

.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    margin-left: 6px;
}

.badge-open {
    background: #78350f;
    color: #fcd34d;
}

.badge-analysis {
    background: #1e3a8a;
    color: #93c5fd;
}

.badge-resolved {
    background: #064e3b;
    color: #6ee7b7;
}

.badge-verified {
    background: #14532d;
    color: #86efac;
}

.badge-discarded {
    background: #3f3f46;
    color: #d4d4d8;
}

.info-box {
    border-left: 3px solid #4b5563;
    padding-left: 12px;
    margin-bottom: 14px;
}

.info-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    color: #9ca3af;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}

.info-text {
    color: #f3f4f6;
    line-height: 1.55;
}

.tag-pill {
    display: inline-block;
    background: #1f2937;
    color: #d1d5db;
    padding: 4px 9px;
    border-radius: 999px;
    font-size: 0.8rem;
    margin-right: 6px;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

def get_status_badge(status):
    status_classes = {
        "Abierto": "badge-open",
        "En análisis": "badge-analysis",
        "Resuelto": "badge-resolved",
        "Verificado": "badge-verified",
        "Descartado": "badge-discarded",
    }

    css_class = status_classes.get(status, "badge-discarded")

    return f"<span class='badge {css_class}'>{status}</span>"


def render_tags(tags):
    if not tags:
        return "-"

    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

    if not tag_list:
        return "-"

    return " ".join([f"<span class='tag-pill'>{tag}</span>" for tag in tag_list])


menu = st.sidebar.radio(
    "Menú",
    ["Buscar problema", "Registrar caso", "Ver casos"],
)


if menu == "Buscar problema":
    st.header("Buscar problema")

    query = st.text_area(
        "Describí el problema",
        placeholder="Ejemplo: No puedo conectarme a la VPN, ya reinicié y borré caché...",
    )

    min_score = st.slider(
        "Nivel mínimo de coincidencia",
        min_value=10,
        max_value=100,
        value=20,
        step=5,
    )

    if st.button("Buscar casos similares"):
        if not query.strip():
            st.warning("Escribí una descripción del problema.")
        else:
            results = search_similar_cases(query, min_score=min_score)

            if not results:
                st.info("No se encontraron casos similares.")
            else:
                st.success(f"Se encontraron {len(results)} casos similares.")

                for result in results:
                    case = result["case"]
                    score = result["score"]

                    with st.expander(f"{case['title']} — Coincidencia: {score}%"):
                        st.write(f"**Sistema:** {case['system']}")
                        st.write(f"**Categoría:** {case.get('category') or '-'}")
                        st.write(f"**Estado:** {case['status']}")
                        st.write(f"**Descripción:** {case['description']}")
                        st.write(f"**Síntomas:** {case.get('symptoms') or '-'}")
                        st.write(f"**Qué se intentó:** {case.get('attempted_steps') or '-'}")
                        st.write(f"**Causa:** {case.get('cause') or '-'}")
                        st.write(f"**Solución:** {case.get('resolution') or '-'}")
                        st.write(f"**Escalamiento:** {case.get('escalation') or '-'}")
                        st.write(f"**Tags:** {case.get('tags') or '-'}")


elif menu == "Registrar caso":
    st.header("Registrar caso")

    with st.form("case_form"):
        title = st.text_input("Título del problema")
        system = st.text_input("Sistema afectado", placeholder="VPN, Learning Hub, Google Drive...")
        category = st.text_input("Categoría", placeholder="Access, Permissions, Content QA...")
        description = st.text_area("Descripción del problema")
        symptoms = st.text_area("Síntomas")
        attempted_steps = st.text_area("Qué se intentó")
        status = st.selectbox(
            "Estado",
            ["Abierto", "En análisis", "Resuelto", "Verificado", "Descartado"],
        )
        cause = st.text_area("Causa detectada")
        resolution = st.text_area("Solución aplicada")
        escalation = st.text_area("Cuándo escalar")
        tags = st.text_input("Tags", placeholder="vpn, acceso, gateway")
        verified = st.checkbox("Solución verificada")

        submitted = st.form_submit_button("Guardar caso")

        if submitted:
            case_data = {
                "title": title,
                "system": system,
                "category": category,
                "description": description,
                "symptoms": symptoms,
                "attempted_steps": attempted_steps,
                "status": status,
                "cause": cause,
                "resolution": resolution,
                "escalation": escalation,
                "tags": tags,
                "verified": verified,
            }

            result = create_case(case_data)

            if result["success"]:
                st.success(f"Caso creado correctamente. ID: {result['case_id']}")
            else:
                for error in result["errors"]:
                    st.error(error)


elif menu == "Ver casos":
    st.header("Casos registrados")

    cases = list_cases()

    if not cases:
        st.info("Todavía no hay casos registrados.")
    else:
        for case in cases:
            status_badge = get_status_badge(case["status"])
            verified_badge = "<span class='badge badge-verified'>Verificado</span>" if case.get("verified") else ""

            st.markdown("<div class='case-card'>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="case-header">
                    <div>
                        <div class="case-title">#{case['id']} · {case['title']}</div>
                        <div class="case-subtitle">
                            Sistema: {case['system']} · Categoría: {case.get('category') or '-'}
                        </div>
                    </div>
                    <div>
                        {status_badge}
                        {verified_badge}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            tab1, tab2, tab3 = st.tabs(["Resumen", "Diagnóstico", "Runbook"])

            with tab1:
                st.markdown(
                    f"""
                    <div class="info-box">
                        <div class="info-label">Descripción</div>
                        <div class="info-text">{case.get("description") or "-"}</div>
                    </div>

                    <div class="info-box">
                        <div class="info-label">Síntomas</div>
                        <div class="info-text">{case.get("symptoms") or "-"}</div>
                    </div>

                    <div class="info-box">
                        <div class="info-label">Tags</div>
                        <div>{render_tags(case.get("tags"))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with tab2:
                col1, col2 = st.columns(2)

                with col1:
                    st.caption("QUÉ SE INTENTÓ")
                    st.write(case.get("attempted_steps") or "-")

                    st.caption("CAUSA DETECTADA")
                    st.write(case.get("cause") or "-")

                with col2:
                    st.caption("SOLUCIÓN APLICADA")
                    st.write(case.get("resolution") or "-")

                    st.caption("CUÁNDO ESCALAR")
                    st.write(case.get("escalation") or "-")

            with tab3:
                if can_generate_runbook(case):
                    if st.button(f"Generar runbook #{case['id']}", key=f"runbook_{case['id']}"):
                        result = save_runbook(case)

                        if result["success"]:
                            st.success(f"Runbook generado: {result['path']}")

                            st.subheader("Vista previa del runbook")
                            st.markdown(result["content"])

                            st.download_button(
                                label="Descargar runbook Markdown",
                                data=result["content"],
                                file_name=result["filename"],
                                mime="text/markdown",
                                key=f"download_{case['id']}"
                            )
                        else:
                            st.error(result["error"])
                else:
                    st.info("Este caso todavía no tiene suficiente información para generar un runbook.")

            st.markdown("</div>", unsafe_allow_html=True)
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
            with st.expander(f"{case['id']} - {case['title']}"):
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
                st.write(f"**Verificado:** {'Sí' if case.get('verified') else 'No'}")
                if can_generate_runbook(case):
                    if st.button(f"Generar runbook #{case['id']}"):
                        result = save_runbook(case)

                        if result["success"]:
                            st.success(f"Runbook generado: {result['path']}")
                        else:
                            st.error(result["error"])
                else:
                    st.info("Este caso todavía no tiene suficiente información para generar un runbook.")
from pathlib import Path
import re


OUTPUT_DIR = Path("output/runbooks")


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text


def can_generate_runbook(case):
    return (
        case.get("status") in ["Resuelto", "Verificado"]
        and case.get("cause")
        and case.get("resolution")
    )


def generate_runbook_content(case):
    verified_text = "Sí" if case.get("verified") else "No"

    return f"""# Runbook: {case.get("title")}

## Sistema afectado
{case.get("system") or "-"}

## Categoría
{case.get("category") or "-"}

## Estado
{case.get("status") or "-"}

## Solución verificada
{verified_text}

## Descripción del problema
{case.get("description") or "-"}

## Síntomas
{case.get("symptoms") or "-"}

## Acciones que no funcionaron o ya se intentaron
{case.get("attempted_steps") or "-"}

## Causa detectada
{case.get("cause") or "-"}

## Solución aplicada
{case.get("resolution") or "-"}

## Cuándo escalar
{case.get("escalation") or "-"}

## Tags
{case.get("tags") or "-"}

---

Generado automáticamente por Support Knowledge Finder.
"""


def save_runbook(case):
    if not can_generate_runbook(case):
        return {
            "success": False,
            "error": "Solo se puede generar runbook para casos resueltos/verificados con causa y solución.",
            "path": None,
        }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{slugify(case.get('title'))}.md"
    file_path = OUTPUT_DIR / filename

    content = generate_runbook_content(case)

    file_path.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "error": None,
        "path": str(file_path),
    }
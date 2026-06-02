REQUIRED_FIELDS = [
    "title",
    "system",
    "description",
    "status",
]


VALID_STATUSES = [
    "Abierto",
    "En análisis",
    "Resuelto",
    "Verificado",
    "Descartado",
]


def validate_case(case_data):
    errors = []

    for field in REQUIRED_FIELDS:
        value = case_data.get(field)

        if not value or not str(value).strip():
            errors.append(f"El campo '{field}' es obligatorio.")

    status = case_data.get("status")

    if status and status not in VALID_STATUSES:
        errors.append(
            f"El estado '{status}' no es válido. Estados permitidos: {', '.join(VALID_STATUSES)}"
        )

    if case_data.get("status") in ["Resuelto", "Verificado"]:
        if not case_data.get("resolution"):
            errors.append("Un caso resuelto debe tener una solución cargada.")

    return errors
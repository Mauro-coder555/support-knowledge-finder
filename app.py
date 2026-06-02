from src.database import init_db
from src.case_service import create_case, list_cases


init_db()

case = {
    "title": "VPN no conecta por gateway incorrecto",
    "system": "VPN",
    "category": "Access",
    "description": "El usuario no puede conectarse a la VPN aunque reinició el entorno y borró caché.",
    "symptoms": "La VPN rechaza la conexión. Reiniciar no resuelve.",
    "attempted_steps": "Borrar caché. Reiniciar entorno. Verificar contraseña.",
    "status": "Resuelto",
    "cause": "La puerta de enlace configurada no correspondía al entorno asignado.",
    "resolution": "Validar entorno asignado, cambiar gateway y probar conexión nuevamente.",
    "escalation": "Escalar a Infraestructura si el gateway es correcto pero sigue fallando.",
    "tags": "vpn, acceso, gateway, soporte",
    "verified": True,
}

result = create_case(case)

if result["success"]:
    print(f"Caso creado con ID: {result['case_id']}")
else:
    print("Errores:")
    for error in result["errors"]:
        print(f"- {error}")

print("\nCasos registrados:")
for item in list_cases():
    print(f"{item['id']} - {item['title']} - {item['status']}")
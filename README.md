# Support Knowledge Finder

Support Knowledge Finder es una aplicación local para registrar problemas de soporte, buscar casos similares y generar runbooks en Markdown a partir de soluciones verificadas.

El proyecto nace de una situación bastante común en equipos de soporte: muchas veces los mismos problemas aparecen una y otra vez, pero la solución queda perdida en un chat, en la memoria de una persona o en un ticket viejo difícil de encontrar. La idea de esta herramienta es simple: guardar esos casos en una base de conocimiento fácil de consultar y convertir las soluciones útiles en documentación reutilizable.

## Qué permite hacer

La aplicación permite:

- registrar casos de soporte, incluso cuando todavía no tienen solución;
- buscar problemas similares usando texto libre;
- revisar qué se intentó antes;
- documentar la causa y la solución aplicada;
- marcar soluciones como verificadas;
- generar runbooks en formato Markdown;
- descargar esos runbooks para compartirlos o versionarlos.

Todo funciona de forma local. No requiere servicios pagos, APIs externas ni cuentas adicionales.

## Para qué sirve

Este proyecto está pensado como una herramienta chica pero práctica para equipos de soporte, operaciones o mesa de ayuda.

Puede servir para casos como:

- problemas de acceso a una plataforma;
- errores de VPN;
- permisos incorrectos;
- usuarios asignados a grupos equivocados;
- links rotos en materiales;
- configuraciones mal realizadas;
- problemas que parecen repetirse pero no están bien documentados.

La aplicación no intenta reemplazar un sistema de tickets. Su objetivo es complementar el trabajo diario ayudando a encontrar antecedentes, evitar repetir pruebas inútiles y documentar soluciones que ya funcionaron.

## Problema que intenta resolver

En soporte técnico muchas veces se empieza desde cero con cada incidente. Una persona reporta un problema, alguien prueba soluciones genéricas, se escala el caso, se resuelve, y después esa información no queda ordenada.

Con el tiempo aparecen situaciones como:

- se recomienda borrar caché aunque el problema real era de permisos;
- se reinicia un entorno aunque el error era de configuración;
- se vuelve a investigar algo que ya había ocurrido;
- no se sabe qué soluciones no funcionaron;
- la documentación se genera tarde o directamente no se genera.

Support Knowledge Finder busca ordenar ese flujo.

Primero se registra el caso. Después se lo puede buscar. Cuando se encuentra una solución, se completa la causa, los pasos aplicados y el criterio de escalamiento. Finalmente, si el caso está resuelto, se puede generar un runbook.

## Flujo de uso

El flujo esperado es:

1. Una persona tiene un problema.
2. Lo busca en la aplicación con lenguaje natural.
3. Si encuentra un caso parecido, revisa qué pasó y cómo se resolvió.
4. Si no encuentra nada útil, registra un nuevo caso.
5. El caso queda abierto o en análisis.
6. Cuando se resuelve, se completa la causa y la solución.
7. Si la solución es confiable, se marca como verificada.
8. Se genera un runbook en Markdown.

## Tecnologías usadas

El proyecto usa herramientas simples y gratuitas:

- Python
- Streamlit
- SQLite
- RapidFuzz
- Markdown

No usa inteligencia artificial ni servicios pagos. La búsqueda de similitud se hace con RapidFuzz, comparando el texto ingresado por el usuario contra los casos guardados.

## Estructura del proyecto

```text
support-knowledge-finder/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── support_cases.db
├── output/
│   └── runbooks/
├── src/
│   ├── database.py
│   ├── search.py
│   ├── case_service.py
│   ├── runbook_generator.py
│   └── validators.py
├── tests/
└── docs/
```

## Qué hace cada parte

### app.py

Contiene la interfaz principal hecha con Streamlit.

Desde ahí se puede:

- buscar problemas;
- registrar casos;
- ver casos guardados;
- generar runbooks;
- descargar la documentación generada.

### src/database.py

Maneja la conexión con SQLite.

Se encarga de:

- crear la base de datos;
- crear la tabla de casos;
- insertar registros;
- listar casos;
- obtener casos por ID;
- actualizar o eliminar información.

### src/case_service.py

Contiene la lógica principal para trabajar con casos.

Actúa como una capa intermedia entre la app y la base de datos. Esto evita que la interfaz tenga que manejar directamente todas las operaciones.

### src/search.py

Contiene el buscador de casos similares.

Construye un texto de búsqueda usando campos como título, descripción, síntomas, causa, solución y tags. Luego compara ese texto contra la consulta del usuario usando RapidFuzz.

### src/validators.py

Valida que los casos tengan los datos mínimos necesarios.

Por ejemplo, evita guardar casos sin título, sin sistema afectado o sin descripción.

También valida que un caso marcado como resuelto tenga una solución cargada.

### src/runbook_generator.py

Genera documentación en Markdown a partir de un caso resuelto o verificado.

El archivo se guarda en:

```text
output/runbooks/
```

La app también muestra una vista previa y permite descargar el archivo.

## Campos de un caso

Cada caso puede incluir:

- título;
- sistema afectado;
- categoría;
- descripción;
- síntomas;
- acciones que ya se intentaron;
- estado;
- causa detectada;
- solución aplicada;
- criterio de escalamiento;
- tags;
- si la solución fue verificada o no.

Los estados disponibles son:

- Abierto
- En análisis
- Resuelto
- Verificado
- Descartado

## Ejemplo de caso

Un caso típico podría ser:

```text
Título: VPN no conecta por gateway incorrecto
Sistema: VPN
Categoría: Access
Descripción: El usuario no puede conectarse a la VPN aunque reinició el entorno y borró caché.
Síntomas: La VPN rechaza la conexión.
Qué se intentó: Borrar caché, reiniciar entorno, verificar contraseña.
Estado: Resuelto
Causa: La puerta de enlace configurada no correspondía al entorno asignado.
Solución: Validar entorno asignado, cambiar gateway y probar conexión nuevamente.
Escalamiento: Escalar a Infraestructura si el gateway es correcto pero sigue fallando.
Tags: vpn, acceso, gateway, soporte
```

A partir de ese caso, la aplicación puede generar un runbook como este:

```markdown
# Runbook: VPN no conecta por gateway incorrecto

## Sistema afectado
VPN

## Categoría
Access

## Estado
Resuelto

## Descripción del problema
El usuario no puede conectarse a la VPN aunque reinició el entorno y borró caché.

## Síntomas
La VPN rechaza la conexión.

## Acciones que no funcionaron o ya se intentaron
Borrar caché, reiniciar entorno, verificar contraseña.

## Causa detectada
La puerta de enlace configurada no correspondía al entorno asignado.

## Solución aplicada
Validar entorno asignado, cambiar gateway y probar conexión nuevamente.

## Cuándo escalar
Escalar a Infraestructura si el gateway es correcto pero sigue fallando.
```

## Cómo instalar el proyecto

Clonar el repositorio:

```bash
git clone https://github.com/usuario/support-knowledge-finder.git
cd support-knowledge-finder
```

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Instalar dependencias:

```bash
python -m pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python -m streamlit run app.py
```

Luego abrir el navegador en:

```text
http://localhost:8501
```

## Cómo usar la aplicación

### Buscar problema

En la sección “Buscar problema” se puede escribir una descripción libre, por ejemplo:

```text
No puedo conectarme a la VPN, ya reinicié y borré caché.
```

La aplicación devuelve los casos más parecidos, junto con su estado, sistema afectado, causa y solución si están disponibles.

### Registrar caso

En la sección “Registrar caso” se carga un nuevo problema.

No hace falta conocer la solución desde el principio. Un caso puede quedar como “Abierto” o “En análisis”.

Cuando se encuentra la causa, se puede completar la solución y marcarlo como resuelto.

### Ver casos

En la sección “Ver casos” se muestran los casos registrados con una vista ordenada por pestañas:

- Resumen
- Diagnóstico
- Runbook

Desde ahí se puede generar un runbook si el caso tiene estado “Resuelto” o “Verificado” y cuenta con causa y solución.

## Por qué este proyecto es útil para soporte IT

El valor del proyecto no está solo en el código. Está en el enfoque operativo.

Muestra una forma simple de transformar problemas repetidos en conocimiento reutilizable. También ayuda a separar lo que se intentó, lo que realmente funcionó y cuándo corresponde escalar.

En un entorno real, esto puede reducir tiempo de diagnóstico, evitar pruebas innecesarias y mejorar la documentación interna.

## Posibles mejoras futuras

Algunas mejoras posibles:

- editar casos desde la interfaz;
- borrar casos desde la interfaz;
- importar casos desde CSV;
- exportar toda la base de conocimiento;
- agregar métricas de casos por sistema o categoría;
- detectar duplicados automáticamente;
- agregar filtros por estado, sistema o tags;
- generar un índice automático de runbooks;
- crear una versión CLI;
- agregar tests automatizados;
- preparar una demo con datos iniciales.

## Estado actual

La versión actual permite:

- registrar casos;
- buscar problemas similares;
- visualizar casos;
- generar runbooks;
- descargar runbooks en Markdown.

Es una primera versión funcional pensada para demostrar una idea concreta: una base de conocimiento simple, local y gratuita para soporte técnico y automatización operativa.

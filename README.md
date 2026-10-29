# RQ Envíos · Cotizador de tarifas — Código de partida

**Caso ficticio con fines didácticos. Cualquier semejanza con empresas o personas reales es coincidencia.**
Curso Calidad y Pruebas de Software (ISOF1401A) · UPN · Unidad III · Semana 11 · Clase 01.

## Propósito
Aplicación mínima (API Flask) del negocio ficticio *Encomiendas Ruta Quinual S.A.C.* (Huancayo, Junín).
En el laboratorio construirás un pipeline de integración continua que ejecuta sus pruebas en cada cambio.

## Requisitos del equipo
- Python 3.12 · Git 2.40 o superior · cuenta de GitHub (repositorio propio del equipo)
- Docker Desktop o Docker Engine (paso 4; opcional si el laboratorio no lo tiene instalado)
- Solo datos sintéticos. Ley N.º 29733: no uses datos personales reales.

## Instalación y ejecución local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   ·   Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest                                  # con pytest
python -m unittest discover -s tests -t .   # alternativa sin conexión (solo biblioteca estándar)
```

## Resultado esperado al iniciar
18 pruebas: **15 aprobadas y 3 fallidas**. Las fallas son intencionales: el pipeline debe detectarlas.
Tu tarea es completar los `TODO` de `.github/workflows/ci.yml` y del `Dockerfile`, ver el pipeline en rojo,
corregir los defectos del cotizador y llegar a un pipeline en verde con evidencias publicadas.

## Uso de IA
Puedes pedir a una IA que explique un error del pipeline, pero valida la respuesta y decláralo en tu evidencia.

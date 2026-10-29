# Imagen para ejecutar las pruebas en un entorno reproducible.
# Python 3.12 en variante "slim" (Debian) para reducir el tamaño.
FROM python:3.12-slim

# Evita archivos .pyc y fuerza salida sin búfer (logs inmediatos en el pipeline).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero dependencias (aprovecha la caché de capas de Docker).
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# TODO 4: copia las carpetas app y tests, y el archivo pytest.ini.

# Usuario sin privilegios (buena práctica de seguridad).
RUN useradd --create-home probador && mkdir -p /app/reportes && chown -R probador /app
USER probador

# Comando por defecto: ejecutar la suite y generar evidencias.
CMD ["pytest", "--junitxml=reportes/junit.xml", "--cov=app", "--cov-report=term-missing", "--cov-report=xml:reportes/cobertura.xml"]

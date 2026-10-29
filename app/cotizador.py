"""Cotizador de tarifas de RQ Envíos.

Encomiendas Ruta Quinual S.A.C. es un negocio FICTICIO con fines didácticos.
Cualquier semejanza con empresas reales es coincidencia.

Reglas de negocio (ficticias):
- Tramos por peso: hasta 1 kg; más de 1 kg hasta 5 kg; más de 5 kg hasta 20 kg.
  Se aceptan envíos desde 0,1 kg hasta 20 kg (ambos inclusive).
- Tarifa = base del tramo x factor de zona del destino.
- Servicio "express": recargo de 35 %.
- Envío frágil: recargo fijo de S/ 4,00.
- Destinos de selva central: recargo de acceso de S/ 6,00.
"""

from decimal import Decimal, ROUND_HALF_UP

PESO_MINIMO_KG = Decimal("0.1")
PESO_MAXIMO_KG = Decimal("20")

# Tarifa base por tramo de peso (soles).
TARIFA_HASTA_1_KG = Decimal("12.00")
TARIFA_HASTA_5_KG = Decimal("18.50")
TARIFA_HASTA_20_KG = Decimal("29.00")

FACTOR_ZONA = {
    "huancayo": Decimal("1.00"),
    "jauja": Decimal("1.10"),
    "concepcion": Decimal("1.10"),
    "tarma": Decimal("1.25"),
    "la oroya": Decimal("1.25"),
    "huancavelica": Decimal("1.40"),
    "satipo": Decimal("1.60"),
    "la merced": Decimal("1.50"),
    "lima": Decimal("1.45"),
}

DESTINOS_SELVA_CENTRAL = {"satipo", "la merced"}
RECARGO_EXPRESS = Decimal("0.35")
RECARGO_FRAGIL = Decimal("4.00")
RECARGO_SELVA = Decimal("6.00")


class CotizacionInvalida(ValueError):
    """Error de validación de los datos de una cotización."""


def normalizar_destino(destino):
    """Devuelve el destino en minúsculas, sin espacios extremos ni tildes comunes."""
    if not isinstance(destino, str) or not destino.strip():
        raise CotizacionInvalida("El destino es obligatorio.")
    texto = destino.strip().lower()
    reemplazos = str.maketrans("áéíóú", "aeiou")
    return texto.translate(reemplazos)


def tarifa_base(peso_kg):
    """Devuelve la tarifa base según el tramo de peso."""
    peso = Decimal(str(peso_kg))
    if peso < PESO_MINIMO_KG or peso > PESO_MAXIMO_KG:
        raise CotizacionInvalida("El peso debe estar entre 0.1 kg y 20 kg.")
    if peso <= Decimal("1"):
        return TARIFA_HASTA_1_KG
    if peso < Decimal("5"):
        return TARIFA_HASTA_5_KG
    return TARIFA_HASTA_20_KG


def cotizar(peso_kg, destino, servicio="estandar", fragil=False):
    """Calcula la tarifa final en soles, redondeada a dos decimales."""
    zona = normalizar_destino(destino)
    if zona not in FACTOR_ZONA:
        raise CotizacionInvalida(f"Destino sin cobertura: {destino}")
    if servicio not in ("estandar", "express"):
        raise CotizacionInvalida("El servicio debe ser 'estandar' o 'express'.")

    total = tarifa_base(peso_kg) * FACTOR_ZONA[zona]
    if servicio == "express":
        total = total * (Decimal("1") + RECARGO_EXPRESS)
    if fragil:
        total += RECARGO_FRAGIL
    if destino in DESTINOS_SELVA_CENTRAL:
        total += RECARGO_SELVA
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

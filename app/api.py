"""API HTTP mínima del cotizador (Flask). Solo datos sintéticos."""

from flask import Flask, jsonify, request

from app.cotizador import CotizacionInvalida, cotizar


def crear_app():
    """Crea la aplicación Flask (patrón fábrica, facilita las pruebas)."""
    aplicacion = Flask(__name__)

    @aplicacion.get("/salud")
    def salud():
        return jsonify(estado="ok", servicio="rq-envios-cotizador")

    @aplicacion.post("/api/cotizar")
    def api_cotizar():
        datos = request.get_json(silent=True) or {}
        try:
            monto = cotizar(
                peso_kg=datos.get("peso_kg"),
                destino=datos.get("destino"),
                servicio=datos.get("servicio", "estandar"),
                fragil=bool(datos.get("fragil", False)),
            )
        except (CotizacionInvalida, TypeError, ArithmeticError) as error:
            return jsonify(error=str(error) or "Datos inválidos"), 400
        return jsonify(moneda="PEN", monto=str(monto)), 200

    return aplicacion


if __name__ == "__main__":
    crear_app().run(host="0.0.0.0", port=5000)

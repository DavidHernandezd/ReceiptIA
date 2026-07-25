import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_health_responde_correctamente():
    """Comprueba que el backend esté disponible."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "servicio": "ReceiptIA Backend",
    }


def test_inicio_muestra_informacion_del_proyecto():
    """Comprueba la información general de ReceiptIA."""

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["aplicacion"] == "ReceiptIA"
    assert response.json()["version"] == "1.0.0"


def test_texto_ocr_vacio_es_invalido():
    """Un OCR vacío no debe considerarse válido."""

    assert main.texto_ocr_es_valido("") is False


def test_texto_ocr_corto_es_invalido():
    """Un texto demasiado corto no contiene información suficiente."""

    assert main.texto_ocr_es_valido("Factura") is False


def test_texto_ocr_suficiente_es_valido():
    """Un texto suficientemente largo puede enviarse al análisis."""

    texto = "Factura consumidor final con un total de veinte dólares."

    assert main.texto_ocr_es_valido(texto) is True


def test_normalizar_factura_agrega_campos_faltantes():
    """La normalización debe agregar la estructura básica esperada."""

    factura = {
        "comercio": "Tienda de prueba",
        "total": 25.50,
    }

    resultado = main.normalizar_factura(factura)

    assert resultado["comercio"] == "Tienda de prueba"
    assert resultado["total"] == 25.50
    assert resultado["items"] == []
    assert resultado["anomalias"] == []
    assert resultado["tiene_anomalias"] is False
    assert resultado["iva"] == 0.00


def test_limpiar_json_respuesta_extrae_objeto():
    """Comprueba que se pueda extraer un JSON desde una respuesta extensa."""

    texto = 'Resultado del análisis: {"comercio": "Prueba", "total": 10.0} Fin.'

    resultado = main.limpiar_json_respuesta(texto)

    assert resultado["comercio"] == "Prueba"
    assert resultado["total"] == 10.0


def test_procesar_lote_sin_archivos_es_rechazado():
    """La API debe rechazar una solicitud sin archivos."""

    response = client.post("/procesar-lote")

    assert response.status_code == 422


def test_gemini_requiere_variable_de_entorno(monkeypatch):
    """Gemini no debe iniciar cuando falta la clave."""

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        main.obtener_cliente_gemini()
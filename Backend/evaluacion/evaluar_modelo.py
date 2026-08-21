import csv
import json
import sys
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import main


EVALUACION_DIR = Path(__file__).resolve().parent
CASOS_PATH = EVALUACION_DIR / "casos_evaluacion.json"
RESULTADOS_DIR = EVALUACION_DIR / "resultados"

CAMPOS_EVALUADOS = [
    "comercio",
    "fecha",
    "total",
    "es_exenta",
    "tiene_anomalias",
]


def normalizar_texto(valor):
    if valor is None:
        return ""

    texto = str(valor).strip().lower()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


def valores_coinciden(campo, obtenido, esperado):

    if campo == "total":
        try:
            return abs(float(obtenido) - float(esperado)) <= 0.02
        except (TypeError, ValueError):
            return False

    if campo in ["es_exenta", "tiene_anomalias"]:
        return obtenido == esperado

    return normalizar_texto(obtenido) == normalizar_texto(esperado)


def ejecutar_evaluacion():

    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

    with open(CASOS_PATH, "r", encoding="utf-8") as archivo:
        casos = json.load(archivo)

    resultados = []

    aciertos_por_campo = {
        campo: 0
        for campo in CAMPOS_EVALUADOS
    }

    casos_completados = 0
    errores_ejecucion = 0

    for caso in casos:

        print(f'\nEvaluando {caso["id"]}: {caso["descripcion"]}')

        fila = {
            "caso": caso["id"],
            "descripcion": caso["descripcion"],
            "estado": "OK",
            "precision_caso": 0,
            "error": "",
        }

        try:
            prompt = main.crear_prompt_factura_individual(
                caso["texto_ocr"]
            )

            respuesta = main.generar_con_gemini(prompt)

            obtenido = main.limpiar_json_respuesta(
                respuesta.text
            )

            obtenido = main.normalizar_factura(
                obtenido
            )

            esperado = caso["esperado"]

            aciertos_caso = 0

            for campo in CAMPOS_EVALUADOS:

                coincide = valores_coinciden(
                    campo,
                    obtenido.get(campo),
                    esperado.get(campo),
                )

                fila[campo] = "OK" if coincide else "ERROR"

                fila[f"obtenido_{campo}"] = obtenido.get(campo)
                fila[f"esperado_{campo}"] = esperado.get(campo)

                if coincide:
                    aciertos_caso += 1
                    aciertos_por_campo[campo] += 1

            precision = (
                aciertos_caso
                / len(CAMPOS_EVALUADOS)
                * 100
            )

            fila["precision_caso"] = round(
                precision,
                2
            )

            casos_completados += 1

            print(
                f'Precisión del caso: '
                f'{fila["precision_caso"]}%'
            )

        except Exception as error:

            errores_ejecucion += 1

            fila["estado"] = "ERROR_EJECUCION"
            fila["error"] = str(error)

            print(
                f"Error evaluando el caso: {error}"
            )

        resultados.append(fila)

    # ==============================
    # PRECISIÓN GENERAL
    # ==============================

    if casos_completados > 0:

        total_aciertos = sum(
            aciertos_por_campo.values()
        )

        total_comparaciones = (
            casos_completados
            * len(CAMPOS_EVALUADOS)
        )

        precision_general = round(
            total_aciertos
            / total_comparaciones
            * 100,
            2,
        )

    else:
        precision_general = 0.0

    precision_por_campo = {}

    for campo in CAMPOS_EVALUADOS:

        if casos_completados > 0:
            precision_por_campo[campo] = round(
                aciertos_por_campo[campo]
                / casos_completados
                * 100,
                2,
            )
        else:
            precision_por_campo[campo] = 0.0

    resumen = {
        "modelo": main.AI_MODEL,
        "prompt_version": main.PROMPT_VERSION,
        "casos_totales": len(casos),
        "casos_completados": casos_completados,
        "errores_ejecucion": errores_ejecucion,
        "precision_general": precision_general,
        "precision_por_campo": precision_por_campo,
    }

    # ==============================
    # GUARDAR CSV
    # ==============================

    csv_path = (
        RESULTADOS_DIR
        / "evaluacion_modelo.csv"
    )

    if resultados:

        campos_csv = list(
            resultados[0].keys()
        )

        for fila in resultados:
            for campo in fila.keys():
                if campo not in campos_csv:
                    campos_csv.append(campo)

        with open(
            csv_path,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as archivo:

            writer = csv.DictWriter(
                archivo,
                fieldnames=campos_csv,
            )

            writer.writeheader()
            writer.writerows(resultados)

    # ==============================
    # GUARDAR RESUMEN
    # ==============================

    resumen_path = (
        RESULTADOS_DIR
        / "resumen_evaluacion.json"
    )

    with open(
        resumen_path,
        "w",
        encoding="utf-8",
    ) as archivo:

        json.dump(
            resumen,
            archivo,
            indent=4,
            ensure_ascii=False,
        )

    print("\n==============================")
    print("EVALUACIÓN FINALIZADA")
    print("==============================")

    print(
        f"Modelo: {main.AI_MODEL}"
    )

    print(
        f"Prompt: {main.PROMPT_VERSION}"
    )

    print(
        f"Casos completados: "
        f"{casos_completados}/{len(casos)}"
    )

    print(
        f"Precisión general: "
        f"{precision_general}%"
    )

    print("\nPrecisión por campo:")

    for campo, precision in precision_por_campo.items():
        print(
            f"- {campo}: {precision}%"
        )

    print(
        f"\nReporte CSV: {csv_path}"
    )

    print(
        f"Resumen JSON: {resumen_path}"
    )


if __name__ == "__main__":
    ejecutar_evaluacion()
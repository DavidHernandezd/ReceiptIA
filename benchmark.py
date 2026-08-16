import csv
import time
import uuid
import urllib.request
import urllib.error
from pathlib import Path
from statistics import median


# =========================
# CONFIGURACIÓN
# =========================

URL = "http://127.0.0.1:8000/procesar"
IMAGE_PATH = Path("factura_prueba.jpg")

TOTAL_REQUESTS = 20
TIMEOUT_SECONDS = 180


# =========================
# MULTIPART FORM-DATA
# =========================

def build_multipart(file_path):
    boundary = "----ReceiptIABenchmark" + uuid.uuid4().hex

    file_data = file_path.read_bytes()
    filename = file_path.name

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: image/jpeg\r\n"
        "\r\n"
    ).encode("utf-8")

    body += file_data

    body += (
        f"\r\n--{boundary}--\r\n"
    ).encode("utf-8")

    content_type = f"multipart/form-data; boundary={boundary}"

    return body, content_type


# =========================
# PERCENTILES
# =========================

def percentile(values, p):
    if not values:
        return None

    values = sorted(values)

    position = (len(values) - 1) * (p / 100)

    lower = int(position)
    upper = min(lower + 1, len(values) - 1)

    if lower == upper:
        return values[lower]

    weight = position - lower

    return (
        values[lower]
        + (values[upper] - values[lower]) * weight
    )


# =========================
# VALIDACIONES
# =========================

if not IMAGE_PATH.exists():
    print(f"ERROR: No se encontró la imagen: {IMAGE_PATH}")
    raise SystemExit(1)


print("=" * 70)
print("BENCHMARK RECEIPTIA - SEMANA 5")
print("=" * 70)
print(f"Endpoint: {URL}")
print(f"Imagen:   {IMAGE_PATH}")
print(f"Solicitudes: {TOTAL_REQUESTS}")
print("=" * 70)

results = []

for i in range(1, TOTAL_REQUESTS + 1):

    print(f"\nSolicitud {i}/{TOTAL_REQUESTS}...")

    try:
        body, content_type = build_multipart(IMAGE_PATH)

        request = urllib.request.Request(
            URL,
            data=body,
            method="POST",
            headers={
                "Content-Type": content_type,
                "Accept": "application/json",
            },
        )

        start = time.perf_counter()

        with urllib.request.urlopen(
            request,
            timeout=TIMEOUT_SECONDS
        ) as response:

            response.read()

            status = response.status
            request_id = response.headers.get("X-Request-ID")

        end = time.perf_counter()

        duration_ms = (end - start) * 1000

        print(
            f"   Estado: {status} | "
            f"Duración: {duration_ms:.2f} ms | "
            f"Request ID: {request_id}"
        )

        results.append({
            "request_number": i,
            "status": status,
            "duration_ms": duration_ms,
            "request_id": request_id,
            "error": "",
        })

    except urllib.error.HTTPError as error:

        end = time.perf_counter()

        duration_ms = (end - start) * 1000

        request_id = error.headers.get("X-Request-ID")

        print(
            f"   ERROR HTTP {error.code} | "
            f"Duración: {duration_ms:.2f} ms | "
            f"Request ID: {request_id}"
        )

        results.append({
            "request_number": i,
            "status": error.code,
            "duration_ms": duration_ms,
            "request_id": request_id,
            "error": f"HTTP_{error.code}",
        })

    except Exception as error:

        end = time.perf_counter()

        duration_ms = (end - start) * 1000

        print(
            f"   ERROR: {error} | "
            f"Duración: {duration_ms:.2f} ms"
        )

        results.append({
            "request_number": i,
            "status": 0,
            "duration_ms": duration_ms,
            "request_id": "",
            "error": str(error),
        })


# =========================
# MÉTRICAS
# =========================

durations = [
    r["duration_ms"]
    for r in results
]

successful = [
    r for r in results
    if 200 <= r["status"] < 300
]

errors = [
    r for r in results
    if not (200 <= r["status"] < 300)
]

p50 = percentile(durations, 50)
p95 = percentile(durations, 95)
maximum = max(durations)

error_rate = (
    len(errors) / len(results) * 100
    if results
    else 0
)


# =========================
# RESULTADOS
# =========================

print("\n")
print("=" * 70)
print("RESULTADOS DEL BENCHMARK")
print("=" * 70)

print(f"Solicitudes totales : {len(results)}")
print(f"Solicitudes exitosas: {len(successful)}")
print(f"Errores             : {len(errors)}")
print(f"Tasa de error       : {error_rate:.2f}%")
print(f"p50                 : {p50:.2f} ms")
print(f"p95                 : {p95:.2f} ms")
print(f"Máximo              : {maximum:.2f} ms")

print("=" * 70)


# =========================
# GUARDAR CSV
# =========================

csv_path = Path("benchmark_resultados.csv")

with csv_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "request_number",
            "status",
            "duration_ms",
            "request_id",
            "error",
        ],
    )

    writer.writeheader()
    writer.writerows(results)


# =========================
# RESUMEN TXT
# =========================

summary_path = Path("benchmark_resumen.txt")

with summary_path.open(
    "w",
    encoding="utf-8"
) as file:

    file.write("BENCHMARK RECEIPTIA - SEMANA 5\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Endpoint: {URL}\n")
    file.write(f"Solicitudes: {len(results)}\n")
    file.write(f"Exitosas: {len(successful)}\n")
    file.write(f"Errores: {len(errors)}\n")
    file.write(f"Tasa de error: {error_rate:.2f}%\n")
    file.write(f"p50: {p50:.2f} ms\n")
    file.write(f"p95: {p95:.2f} ms\n")
    file.write(f"Máximo: {maximum:.2f} ms\n")


print("\nArchivos generados:")
print(f"  - {csv_path}")
print(f"  - {summary_path}")
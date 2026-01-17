import csv
from datetime import datetime
from pathlib import Path

# ========= RUTAS =========
INPUT_TXT  = Path(r"..\Datos del interrogador\Primer sensor\Caracterizacion temp 191225.txt")
OUTPUT_CSV = Path(r"..\Datos del interrogador\Primer sensor\fbg_lambda_avg_1s_hms.csv")

TIME_FORMAT = "%d/%m/%Y %H:%M:%S.%f"
# =========================

def main():

    current_second = None
    sum_lambda = 0.0
    count = 0

    with INPUT_TXT.open("r", encoding="utf-8", errors="ignore") as fin, \
         OUTPUT_CSV.open("w", newline="", encoding="utf-8") as fout:

        writer = csv.writer(fout)
        writer.writerow(["time_hms", "lambda_bragg_nm"])

        fin.readline()  # saltar encabezado

        for line in fin:
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            # Timestamp completo
            ts_str = f"{parts[0]} {parts[1]}"
            ts = datetime.strptime(ts_str, TIME_FORMAT)

            # Columna 3 → longitud de onda (nm)
            lambda_bragg = float(parts[3])

            # Redondear al segundo
            ts_sec = ts.replace(microsecond=0)

            if current_second is None:
                current_second = ts_sec

            # Cambio de segundo → guardar promedio
            if ts_sec != current_second:
                writer.writerow([
                    current_second.strftime("%H:%M:%S"),
                    sum_lambda / count
                ])
                current_second = ts_sec
                sum_lambda = 0.0
                count = 0

            sum_lambda += lambda_bragg
            count += 1

        # Último segundo
        if count > 0:
            writer.writerow([
                current_second.strftime("%H:%M:%S"),
                sum_lambda / count
            ])

    print("CSV generado correctamente:")
    print(OUTPUT_CSV.resolve())


if __name__ == "__main__":
    main()

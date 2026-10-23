
from pathlib import Path
from datetime import datetime, timedelta
import random
import pandas as pd

# =========================
# 設定値
# =========================

YEAR = 2026

PRODUCTS = {
    "P001": {"length": 12.3, "width": 4.25, "height": 2.11, "weight": 15.2},
    "P002": {"length": 13.8, "width": 4.80, "height": 2.30, "weight": 17.5},
    "P003": {"length": 15.1, "width": 5.32, "height": 2.84, "weight": 21.3},
    "P004": {"length": 16.7, "width": 5.95, "height": 2.95, "weight": 24.8},
    "P005": {"length": 18.4, "width": 6.53, "height": 3.11, "weight": 28.2},
}

LINES = ["L01", "L02", "L03"]
OPERATORS = ["SUZUKI", "YAMADA", "SATO", "SASAKI"]

BASE_PATH = Path("data") / str(YEAR)

BASE_PATH.mkdir(parents=True, exist_ok=True)


def create_record(
    timestamp,
    line,
    product,
    lot_no,
    operator,
    ng_rate
):

    spec = PRODUCTS[product]

    result = "NG" if random.random() < ng_rate else "OK"

    length = random.gauss(spec["length"], 0.05)
    width = random.gauss(spec["width"], 0.02)
    height = random.gauss(spec["height"], 0.01)
    weight = random.gauss(spec["weight"], 0.10)

    if result == "NG":
        length += random.choice([-1.5, 1.5])
        width += random.choice([-0.3, 0.3])

    return {
        "timestamp": timestamp,
        "line_no": line,
        "product_no": product,
        "lot_no": lot_no,
        "operator": operator,
        "result": result,
        "length": round(length, 2),
        "width": round(width, 2),
        "height": round(height, 2),
        "weight": round(weight, 2),
        "temperature": round(random.uniform(20, 30), 1),
        "humidity": round(random.uniform(35, 70), 1)
    }


for month in range(1, 10):

    rows = []

    # 7月以降は不良率上昇
    ng_rate = 0.02 if month <= 6 else 0.08

    start_date = datetime(YEAR, month, 1)

    if month == 12:
        end_date = datetime(YEAR + 1, 1, 1)
    else:
        end_date = datetime(YEAR, month + 1, 1)

    current_day = start_date

    while current_day < end_date:

        # 土日除外
        if current_day.weekday() < 5:

            lot_times = [
                current_day.replace(hour=8, minute=0, second=0),
                current_day.replace(hour=13, minute=0, second=0),
                current_day.replace(hour=18, minute=0, second=0)
            ]

            for lot_index, lot_time in enumerate(lot_times, start=1):

                line = random.choice(LINES)
                product = random.choice(list(PRODUCTS.keys()))
                operator = random.choice(OPERATORS)

                lot_no = (
                    f"LOT"
                    f"{YEAR}"
                    f"{month:02}"
                    f"{current_day.day:02}"
                    f"{lot_index:02}"
                )

                for i in range(100):

                    timestamp = (
                        lot_time +
                        timedelta(seconds=i * 15)
                    )

                    rows.append(
                        create_record(
                            timestamp,
                            line,
                            product,
                            lot_no,
                            operator,
                            ng_rate
                        )
                    )

        current_day += timedelta(days=1)

    df = pd.DataFrame(rows)

    output_file = (
        BASE_PATH /
        f"inspection_results_{YEAR}{month:02}.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"{output_file.name} "
        f"作成完了 : {len(df):,}件"
    )

print("全データ生成完了")


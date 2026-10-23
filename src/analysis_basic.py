from pathlib import Path
import pandas as pd

# ファイルパス
DATA_FILE = Path(
    r"data\\inspection_results_all.csv"
)

# CSV読込
df = pd.read_csv(DATA_FILE)

print("=" * 50)
print("検査データ基本分析")
print("=" * 50)

# ------------------
# 全体集計
# ------------------

total_count = len(df)

result_counts = df["result"].value_counts()

ok_count = result_counts.get("OK", 0)
ng_count = result_counts.get("NG", 0)

yield_rate = ok_count / total_count * 100

print(f"総検査数 : {total_count:,}")
print(f"OK数     : {ok_count:,}")
print(f"NG数     : {ng_count:,}")
print(f"歩留まり : {yield_rate:.2f}%")

print()

# ------------------
# ライン別
# ------------------

print("=" * 50)
print("ライン別歩留まり")
print("=" * 50)

line_summary = (
    df.groupby("line_no")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

line_summary["Yield(%)"] = (
    line_summary["OK"]
    / (line_summary["OK"] + line_summary["NG"])
    * 100
)

print(line_summary)

print()

# ------------------
# 品番別
# ------------------

print("=" * 50)
print("品番別歩留まり")
print("=" * 50)

product_summary = (
    df.groupby("product_no")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

product_summary["Yield(%)"] = (
    product_summary["OK"]
    / (product_summary["OK"] + product_summary["NG"])
    * 100
)

print(product_summary)

print()

# ------------------
# 作業者別
# ------------------

print("=" * 50)
print("作業者別歩留まり")
print("=" * 50)

operator_summary = (
    df.groupby("operator")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

operator_summary["Yield(%)"] = (
    operator_summary["OK"]
    / (operator_summary["OK"] + operator_summary["NG"])
    * 100
)

print(operator_summary)

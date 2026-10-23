from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# ファイル読込
# ==========================

DATA_FILE = Path(
    r"C:\\Users\\4096834\\Desktop\\作業\\ポートフォリオ用\\検査工程データ分析ツール\\data\\inspection_results_all.csv"
)

df = pd.read_csv(DATA_FILE)

# ==========================
# 日付変換
# ==========================

df["timestamp"] = pd.to_datetime(df["timestamp"])

df["month"] = df["timestamp"].dt.month

# ==========================
# 月別集計
# ==========================

monthly_summary = (
    df.groupby("month")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

monthly_summary["NG Rate (%)"] = (
    monthly_summary["NG"]
    / (monthly_summary["OK"] + monthly_summary["NG"])
    * 100
)

print(monthly_summary)

# ==========================
# グラフ作成
# ==========================

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_summary.index,
    monthly_summary["NG Rate (%)"],
    marker="o",
    linewidth=2
)

plt.title("Monthly NG Rate Trend")
plt.xlabel("Month")
plt.ylabel("NG Rate (%)")
plt.grid(True)

plt.xticks(range(1, 10))

plt.tight_layout()

# ==========================
# 保存
# ==========================

output_file = Path(
    r"C:\\Users\\4096834\\Desktop\\作業\\ポートフォリオ用\\検査工程データ分析ツール\\graphs\\monthly_ng_rate.png"
)

output_file.parent.mkdir(
    exist_ok=True
)

plt.savefig(output_file)

print()
print(f"グラフ保存完了: {output_file}")

plt.show()
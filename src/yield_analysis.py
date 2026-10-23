from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# ファイル読込
# ==========================

DATA_FILE = Path(
    r"C:\\Users\\4096834\\Desktop\\作業\\ポートフォリオ用\\検査工程データ分析ツール\\data\\inspection_results_all.csv"
)

GRAPH_DIR = Path(
    r"C:\\Users\\4096834\\Desktop\\作業\\ポートフォリオ用\\検査工程データ分析ツール\\graphs"
)

GRAPH_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

# ==========================
# 共通関数
# ==========================

def create_yield_graph(group_col, output_name, title):

    summary = (
        df.groupby(group_col)["result"]
        .value_counts()
        .unstack(fill_value=0)
    )

    summary["Yield(%)"] = (
        summary["OK"]
        / (summary["OK"] + summary["NG"])
        * 100
    )

    print()
    print(f"===== {title} =====")
    print(summary)

    plt.figure(figsize=(10, 5))

    bars = plt.bar(
        summary.index,
        summary["Yield(%)"]
    )

    plt.title(title)
    plt.ylabel("Yield (%)")
    plt.ylim(90, 100)
    plt.grid(axis="y")

    for bar in bars:
        y = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width()/2,
            y + 0.05,
            f"{y:.2f}%",
            ha="center"
        )

    plt.tight_layout()

    output_file = GRAPH_DIR / output_name

    plt.savefig(output_file)

    print(f"保存完了: {output_file}")

    plt.close()


# ==========================
# ライン別歩留まり
# ==========================

create_yield_graph(
    "line_no",
    "line_yield_rate.png",
    "Line Yield Rate"
)

# ==========================
# 作業者別歩留まり
# ==========================

create_yield_graph(
    "operator",
    "operator_yield_rate.png",
    "Operator Yield Rate"
)

# ==========================
# 品番別歩留まり
# ==========================

create_yield_graph(
    "product_no",
    "product_yield_rate.png",
    "Product Yield Rate"
)

print()
print("全グラフ出力完了")
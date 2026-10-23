from pathlib import Path
import pandas as pd

# データフォルダ
DATA_DIR = Path(
    r"data\\2026"
)

# CSVファイル取得
csv_files = sorted(DATA_DIR.glob("*.csv"))

print(f"CSVファイル数: {len(csv_files)}")

# DataFrame格納用
df_list = []

for file in csv_files:
    print(f"読込中: {file.name}")

    df = pd.read_csv(file)

    # 元ファイル名を保持
    df["source_file"] = file.name

    df_list.append(df)

# 全CSV結合
df_all = pd.concat(df_list, ignore_index=True)

print()
print("===== 読込結果 =====")
print(f"総レコード数: {len(df_all):,}")
print(f"総列数: {len(df_all.columns)}")

print()
print(df_all.head())

# 統合CSV保存
output_file = DATA_DIR.parent / "inspection_results_all.csv"

df_all.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print()
print(f"保存完了: {output_file}")

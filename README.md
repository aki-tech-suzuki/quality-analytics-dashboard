# 📊 AKI TECH Quality Analytics Platform

製造業向け品質分析ダッシュボード

Python・Streamlit・Plotlyを用いて開発した、
品質管理業務の効率化を目的としたWebアプリケーションです。

---

## 📌 開発背景

製造現場では品質データをExcelで集計・分析するケースが多く、

- 集計に時間がかかる
- 異常傾向の発見が遅れる
- ラインごとの比較が難しい

といった課題があります。

本システムでは品質データを自動集計し、
リアルタイムに分析できる環境を構築しました。

---

## 🚀 主な機能

- KPIダッシュボード
- 月別NG率分析
- ライン別歩留まり分析
- 作業者別歩留まり分析
- 品番別歩留まり分析
- 異常月検知
- ワーストランキング分析
- CSVエクスポート

---

## 🛠 使用技術

- Python
- Pandas
- Streamlit
- Plotly

---

## 📈 想定導入効果

- 集計作業の自動化
- 品質異常の早期発見
- レポート作成時間の削減
- データに基づく改善活動の推進

---

## 📷 スクリーンショット

### ダッシュボード画面

![Dashboard](screenshots/dashboard_top.png)

### 分析画面

![Analysis](screenshots/dashboard_analysis.png)

---

## 📂 フォルダ構成

```text
quality-analytics-dashboard

├── app.py
├── requirements.txt
├── README.md
├── data/
├── graphs/
└── src/
```

---

## ▶ 実行方法

```bash
pip install -r requirements.txt

streamlit run app.py
```

---

## 💡 ポイント

- 製造業向け品質分析ダッシュボード
- リアルタイム集計
- 異常月の自動検出
- KPIの可視化
- フィルタ機能による分析

---

## ⚠ 注意

掲載データはポートフォリオ用のサンプルデータです。

実際の業務データ、顧客情報、機密情報は含まれていません。

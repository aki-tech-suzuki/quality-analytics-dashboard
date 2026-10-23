from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# ==================================
# ページ設定
# ==================================

st.set_page_config(
    page_title="AKI TECH Quality Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================
# CSS
# ==================================

st.markdown("""
<style>

.main{
    background-color:#f8fafc;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 3px 12px rgba(0,0,0,0.08);
    border-left:6px solid #2563eb;
}

.metric-title{
    color:#64748b;
    font-size:14px;
}

.metric-value{
    color:#0f172a;
    font-size:32px;
    font-weight:bold;
}

.footer{
    text-align:center;
    color:#64748b;
    padding:30px;
    margin-top:30px;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# ヘッダー
# ==================================

st.markdown("""
# 📊 AKI TECH Quality Analytics Platform

リアルタイム品質分析ダッシュボード

製造ライン・作業者・品番ごとの品質状況を可視化し、
異常傾向を自動検出します。
""")

# ==================================
# ポートフォリオ説明
# ==================================

st.info("""
【課題】

・Excelによる品質集計に時間がかかる

・品質異常の発見が遅れる

・ライン別比較が難しい

【解決】

Python + Streamlit による品質分析ダッシュボードを開発

【効果】

・集計作業を自動化

・異常傾向を即時把握

・ライン別、作業者別、品番別の分析を実現
""")

# ==================================
# データ読込
# ==================================

DATA_FILE = Path(
    r"data\inspection_results_all.csv"
)

df = pd.read_csv(DATA_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["month"] = df["timestamp"].dt.month

# ==================================
# サイドバー
# ==================================

with st.sidebar:

    st.markdown("# AKI TECH")

    st.markdown("### 🎛 Dashboard Filter")

    st.markdown("---")

    selected_lines = st.multiselect(
        "Line",
        sorted(df["line_no"].unique()),
        default=sorted(df["line_no"].unique())
    )

    selected_products = st.multiselect(
        "Product",
        sorted(df["product_no"].unique()),
        default=sorted(df["product_no"].unique())
    )

    st.markdown("---")

    st.caption("Quality Analytics Dashboard")

# ==================================
# フィルタ
# ==================================

df = df[
    (df["line_no"].isin(selected_lines))
    &
    (df["product_no"].isin(selected_products))
]

# ==================================
# KPI
# ==================================

total_count = len(df)

ok_count = (df["result"] == "OK").sum()
ng_count = (df["result"] == "NG").sum()

yield_rate = ok_count / total_count * 100

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📦 Inspection</div>
        <div class="metric-value">{total_count:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">✅ Yield</div>
        <div class="metric-value">{yield_rate:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">❌ NG Count</div>
        <div class="metric-value">{ng_count:,}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🎯 OK Count</div>
        <div class="metric-value">{ok_count:,}</div>
    </div>
    """, unsafe_allow_html=True)

# ==================================
# 品質ステータス
# ==================================

status_color = "#22c55e"
status_text = "Excellent"

if yield_rate < 95:
    status_color = "#ef4444"
    status_text = "Critical"

elif yield_rate < 98:
    status_color = "#f59e0b"
    status_text = "Attention"

st.markdown(
    f"""
    <div style="
        background:{status_color};
        color:white;
        padding:15px;
        border-radius:10px;
        text-align:center;
        font-weight:bold;
        margin-top:10px;
        margin-bottom:10px;
    ">
        Quality Status : {status_text}
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================
# 月別NG率
# ==================================

monthly = (
    df.groupby("month")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

monthly["NG Rate"] = (
    monthly["NG"]
    /
    (monthly["NG"] + monthly["OK"])
    * 100
)

mean_ng = monthly["NG Rate"].mean()
std_ng = monthly["NG Rate"].std()

threshold = mean_ng + std_ng

abnormal_months = monthly[
    monthly["NG Rate"] > threshold
]

fig_month = px.line(
    monthly,
    x=monthly.index,
    y="NG Rate",
    markers=True,
    title="Monthly NG Rate"
)

fig_month.update_traces(
    line=dict(
        color="#2563eb",
        width=4
    )
)

fig_month.add_hline(
    y=threshold,
    line_dash="dash",
    line_color="red",
    annotation_text="Abnormal Threshold"
)

# ==================================
# ライン別歩留まり
# ==================================

line = (
    df.groupby("line_no")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

line["Yield"] = (
    line["OK"]
    /
    (line["OK"] + line["NG"])
    * 100
)

fig_line = px.bar(
    line.sort_values("Yield"),
    x=line.index,
    y="Yield",
    title="Line Yield Rate",
    text_auto=".2f",
    color_discrete_sequence=["#2563eb"]
)

# ==================================
# 作業者別歩留まり
# ==================================

operator = (
    df.groupby("operator")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

operator["Yield"] = (
    operator["OK"]
    /
    (operator["OK"] + operator["NG"])
    * 100
)

fig_operator = px.bar(
    operator.sort_values("Yield"),
    x=operator.index,
    y="Yield",
    title="Operator Yield Rate",
    text_auto=".2f",
    color_discrete_sequence=["#22c55e"]
)

# ==================================
# 品番別歩留まり
# ==================================

product = (
    df.groupby("product_no")["result"]
    .value_counts()
    .unstack(fill_value=0)
)

product["Yield"] = (
    product["OK"]
    /
    (product["OK"] + product["NG"])
    * 100
)

fig_product = px.bar(
    product.sort_values("Yield"),
    x=product.index,
    y="Yield",
    title="Product Yield Rate",
    text_auto=".2f",
    color_discrete_sequence=["#f59e0b"]
)

# ==================================
# グラフ共通設定
# ==================================

for fig in [
    fig_month,
    fig_line,
    fig_operator,
    fig_product
]:
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Segoe UI",
            size=14
        ),
        title_x=0.03,
        height=400
    )

# ==================================
# グラフ表示
# ==================================

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        fig_line,
        use_container_width=True
    )

c3, c4 = st.columns(2)

with c3:
    st.plotly_chart(
        fig_operator,
        use_container_width=True
    )

with c4:
    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

# ==================================
# 異常月分析
# ==================================

st.markdown("---")

st.subheader("🚨 Abnormal Month Detection")

if len(abnormal_months) > 0:

    st.error(
        f"{len(abnormal_months)} abnormal month(s) detected."
    )

    st.dataframe(
        abnormal_months[["NG Rate"]]
    )

else:

    st.success(
        "No abnormal months detected."
    )

# ==================================
# ワースト分析
# ==================================

st.markdown("---")

w1, w2 = st.columns(2)

with w1:

    st.subheader("🏭 Worst Line")

    st.dataframe(
        line
        .sort_values("Yield")
        .head(5)[["Yield"]]
        .style.format("{:.2f}")
    )

with w2:

    st.subheader("📦 Worst Product")

    st.dataframe(
        product
        .sort_values("Yield")
        .head(5)[["Yield"]]
        .style.format("{:.2f}")
    )

# ==================================
# CSVダウンロード
# ==================================

st.markdown("---")

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="quality_analysis.csv",
    mime="text/csv"
)

# ==================================
# サマリー
# ==================================

st.markdown("---")

st.subheader("📋 Analysis Summary")

st.info(f"""
Inspection Count : {total_count:,}

Yield Rate : {yield_rate:.2f}%

NG Count : {ng_count:,}

Available Analysis

・KPI Monitoring

・Monthly NG Trend

・Line Comparison

・Operator Comparison

・Product Comparison

・Abnormal Month Detection

・Worst Yield Ranking

・CSV Export
""")

# ==================================
# フッター
# ==================================

st.markdown("---")

st.markdown("""
<div class="footer">
Developed by AKI TECH<br>
Python / Pandas / Plotly / Streamlit
</div>
""", unsafe_allow_html=True)

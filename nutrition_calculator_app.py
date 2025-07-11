
import streamlit as st
import pandas as pd

# 食材營養對照表
data = {
    "食材": [
        "雞胸肉", "地瓜", "糙米(熟飯)", "水煮蛋", "酪梨油", "香蕉", "蛋白飲", "黑豆漿"
    ],
    "單位": [
        "100g", "100g", "250g", "1顆", "100g", "1根", "20+20g", "100g"
    ],
    "熱量": [
        165, 123, 353, 70, 792, 90, 171.56, 35.4
    ],
    "蛋白質": [
        31, 1.3, 8.8, 6, 0, 1, 25.44, 3.5
    ],
    "碳水": [
        3.6, 28, 74.6, 0.6, 0, 24, 6.88, 1.3
    ],
    "油脂": [
        0, 0.3, 2.1, 5, 88, 0.2, 4.7, 1.8
    ]
}
df = pd.DataFrame(data)

st.title("每日營養素計算器")

st.write("請輸入以下食材的攝取量（單位如右表）")

# 使用者輸入欄位
user_input = {}
cols = st.columns(4)
for i, row in df.iterrows():
    with cols[i % 4]:
        qty = st.number_input(f"{row['食材']}（{row['單位']}）", min_value=0.0, value=0.0, step=1.0)
        user_input[row["食材"]] = qty

# 單位轉換
unit_mapping = {
    "100g": 100,
    "1顆": 1,
    "1根": 1,
    "20+20g": 1,
    "250g": 250
}

# 計算總營養
total = {"熱量": 0, "蛋白質": 0, "碳水": 0, "油脂": 0}
for i, row in df.iterrows():
    food = row["食材"]
    intake = user_input[food]
    base = unit_mapping[row["單位"]]
    ratio = intake / base
    total["熱量"] += row["熱量"] * ratio
    total["蛋白質"] += row["蛋白質"] * ratio
    total["碳水"] += row["碳水"] * ratio
    total["油脂"] += row["油脂"] * ratio

st.subheader("總攝取營養素")
st.metric("熱量 (kcal)", f"{total['熱量']:.1f}")
st.metric("蛋白質 (g)", f"{total['蛋白質']:.1f}")
st.metric("碳水 (g)", f"{total['碳水']:.1f}")
st.metric("油脂 (g)", f"{total['油脂']:.1f}")

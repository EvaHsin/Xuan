
import streamlit as st
import pandas as pd

# 固定食材營養資料表
nutrition_data = {
    "食材": ["雞胸肉", "地瓜", "糙米(熟飯)", "水煮蛋", "酪梨油", "香蕉", "蛋白飲", "黑豆漿"],
    "單位": ["100g", "100g", "250g", "1顆", "100g", "1根", "20+20g", "100g"],
    "熱量": [165, 123, 353, 70, 792, 90, 171.56, 35.4],
    "蛋白質": [31, 1.3, 8.8, 6, 0, 1, 25.44, 3.5],
    "碳水": [3.6, 28, 74.6, 0.6, 0, 24, 6.88, 1.3],
    "油脂": [0, 0.3, 2.1, 5, 88, 0.2, 4.7, 1.8],
}
df_nutrition = pd.DataFrame(nutrition_data)
unit_map = {"100g": 100, "250g": 250, "1顆": 1, "1根": 1, "20+20g": 1}

# 訓練日與非訓練日時段定義
time_slots = {
    "訓練日": ["06:30", "09:30", "12:30", "17:30", "18:00", "21:00", "22:00"],
    "非訓練日": ["06:30", "09:30", "12:30", "17:30", "21:00"],
}

st.title("每日營養素計算器（含臨時餐）")

# 選擇訓練日與否
day_type = st.radio("今天是訓練日嗎？", ["訓練日", "非訓練日"])
slots = time_slots[day_type]

daily_total = {"熱量": 0, "蛋白質": 0, "碳水": 0, "油脂": 0}

st.header("📋 固定時段攝取（每餐8項）")

# 每個時段輸入欄位
for time in slots:
    with st.expander(f"🍱 {time} 餐"):
        meal_total = {"熱量": 0, "蛋白質": 0, "碳水": 0, "油脂": 0}
        cols = st.columns(4)
        for i, row in df_nutrition.iterrows():
            with cols[i % 4]:
                val = st.number_input(f"{row['食材']} ({row['單位']}) - {time}", min_value=0, value=0, step=1)
                ratio = val / unit_map[row["單位"]]
                meal_total["熱量"] += row["熱量"] * ratio
                meal_total["蛋白質"] += row["蛋白質"] * ratio
                meal_total["碳水"] += row["碳水"] * ratio
                meal_total["油脂"] += row["油脂"] * ratio
        st.markdown(f"✅ 總熱量：{meal_total['熱量']:.1f} kcal，蛋白質：{meal_total['蛋白質']:.1f}g，碳水：{meal_total['碳水']:.1f}g，脂肪：{meal_total['油脂']:.1f}g")
        for k in daily_total:
            daily_total[k] += meal_total[k]

# 臨時餐自由輸入區
st.header("🆘 臨時餐（自由輸入）")

temp_foods = st.number_input("你今天吃了幾樣臨時食物？", min_value=0, max_value=10, step=1)
for i in range(temp_foods):
    with st.expander(f"🍡 臨時餐第 {i+1} 項"):
        name = st.text_input(f"食物名稱 {i+1}", key=f"name_{i}")
        cal = st.number_input("熱量 (kcal)", min_value=0.0, step=1, key=f"cal_{i}")
        pro = st.number_input("蛋白質 (g)", min_value=0.0, step=0.1, key=f"pro_{i}")
        carb = st.number_input("碳水 (g)", min_value=0.0, step=0.1, key=f"carb_{i}")
        fat = st.number_input("油脂 (g)", min_value=0.0, step=0.1, key=f"fat_{i}")
        daily_total["熱量"] += cal
        daily_total["蛋白質"] += pro
        daily_total["碳水"] += carb
        daily_total["油脂"] += fat

# 總結



st.markdown("## 📊 全日總攝取")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"**熱量**
{daily_total['熱量']:.1f} / 2000 kcal")
with col2:
    st.markdown(f"**蛋白質**
{daily_total['蛋白質']:.1f} / 130 g")
with col3:
    st.markdown(f"**碳水**
{daily_total['碳水']:.1f} / 250 g")
with col4:
    st.markdown(f"**油脂**
{daily_total['油脂']:.1f} / 55 g")

st.header("📊 全日總攝取")
st.metric("總熱量 (kcal)", f"{daily_total['熱量']:.1f}")
st.metric("總蛋白質 (g)", f"{daily_total['蛋白質']:.1f}")
st.metric("總碳水 (g)", f"{daily_total['碳水']:.1f}")
st.metric("總脂肪 (g)", f"{daily_total['油脂']:.1f}")

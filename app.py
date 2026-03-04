import streamlit as st
import json
from datetime import date

# 设置
START_DATE = date(2026, 3, 2) # [cite: 6]
st.set_page_config(page_title="申邦鹞的课表", layout="centered")

# 读取数据
with open("my_schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

# 计算当前周
today = date.today()
delta_weeks = (today - START_DATE).days // 7 + 1
days_map = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
curr_day = days_map[today.weekday()]

st.title("📅 我的课表")
view_week = st.sidebar.number_input("查看周次", 1, 19, value=max(1, delta_weeks))

st.subheader(f"第 {view_week} 周 · {curr_day}")

day_courses = schedule.get(curr_day, [])
filtered = [c for c in day_courses if view_week in c['weeks']]

if not filtered:
    st.info("今天没课，好好休息！")
else:
    for c in filtered:
        with st.expander(f"{c['slot']} - {c['name']}", expanded=True):
            st.write(f"📍 地点：{c['location']}")
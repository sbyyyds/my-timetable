import streamlit as st
import json
from datetime import date, timedelta

# 基础配置
START_DATE = date(2026, 3, 2)
st.set_page_config(page_title="申邦鹞的课表", layout="centered")

# 加载数据
@st.cache_data
def load_data():
    with open("my_schedule.json", "r", encoding="utf-8") as f:
        return json.load(f)

schedule = load_data()

# 侧边栏
st.sidebar.header("📅 日期切换")
selected_date = st.sidebar.date_input("查看哪天？", value=date.today())

# 计算日期信息
delta_days = (selected_date - START_DATE).days
view_week = (delta_days // 7) + 1
days_map = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
view_day_name = days_map[selected_date.weekday()]

# 主界面显示
st.title("📚 我的智能课表")
st.info(f"今天是：{date.today()} (第 {max(1, (date.today()-START_DATE).days//7+1)} 周)")

st.subheader(f"{view_day_name} · 第 {view_week} 周")

# 筛选课程
day_courses = schedule.get(view_day_name, [])
filtered = [c for c in day_courses if view_week in c['weeks']]

if not filtered:
    st.success("☕ 今天竟然没有课！去运动或者休息一下吧。")
else:
    for c in filtered:
        with st.container():
            st.markdown(f"""
            <div style="border:1px solid #e6e9ef; padding:15px; border-radius:10px; margin-bottom:10px; background-color: #f9f9f9;">
                <h3 style="margin-top:0; color: #1f77b4;">{c['name']}</h3>
                <p style="margin-bottom:5px;"><b>⏰ 时间：</b>{c['slot']}</p>
                <p style="margin-bottom:0;"><b>📍 地点：</b>{c['location']}</p>
            </div>
            """, unsafe_allow_html=True)

if st.sidebar.button("回到今天"):
    st.rerun()

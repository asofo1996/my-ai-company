# ✅ admin_dashboard.py (완성형 관리자 대시보드 with Supabase, 상태 추적, 시각화, 수정 기능)

import streamlit as st
import pandas as pd
import os
import time
import datetime
import graphviz
from dotenv import load_dotenv
from supabase import create_client

# ✅ 환경변수 로딩 및 Supabase 클라이언트 연결
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ 관리자 전용 접근
ADMIN_EMAIL = "tjryv1996@gmail.com"
email = st.text_input("👤 관리자 이메일을 입력하세요:", value=ADMIN_EMAIL)
if email != ADMIN_EMAIL:
    st.warning("⚠️ 접근 권한이 없습니다. 관리자 이메일로 로그인해주세요.")
    st.stop()

# ✅ 앱 설정
st.set_page_config(page_title="Crew AI 관리자 대시보드", layout="wide")
st.title("🚀 Crew AI 관리자 대시보드")

# ✅ Supabase에서 작업 데이터 가져오기
@st.cache_data(ttl=60)
def fetch_feedbacks():
    res = supabase.table("feedbacks").select("*").order("created_at", desc=True).limit(100).execute()
    return pd.DataFrame(res.data)

df = fetch_feedbacks()

# ✅ 날짜 포맷 변경
if not df.empty:
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)

# ✅ 탭 구성
탭1, 탭2, 탭3, 탭4, 탭5 = st.tabs(["📡 실시간 작업", "📋 전체 내역", "📈 상태 분석", "🧠 역할 구조", "✅ 단계 추적"])

# ✅ [1] 실시간 작업 현황
with 탭1:
    st.subheader("📡 최신 작업 결과")
    latest = df.iloc[0] if not df.empty else None
    if latest is not None:
        st.markdown(f"**🕒 작업일시:** {latest['created_at']}")
        st.markdown(f"**📧 작성자:** {latest['creator_email']}")
        st.markdown(f"**📂 카테고리:** {latest['category']}")
        st.markdown(f"**📝 지시 내용:** {latest['feedback_text']}")
        st.markdown(f"**🤖 GPT 결과:**\n\n{latest['result']}")
    else:
        st.info("데이터가 없습니다.")

# ✅ [2] 전체 내역 확인 및 수정
with 탭2:
    st.subheader("📋 전체 작업 기록")
    st.dataframe(df[["created_at", "creator_email", "category", "feedback_text", "result"]], use_container_width=True)

    st.markdown("---")
    st.subheader("🔄 결과 수동 수정")
    target = st.selectbox("수정할 피드백을 선택하세요", df["id"])
    selected = df[df["id"] == target].iloc[0]
    new_result = st.text_area("🧠 새 GPT 결과 입력", value=selected["result"])
    if st.button("💾 결과 저장"):
        supabase.table("feedbacks").update({"result": new_result}).eq("id", target).execute()
        st.success("저장 완료! 새로고침해주세요.")

# ✅ [3] 상태 분석
with 탭3:
    st.subheader("📈 작업 상태 분석")
    count_by_category = df["category"].value_counts()
    st.bar_chart(count_by_category)

    df_day = df.copy()
    df_day["day"] = df_day["created_at"].dt.date
    st.line_chart(df_day.groupby("day").size())

# ✅ [4] 역할 구조 시각화
with 탭4:
    st.subheader("🧠 Crew AI 역할 구조")
    graph = graphviz.Digraph()
    graph.edge("CEO", "PM")
    graph.edge("PM", "Dev")
    graph.edge("PM", "Design")
    graph.edge("Dev", "Test")
    graph.edge("Design", "Test")
    graph.edge("Test", "Report")
    graph.edge("Report", "ADMIN")
    st.graphviz_chart(graph)

# ✅ [5] 단계 추적 (단계별 완료 여부 체크 및 저장)
with 탭5:
    st.subheader("✅ 지시별 작업 단계 추적")
    row = df.iloc[0] if not df.empty else None
    if row is not None:
        stages = ["지시 분석", "콘텐츠 생성", "검토", "리포트 작성"]
        state_dict = {}
        for s in stages:
            state_dict[s] = st.checkbox(f"✔️ {s} 완료", value=False)

        if st.button("💾 단계 저장"):
            supabase.table("feedbacks").update({"current_stage": ", ".join([k for k,v in state_dict.items() if v])}).eq("id", row["id"]).execute()
            st.success("저장 완료. 단계가 기록되었습니다.")
    else:
        st.info("데이터가 없습니다.")

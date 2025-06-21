import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime
import graphviz

# ✅ 환경변수 기반 DB 경로 연결
def get_db_connection():
    db_path = os.getenv("AI_DB_PATH")
    if not db_path:
        db_path = os.path.join(os.path.dirname(__file__), "app", "db", "company_data.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- 페이지 기본 설정 ---
st.set_page_config(layout="wide", page_title="AI CEO Command Center")
st.title("🚀 AI CEO Command Center")

# --- 탭 구성 ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 프로젝트 지휘소", 
    "📂 보고 및 산출물", 
    "✍️ 프로젝트 위키", 
    "💳 결제 및 승인",
    "🤖 AI 역할 구조도"
])

# --- 탭 1: 프로젝트 지휘소 ---
with tab1:
    st.header("프로젝트 지휘소")
    project_list = [
        "광고 콘텐츠 생성기", "유튜브 자동 영상 편집기", "병원 성과 보고서 자동화",
        "카카오톡 이모티콘 분석기", "쇼핑몰 스마트 마케팅", "미팅 자동 기록 분석기",
        "AI 고객상담 비서", "GPT 채용면접관", "자동 랜딩페이지 제작기",
        "영상 검토 리포트 엔진", "기업 AI 대시보드"
    ]
    selected_project_name = st.selectbox("지휘할 프로젝트를 선택하십시오:", project_list)
    project_id = project_list.index(selected_project_name)

    feedback_text = st.text_area("새로운 지시사항이나 피드백을 여기에 입력하세요:", height=150)
    if st.button("AI 직원들에게 지시 전달하기", use_container_width=True):
        if feedback_text:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO feedback (project_id, feedback_text) VALUES (?, ?)',
                (project_id, feedback_text)
            )
            conn.commit()
            conn.close()
            st.success("✅ 새로운 지시가 성공적으로 전달되었습니다!")
            st.rerun()
        else:
            st.warning("⚠️ 지시사항을 입력해주세요.")

# --- 탭 2: 보고 및 산출물 ---
with tab2:
    st.header("프로젝트 보고 및 산출물")
    conn = get_db_connection()
    reports = conn.execute("SELECT * FROM reports ORDER BY timestamp DESC").fetchall()
    conn.close()

    if reports:
        df = pd.DataFrame(reports)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 보고서가 없습니다. 피드백을 입력하고 조금만 기다려보세요.")

# --- 탭 3: 프로젝트 위키 (상태 로그) ---
with tab3:
    st.header("프로젝트 상태 로그")
    conn = get_db_connection()
    logs = conn.execute("SELECT * FROM status_logs ORDER BY timestamp DESC").fetchall()
    conn.close()

    if logs:
        df = pd.DataFrame(logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("아직 상태 로그가 없습니다.")

# --- 탭 4: 결제 및 승인 ---
with tab4:
    st.header("결제 및 승인 요청")
    st.info("AI 직원들이 업무 수행 중 대표님의 결제/승인 확인이 필요한 요청들입니다.")

    conn = get_db_connection()
    approval_requests = conn.execute("SELECT * FROM approval_requests ORDER BY timestamp DESC").fetchall()
    conn.close()

    if approval_requests:
        df = pd.DataFrame(approval_requests)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df_display = df[['id', 'project_id', 'request_text', 'status', 'timestamp']]
        st.dataframe(df_display, use_container_width=True)

        with st.form("approval_form"):
            request_id = st.text_input("승인/거절할 요청 ID를 입력하세요:")
            col1, col2 = st.columns(2)
            with col1:
                approve = st.form_submit_button("✅ 승인")
            with col2:
                reject = st.form_submit_button("❌ 거절")

            if approve and request_id.isdigit():
                conn = get_db_connection()
                conn.execute("UPDATE approval_requests SET status = '승인 완료' WHERE id = ?", (request_id,))
                conn.commit()
                conn.close()
                st.success(f"요청 ID {request_id}를 승인했습니다.")
                st.rerun()
            elif reject and request_id.isdigit():
                conn = get_db_connection()
                conn.execute("UPDATE approval_requests SET status = '승인 거절' WHERE id = ?", (request_id,))
                conn.commit()
                conn.close()
                st.warning(f"요청 ID {request_id}를 거절했습니다.")
                st.rerun()
    else:
        st.info("현재 승인 요청이 없습니다.")

# --- 탭 5: AI 역할 구조도 ---
with tab5:
    st.header("🤖 AI 역할 및 상호작용 구조")
    st.markdown("각 AI 모듈 간의 협업 흐름을 시각화한 다이어그램입니다.")

    dot = graphviz.Digraph()
    dot.attr(rankdir="LR")
    dot.node("CEO", "👤 CEO 지시")
    dot.node("PM", "📋 프로젝트 매니저")
    dot.node("WRITER", "✍️ 콘텐츠 작성 AI")
    dot.node("EDITOR", "🎬 영상 편집 AI")
    dot.node("REPORT", "📊 분석/리포트 AI")
    dot.node("ADMIN", "🧑‍💼 관리자")

    dot.edge("CEO", "PM")
    dot.edge("PM", "WRITER")
    dot.edge("PM", "EDITOR")
    dot.edge("PM", "REPORT")
    dot.edge("REPORT", "ADMIN")
    dot.edge("EDITOR", "ADMIN")

    st.graphviz_chart(dot)

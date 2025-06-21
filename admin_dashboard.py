import streamlit as st
from supabase import create_client
import os
from datetime import datetime
import pandas as pd
import graphviz

# 환경변수에서 Supabase 연결 정보 불러오기
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit 설정
st.set_page_config(page_title="🧠 관리자 대시보드", layout="wide")
st.title("🧠 Crew AI 관리자 대시보드")
st.markdown("대표님의 전략적 판단이 더해질 때 AI는 비로소 진짜 일을 시작합니다.")

# 관리자 이메일 인증
admin_email = st.session_state.get("user_email", "")
if admin_email != "tjryv1996@gmail.com":
    st.error("관리자 전용 페이지입니다.")
    st.stop()

# Supabase에서 데이터 불러오기
try:
    data = supabase.table("feedbacks").select("*").order("timestamp", desc=True).execute().data
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
except Exception as e:
    st.error(f"❌ Supabase에서 데이터를 불러오지 못했습니다: {e}")
    st.stop()

# 탭 구성
st.sidebar.success("🧭 탭을 선택하세요")
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "🟢 실시간 진행 현황", "📋 전체 지시 내역", "📈 상태 분석", "🤖 역할 구조", "🧠 작업 단계 추적"
])

# --- 탭 0: 실시간 진행 현황 ---
with tab0:
    st.subheader("🟢 실시간 진행 현황 요약")
    if df.empty:
        st.info("아직 진행 중인 작업이 없습니다.")
    else:
        latest = df.iloc[0]
        st.markdown(f"**📥 현재 지시:** {latest['feedback_text']}")
        st.markdown(f"**📤 현재 결과 요약:** {latest['result'][:200]}...")
        st.markdown(f"**🧠 현재 AI 작업자:** {'자동 생성' if latest['is_auto'] else '수동 요청'}")
        st.markdown(f"**📅 시간:** {latest['timestamp']}")
        st.progress(0.6)

# --- 탭 1: 전체 지시 내역 ---
with tab1:
    st.subheader("📋 전체 지시 내역 및 피드백")
    if df.empty:
        st.info("지시 기록이 아직 없습니다.")
    else:
        for item in data:
            with st.expander(f"📄 {item.get('feedback_text')[:40]}... | 생성자: {item.get('creator_email')} | {item.get('timestamp', '')[:10]}"):
                st.markdown(f"**📥 지시 내용:**\n{item.get('feedback_text')}")
                st.markdown(f"**📤 AI 응답 결과:**\n{item.get('result') or '_응답 없음_'}")

                admin_comment = st.text_area("📝 관리자 코멘트", value=item.get("admin_comment") or "", key=f"comment_{item['id']}")
                reviewed = st.checkbox("✅ 검토 완료", value=item.get("reviewed_by_admin") or False, key=f"reviewed_{item['id']}")
                followup = st.checkbox("📌 후속 조치 필요", value=item.get("followup_required") or False, key=f"followup_{item['id']}")
                is_auto = st.checkbox("⚙️ 자동 생성 지시", value=item.get("is_auto") or False, key=f"auto_{item['id']}")

                if st.button("💾 저장", key=f"save_{item['id']}"):
                    try:
                        supabase.table("feedbacks").update({
                            "admin_comment": admin_comment,
                            "reviewed_by_admin": reviewed,
                            "followup_required": followup,
                            "is_auto": is_auto
                        }).eq("id", item["id"]).execute()
                        st.success("✅ 저장 완료")
                    except Exception as err:
                        st.error(f"❌ 저장 실패: {err}")

# --- 탭 2: 분석 및 시각화 ---
with tab2:
    st.subheader("📊 AI 응답 상태 및 전환율 분석")
    try:
        st.metric("전체 지시 수", len(df))
        st.metric("검토 완료 수", df['reviewed_by_admin'].sum())
        st.metric("후속 조치 필요 수", df['followup_required'].sum())
        chart_data = df.groupby(df['timestamp'].dt.date).size()
        st.line_chart(chart_data)
    except Exception as e:
        st.warning(f"시각화 불가: {e}")

# --- 탭 3: AI 역할 구조 시각화 ---
with tab3:
    st.subheader("🤖 AI 역할 및 상호작용 구조")
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

# --- 탭 4: 작업 단계 추적 ---
with tab4:
    st.subheader("🧠 AI 작업 단계별 흐름 추적")
    if df.empty:
        st.info("진행 중인 피드백이 없습니다.")
    else:
        latest = data[0]
        feedback_id = latest["id"]
        all_stages = ["지시 분석", "콘텐츠 작성", "영상 생성", "리포트 요약", "최종 검토"]

        current_stage = latest.get("current_stage") or all_stages[0]
        stage_index = latest.get("stage_index") or 0
        stage_total = latest.get("stage_total") or len(all_stages)

        st.markdown(f"**📍 현재 단계:** {current_stage} ({stage_index + 1} / {stage_total})")
        st.progress((stage_index + 1) / stage_total)

        for i, stage in enumerate(all_stages):
            symbol = "✅" if i < stage_index else "🔄" if i == stage_index else "☐"
            st.markdown(f"{symbol} 단계 {i+1}: {stage} {'완료' if i < stage_index else '진행 중' if i == stage_index else '대기'}")

        with st.form("수동 업데이트"):
            selected = st.selectbox("📌 현재 진행 단계 선택", all_stages, index=stage_index)
            new_index = all_stages.index(selected)
            submit = st.form_submit_button("📤 단계 저장")
            if submit:
                try:
                    supabase.table("feedbacks").update({
                        "current_stage": selected,
                        "stage_index": new_index,
                        "stage_total": len(all_stages)
                    }).eq("id", feedback_id).execute()
                    st.success("✅ 단계가 성공적으로 저장되었습니다!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 저장 실패: {e}")

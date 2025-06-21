import streamlit as st
from supabase import create_client
from app.utils.router import process_instruction
from app.utils.auth import signup, login
from app.utils.stripe import create_checkout_session
import stripe
import io
from datetime import datetime
import pandas as pd

# 기본 설정
st.set_page_config(page_title="My AI SaaS", layout="centered")
st.title("🧠 My AI SaaS 시스템 (Crew AI 버전)")
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

# --- 로그인 또는 회원가입 ---
auth_mode = st.radio("모드 선택", ["로그인", "회원가입"], horizontal=True)
email = st.text_input("이메일")
password = st.text_input("비밀번호", type="password")

if auth_mode == "회원가입":
    if st.button("회원가입"):
        try:
            res = signup(email, password)
            st.success("회원가입 완료. 로그인 해주세요.")
        except Exception as e:
            st.error(f"회원가입 실패: {e}")
else:
    if st.button("로그인"):
        try:
            res = login(email, password)
            if res and res.session:
                st.session_state["user_id"] = res.user.id
                st.session_state["user_email"] = email  # ✅ 관리자 인증용
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("로그인 실패")
        except Exception as e:
            st.error(f"로그인 오류: {e}")

# --- 로그인된 사용자 전용 기능 ---
if "user_id" in st.session_state:
    st.success(f"✅ 로그인됨: {st.session_state['user_email']}")

    # 로그아웃 버튼 추가
    if st.button("로그아웃"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

    tab1, tab2, tab3 = st.tabs(["📥 지시 전달", "📄 내 지시 이력", "💳 유료 기능 결제"])

    # --- 탭 1: 지시 전달 ---
    with tab1:
        st.subheader("📥 AI에게 지시할 내용을 입력하세요")
        project_id = st.selectbox("프로젝트 선택", [1, 2, 3])
        feedback = st.text_area("지시사항 입력", height=150)

        if st.button("AI에게 지시 전달"):
            try:
                gpt_result = process_instruction(feedback)

                # Supabase 저장
                supabase.table("feedbacks").insert({
                    "user_id": st.session_state["user_id"],
                    "project_id": project_id,
                    "feedback_text": feedback,
                    "category": gpt_result.split(" ")[0].replace("📢", "").replace("📊", "").replace("🎬", "").replace("💻", ""),
                    "result": gpt_result
                }).execute()

                st.success("✅ AI 응답:")
                st.info(gpt_result)

                # 응답 저장 버튼
                file_buffer = io.StringIO()
                file_buffer.write("🧠 AI 지시 내용\n\n")
                file_buffer.write(feedback + "\n\n")
                file_buffer.write("✅ AI 응답 결과\n\n")
                file_buffer.write(gpt_result)
                file_contents = file_buffer.getvalue().encode("utf-8")

                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"ai_response_{now}.txt"

                st.download_button(
                    label="📄 응답을 텍스트로 저장",
                    data=file_contents,
                    file_name=file_name,
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"처리 중 오류: {e}")

    # --- 탭 2: 지시 이력 ---
    with tab2:
        st.subheader("📄 내가 보낸 지시 목록")
        try:
            rows = supabase.table("feedbacks") \
                .select("*") \
                .eq("user_id", st.session_state["user_id"]) \
                .order("timestamp", desc=True) \
                .execute()

            if rows.data:
                df = pd.DataFrame(rows.data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                st.dataframe(df[['timestamp', 'project_id', 'category', 'feedback_text', 'result']], use_container_width=True)
            else:
                st.info("아직 지시사항이 없습니다.")
        except Exception as e:
            st.error(f"지시 목록 불러오기 오류: {e}")

    # --- 탭 3: 결제 ---
    with tab3:
        st.subheader("💳 유료 기능 결제하기")
        if st.button("Stripe 결제 시작"):
            try:
                url = create_checkout_session(st.session_state["user_email"])
                st.markdown(f"[👉 결제 페이지로 이동하기]({url})", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"결제 세션 생성 실패: {e}")

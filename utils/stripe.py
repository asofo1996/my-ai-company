import stripe
import streamlit as st

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

def create_checkout_session(user_email):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=user_email,
            line_items=[{
                "price": st.secrets["STRIPE_PRICE_ID"],  # .streamlit/secrets.toml에 설정
                "quantity": 1
            }],
            mode="payment",
            success_url=st.secrets.get("STRIPE_SUCCESS_URL", "https://example.com/success"),
            cancel_url=st.secrets.get("STRIPE_CANCEL_URL", "https://example.com/cancel")
        )
        return session.url
    except Exception as e:
        raise RuntimeError(f"Stripe 세션 생성 오류: {e}")

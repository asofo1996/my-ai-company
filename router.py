import requests

def classify_instruction(user_input):
    prompt = (
        "다음 지시사항을 [광고, 리포트, 영상, 개발, 기타] 중 하나로 분류하세요. "
        "반드시 하나의 단어만 출력하고, 설명은 하지 마세요.\n\n"
        f"{user_input}"
    )
    try:
        response = call_ollama(prompt)  # 아래에서 정의한 Ollama 호출 함수 사용
        return response.strip().lower()
    except Exception as e:
        return "기타"

def call_ollama(prompt):
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=150
        )
        data = res.json()
        return data.get("response", "[오류] 응답 파싱 실패")
    except Exception as e:
        return f"[연결 실패] Ollama 서버에 연결할 수 없습니다.\n\n{str(e)}"

def process_instruction(user_input):
    category = classify_instruction(user_input)
    # 원하는 형식으로 응답을 만들 수도 있음
    result = call_ollama(f"[{category.upper()}] 지시사항:\n{user_input}")
    return result

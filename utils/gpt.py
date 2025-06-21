import os
import requests

def call_gpt(prompt, model="llama3"):
    """
    Ollama 로컬 서버를 통해 GPT 모델에 프롬프트를 전달하고 응답을 반환합니다.
    환경변수 OLLAMA_BASE_URL이 설정되어 있으면 해당 주소를,
    없으면 기본적으로 host.docker.internal:11434를 사용합니다.
    """
    base_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
    url = f"{base_url}/api/chat"

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("message", {}).get("content", "").strip()
    except requests.exceptions.HTTPError as http_err:
        return f"[HTTP 오류] {http_err.response.status_code}: {http_err.response.text}"
    except requests.exceptions.ConnectionError:
        return "[연결 실패] Ollama 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요."
    except requests.exceptions.Timeout:
        return "[시간 초과] Ollama 응답이 지연되고 있습니다."
    except requests.exceptions.RequestException as e:
        return f"[요청 예외] {str(e)}"
    except Exception as e:
        return f"[알 수 없는 오류] {str(e)}"

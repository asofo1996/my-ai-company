# 1. Python 3.10 + 최소한의 OS 이미지
FROM python:3.10-slim

# 2. 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y curl

# 3. Ollama 설치 (서버는 외부에서 따로 실행)
RUN curl -fsSL https://ollama.com/install.sh | sh

# 4. 앱 작업 디렉토리 지정
WORKDIR /app

# 5. 전체 소스 복사 (app.py, utils, secrets.toml 등)
COPY . .

# 6. Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 7. Ollama 모델 다운로드는 주석 처리 (서버 외부 실행 필요)
# RUN ollama pull llama3

# 8. 컨테이너 포트 오픈
EXPOSE 8501

# 9. Streamlit 앱 실행 명령
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

from utils.gpt import call_gpt
from datetime import datetime

def generate_auto_instruction():
    today = datetime.now().strftime('%Y년 %m월 %d일')
    prompt = f"""
오늘은 {today}입니다.

당신은 국내외 최고의 수익을 창출할 SaaS 회사를 만들고 있는 CEO입니다.  
이 프로젝트에는 다음과 같은 10가지 고급 서비스를 통합하여 단일 웹 소프트웨어 형태로 제공합니다:

1. 광고 성과 리포트 시각화 (React, Recharts 기반)
2. 광고 영상 및 이미지 자동 제작 (Vrew, Dreamina 스타일)
3. 상세페이지/랜딩페이지 자동 생성 (DB카트+제디터 이상)
4. SNS 콘텐츠 자동 제작 및 일정 관리
5. 회사 맞춤형 자동화 프로그램 개발
6. 기존 광고 콘텐츠 분석 및 최적화 자동화
7. 수익형 SaaS 개발 컨설팅
8. 관련 강의 콘텐츠 자동 생성
9. PPT 자동 생성 (Felo AI, Gamma AI 이상)
10. Veo3 수준의 고품질 AI 영상 제작

오늘 Crew AI 팀에게 전달할 실제 업무 지시문 1개를 생성해줘.  
다음 조건을 만족해야 해:

조건:
- 위의 10가지 항목 중 오늘 가장 수익성과 실현 가능성이 높은 1가지를 선택
- 사용자가 직접 입력한 것처럼 자연스러운 문장으로 구성
- 실행 즉시 Crew가 어떤 Agent를 호출해야 할지 명확하게 판단할 수 있게 작성
- 너무 추상적이거나 한 줄 요약식은 피하고, 프로젝트를 시작할 수 있을 정도로 충분히 자세히 설명

결과는 오직 한 개의 지시문만 출력해줘.
"""
    return call_gpt(prompt).strip()

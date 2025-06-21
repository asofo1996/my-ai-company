from datetime import datetime
import os
import requests

# 환경 변수에서 Notion 토큰과 데이터베이스 ID 불러오기
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def log_to_notion(task, status, agent=None, notes=None):
    """
    작업 내용을 Notion 데이터베이스에 자동 기록합니다.

    Args:
        task (str): 수행한 작업 내용
        status (str): 상태 값 (예: 완료, 진행 중 등) - Notion DB의 select 항목과 일치해야 함
        agent (str, optional): 담당한 AI 또는 사용자 이름
        notes (str, optional): 비고 또는 부가 설명
    """

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "작업 내용": {"title": [{"text": {"content": task}}]},
            "상태": {"select": {"name": status}},
            "시간": {"date": {"start": datetime.utcnow().isoformat()}},
        }
    }

    if agent:
        payload["properties"]["담당자"] = {"rich_text": [{"text": {"content": agent}}]}
    if notes:
        payload["properties"]["비고"] = {"rich_text": [{"text": {"content": notes}}]}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in [200, 201]:
        print("✅ Notion 기록 성공")
    else:
        print(f"❌ Notion 기록 실패: {response.status_code}\n{response.text}")

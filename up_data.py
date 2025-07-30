import requests
import os
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

def up(oldest_date, latest_date, number_counts_dict, result):

    # Notion API Token（請確保有存取權限）
    notion_token = os.getenv("NOTION_TOKEN")


    # Notion Database ID
    database_id = os.getenv("NOTION_DATABASE_ID")

    # 設定 Notion API Headers
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # 建立 Notion Page 的 Payload
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "結果": {"title": [{"text": {"content": "數據分析結果"}}]},  # 確保這是資料庫中的欄位名稱
            "最舊日期": {"date": {"start": oldest_date}},  # 使用日期格式
            "最新日期": {"date": {"start": latest_date}},  # 使用日期格式
            "出現次數 {號碼: 次數}": {"rich_text": [{"text": {"content": str(number_counts_dict)}}]},  # 文字格式
            "是否有組": {"rich_text": [{"text": {"content": str(result)}}]}  # 文字格式
        }
    }

    # 送出 API 請求
    response = requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers)

    # 檢查回應
    if response.status_code == 200:
        print("✅ 成功上傳到 Notion！")
    else:
        print("❌ 上傳失敗:", response.text)

# 執行函數
if __name__ == "__main__":
    up()
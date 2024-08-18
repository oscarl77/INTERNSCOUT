import requests
import json

class Integration:

    def __init__(self, NOTION_TOKEN, DATABASE_ID):
        self.NOTION_TOKEN = NOTION_TOKEN
        self.DATABASE_ID = DATABASE_ID
        self.headers = {
            "Authorization": f"Bearer {self.NOTION_TOKEN}",
            "Content-type": "application/json",
            "Notion-version": "2022-06-28"
        }

    def _update_notion_page(self, internship_title, internship_url, submission_status):
        API_URL = "https://api.notion.com/v1/pages"
        
        data = {
            "parent": { "database_id": self.DATABASE_ID },
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": internship_title
                            }
                        }
                    ]
                },
                "Internship Description link": {
                    "url": internship_url
                },
                "Application submitted": {
                    "status": {
                        "name": submission_status
                    }
                }
            }
        }

        response = requests.post(API_URL, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Data added to Notion successfully")
        else:
            print(f"Failed to add data to Notion: {response.status_code}, {response.text}")
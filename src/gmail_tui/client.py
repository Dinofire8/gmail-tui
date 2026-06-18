from googleapiclient.discovery import build
from gmail_tui.auth import get_credentials

class GmailClient:
    def __init__(self):
        creds = get_credentials()
        self.service = build("gmail", "v1", credentials=creds)
        self.user = "me"
    
    def list_threads(self, label: str = "INBOX", max_results: int = 20):
        res = (
        self.service.users().threads().list(
            userId=self.user, labelIds=[label], maxResults=max_results).execute())
        return res.get("threads", [])
              
    def get_email(self,msg_id: str):
        res = (
            self.service.users().messages().get(userId=self.user, id=msg_id).execute()
        )
        return res
    
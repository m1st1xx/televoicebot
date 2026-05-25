import gspread

from datetime import datetime
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open(
    "Telegram Voice Logs"
).sheet1


def save_transcription(username: str, text: str):
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        username,
        text
    ])

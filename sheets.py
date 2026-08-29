import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets से डेटा पढ़ने और लिखने का फंक्शन
def get_depot_data(sheet_name):
    # Google API ऑथेंटिकेशन सेटअप
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # नोट: बाद में हम इसमें आपकी credentials.json फाइल जोड़ेंगे
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("RCM ALL").worksheet(sheet_name)
        data = sheet.get_all_records()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

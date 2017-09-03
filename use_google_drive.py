
"""
用途：串接 google 雲服務儲存
	  記得 client_secret.json 要先去取得，放當下目錄
	  取得方法可參考文獻
function:
    1.get_credentials : 取得並回傳一個憑證
    2.main() 上傳file，並設定參數 
    FILENAME=圖檔名稱 ,    enter_MIMETYPE=檔案類型，僅有圖、文,
    TITLE=雲服務上檔名,    DESCRIPTION=檔案描述，預設空白
    ex: FILENAME='eee.jpg',enter_MIMETYPE='圖',TITLE='image.jpg',DESCRIPTION=''
	
	參考文獻：https://developers.google.com/drive/v3/web/quickstart/python
"""

from __future__ import print_function
import httplib2
import os

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import googleapiclient.discovery
import googleapiclient.http
from googleapiclient.http import MediaFileUpload
import oauth2client.client

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive' # 設定要使用的更功能/權限
CLIENT_SECRET_FILE = 'client_secret.json' # json檔案裡面有設定檔案
APPLICATION_NAME = 'Drive API Python Quickstart' # 應用程式的名稱


def get_credentials(): # 讀取憑證
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('./') # 設定當下目錄路徑
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get() # 從Store取得憑證

    if not credentials or credentials.invalid: # 如果Store沒憑證，以下便從網頁上獲取 
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(FILENAME='eee.jpg',enter_MIMETYPE='圖',TITLE='image.jpg',DESCRIPTION=''):

    MIMETYPE_type = {'圖':'image/jpeg','文':'text/plain'} # 上傳檔案的格式
    MIMETYPE = MIMETYPE_type[enter_MIMETYPE] # 從dict尋找檔案的英文名稱

    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials() # 從這裡取得憑證

	# Create an authorized Drive API client.
    http = httplib2.Http()
    credentials.authorize(http)
    drive_service = googleapiclient.discovery.build('drive', 'v2', http=http)

    # Insert a file. Files are comprised of contents and metadata.
    # MediaFileUpload abstracts uploading file contents from a file on disk.
    # 這裡是填寫要上傳的資訊 MediaFileUpload 小型傳送 最多5MB
    media_body = googleapiclient.http.MediaFileUpload(
        FILENAME, 
        mimetype=MIMETYPE,
        resumable=True
    )
    # The body contains the metadata for the file.
    # 這裡是控制要傳送上雲端後的狀況 title=名稱 description=描述 parents=所在資料夾
    body = {
      'title': TITLE,
      'description': DESCRIPTION,
      'parents':[{'id':'0B3ZclpD_f2iwbDZubERpQk81ajQ'}]
    }

    # Perform the request and print the result.
    new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
    print('執行成功!')

if __name__ == '__main__':
    main()
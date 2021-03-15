from app.tool.aip import AipSpeech
""" 你的 APPID AK SK """
APP_ID = '15574037'
API_KEY = 'rny7V5diKufrA1ui5O5NZdlH'
SECRET_KEY = '2WGmf1pTj9HwimOBajBQBXqbO9orDi0L'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
# 识别本地文件
def Voice2Word():
	li=client.asr(get_file_content('wav/01.wav'), 'wav', 16000, {
    	'lan': 'zh',
	})

	return li
# 从URL获取文件识别
# client.asr('', 'pcm', 16000, {
#     'url': 'http://121.40.195.233/res/16k_test.pcm',
#     'callback': 'http://xxx.com/receive',
# })
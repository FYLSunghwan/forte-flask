import requests
url='http://0.0.0.0:5000/audiveris'
values={'TEST':'test'}
files={'file':open('test.py','rb')}
r = requests.post(url,files=files,data=values)
print(r.content)
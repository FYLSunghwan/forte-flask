import requests
url='http://0.0.0.0:5000/omr-convert'
values={'id':'test'}
files={'file':open('nandemo.pdf','rb')}
r = requests.post(url,files=files,data=values)
print(r.content)
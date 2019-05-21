import requests
from urllib.request import urlretrieve
path = 'C:/Users/luopan/Desktop/photo/'
url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1550468777489&di=054054453d3e36667596e249a7f6e7ae&imgtype=0&src=http%3A%2F%2Fs9.knowsky.com%2Fbizhi%2Fl%2F20100615%2F20109119%2520%25286%2529.jpg'
res = requests.get(url)
urlretrieve(url,path+url[-10:])

# import requests
#
# header = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like 09	Gecko) Chrome/55.0.2883.87 Safari/537.36'
# }
#
# path = 'C:/Users/luopan/Desktop/photo/'
# url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1550468777489&di=054054453d3e36667596e249a7f6e7ae&imgtype=0&src=http%3A%2F%2Fs9.knowsky.com%2Fbizhi%2Fl%2F20100615%2F20109119%2520%25286%2529.jpg'
#
# data = requests.get(url,headers=header)
# fp = open(path + url[-10:],'wb')
# fp.write(data.content)
# fp.close()
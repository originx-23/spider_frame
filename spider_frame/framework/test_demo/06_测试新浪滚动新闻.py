import requests

url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'http://roll.news.sina.com.cn/s/channel.php?ch=01'
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.content.decode('gbk'))

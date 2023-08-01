import requests
from bs4 import BeautifulSoup

# 指定目标网址
url = 'https://live.blockcypher.com/btc-testnet/tx/f96ba3e152b89a7318f88566d192ef37fcd44dd25b5305b5e1dedcd6b2c7861e/'

# 发送GET请求获取网页内容
response = requests.get(url)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 获取网页文本内容（去除HTML标签）
text_content = soup.get_text()

# 将文本内容保存到.txt文件中
with open('output after parse.txt', 'w', encoding='utf-8') as file:
    file.write(text_content)

import requests

url = "http://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?shopId=l33Y9txfMPk8v2nz&_token=eJyV0E8LgjAYBvCv4m0Xce/mXLOb0cXKiLAgokN/TSoTNzSKvnu+g4qOHQbP8+Md79iDVPGOdB3CAEAw4jqk3lcWPPAkdqPbyjogAz8AIXkoWtz+aiCtbqp5v+UlCzm4DlNyZXGK9kZQ0OqnCWxc4LHDMc6SozFll9Kmabxdvi7KvMi87fVC9fFa0rPvL0JzOySTk6p5ccdH/ncBN11Su4lxIdxAKWsna5jWn2S+luC/4DadZwXm/eCWDnUnHtFeotMZH6dRk4zmsyiLyjqbTsjzBYsLXls=&tcv=zj9r0md0w5&uuid=e5f18ed2-0f94-a5c1-6eba-496cdaa569fc.1623815619&platform=1&partner=150&optimusCode=10&originUrl=http://www.dianping.com/shop/l33Y9txfMPk8v2nz"  # 替换成你想要发送 GET 请求的 URL

# 发送 GET 请求
response = requests.get(url)
print(response)

# 检查请求是否成功
if response.status_code == 200:
    print("GET 请求成功！")
    print("响应内容:")
    print(response.text)
else:
    print(f"GET 请求失败，状态码: {response.status_code}")

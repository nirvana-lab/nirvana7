import requests

def s_config1(author, name):
    h = {"Authorization": author }
    url = "http://10.8.1.244:8888/contents"
    body = {"msgtype": "text","content": "jjjjji","name": name}
    rs = requests.request("POST",url, headers = h , json = body)
    print(rs.content)
    
def s_config2(a, b):
    y = a + b
    
def t_config1(author, name):
    h = {"Authorization": author }
    url = f"http://10.8.1.244:8888/contents/{name}"
    print(url)
    body = {"msgtype": "text","content": "update","name": name}
    rs = requests.request("PUT",url, headers = h , json = body)

def t_config2(a, b):
    y = a + b
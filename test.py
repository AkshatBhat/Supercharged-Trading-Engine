import requests

url = 'http://127.0.0.1:8000/api/token/'
data = {'username': 'KaranShah00', 'password': 'testing321'}
x = requests.post(url, data=data)
print(x.text)

# url = 'http://127.0.0.1:8000/api/orders/'
# x = requests.get(url, headers={"Authorization": "Token 2178f83db48752bf6f9a107cc126351bb01191b8"})
# print(x.text)
#"token":"2178f83db48752bf6f9a107cc126351bb01191b8"

# url = 'http://127.0.0.1:8000/api/signup/'
# data = {'username': 'KaranShah', 'password': 'testing321', 'email': 'kbshah2000@gmail.com'}
# x = requests.post(url, json=data)
# print(x.text)
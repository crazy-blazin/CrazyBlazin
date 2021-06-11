import requests



url = 'http://localhost:5000/api/admin/getinfo'
users = requests.get(url).json()

#### CHANGE

url = 'http://localhost:5000/api/admin/writeinfouser'
requests.post(url, json = users)


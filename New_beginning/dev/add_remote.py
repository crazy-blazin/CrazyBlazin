import requests



url = 'https://ec081fd7903d.ngrok.io/api/admin/getinfo'
users = requests.get(url).json()

users['Verzac']['health'] = 114
users['Verzac']['coins'] += 100

url = 'https://ec081fd7903d.ngrok.io/api/admin/writeinfouser'
x = requests.post(url, json = users)


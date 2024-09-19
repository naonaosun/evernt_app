import requests
import xmltodict

address = "岩手県盛岡市本宮荒屋25-11"

response = requests.get(f"https://www.geocoding.jp/api/?q={address}")

# XMLを辞書型に変換
data_dict = xmltodict.parse(response.text)

# 辞書から緯度と経度を取得
lat = data_dict['result']['coordinate']['lat']
lng = data_dict['result']['coordinate']['lng']

print(f"Latitude: {lat}")
print(f"Longitude: {lng}")


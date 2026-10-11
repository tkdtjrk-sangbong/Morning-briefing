import requests

url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type": "authorization_code",
    "client_id": "8f33572da213a3adbf0b97bdd6ff1e96",
    "redirect_uri": "https://localhost",
    "code": "Z0zzqFO_khexATtdsFYA7z_wn1cYOfJ5oNFzIOyILEHuCLP0vILWQQAAAAQKDSAbAAABoSv7Q_D_A_o_BVb6-Q"
}

response = requests.post(url, data=data)
print(response.json())
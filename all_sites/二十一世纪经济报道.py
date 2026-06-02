import requests
import json
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_search_key():

    url = "https://so.21jingji.com/elk/search/getSearchKey"

    resp = requests.get(url, headers=HEADERS)

    data = resp.json()

    return data["key"]


def aes_decrypt(encrypted_text, key):

    iv = "21jingji_search_".encode("utf-8")

    key = key.encode("utf-8")

    encrypted_data = base64.b64decode(encrypted_text)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(encrypted_data)

    decrypted = unpad(decrypted, AES.block_size)

    return decrypted.decode("utf-8")


def search_news(keyword, page=1):

    # 获取动态 key
    key = get_search_key()

    url = "https://so.21jingji.com/elk/search/searchWeb/"

    params = {
        "keywords": keyword,
        "page": page
    }

    resp = requests.get(url, params=params, headers=HEADERS)

    data = resp.json()

    # 解密
    encrypted_list = data["list"]

    decrypted_json = aes_decrypt(encrypted_list, key)

    news_list = json.loads(decrypted_json)

    result = []

    for item in news_list:

        result.append({
            "title": item.get("title", ""),
            "publish_time": item.get("inputtime", ""),
            "url": item.get("url", ""),
            "source": "21世纪经济报道"
        })

    return result


if __name__ == "__main__":

    news = search_news("银行")

    for i in news:
        print(i)
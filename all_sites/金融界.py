from utils.request_util import post_json


def search_news(keyword, page_num=1, page_size=20):
    url = "https://gateway.jrj.com/jrj-news/news/searchNews2025"

    payload = {
        "keyWord": keyword,
        "pageSize": page_size,
        "pageNo": page_num,
        "type": 2,
        "makeDate": ""
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://www.jrj.com.cn",
        "Referer": "https://www.jrj.com.cn/",
        "Productid": "6000021"
    }

    data = post_json(
        url,
        json_data=payload,
        headers=headers
    )

    result = []

    for news in data.get("data", {}).get("data", []):
        result.append({
            "title": news.get("title", ""),
            "publish_time": news.get("makeDate", ""),
            "url": news.get("pcInfoUrl", ""),
            "source": "金融界"
        })

    return result


if __name__ == "__main__":

    news = search_news("银行")

    for i in news:
        print(i)

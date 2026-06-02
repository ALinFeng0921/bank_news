from utils.request_util import get_json


def search_news(keyword, page_num=1, page_size=20):
    url = "https://www.gz-cmc.com/contentapi/api/content/getChannelAllContents"

    params = {
        "siteId": "5e88c884e2ed4e7a9a8d5225c299f707",
        "keyword": keyword,
        "channelCode": "shouye",
        "pageNum": page_num,
        "pageSize": page_size
    }

    headers = {
        "Referer": "https://www.gz-cmc.com/",
        "X-Requested-With": "XMLHttpRequest"
    }

    data = get_json(url, params=params, headers=headers)

    result = []

    for item in data.get("list", []):
        news = item.get("data", {})

        result.append({
            "title": news.get("title", ""),
            "publish_time": news.get("publishTime", ""),
            "url": news.get("url", ""),
            "source": "广州日报"
        })

    return result

from utils.request_util import post_form
import re


def search_news(keyword, page_num=1, page_size=20):
    url = "https://api.zgswcn.com/cmsapi/searchArticle"

    data = {
        "keyWord": keyword,
        "searchLocation": 1,
        "searchType": 0,
        "beginTime": "",
        "endTime": "",
        "orderType": 1,
        "pageNumber": page_num,
        "pageSize": page_size,
        "total": 0,
        "columnID": -1,
        "subSiteID": 1,
        "siteID": 1,
        "includeSubNode": 1
    }

    headers = {
        "Origin": "https://www.zgswcn.com",
        "Referer": "https://www.zgswcn.com/",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    result = post_form(
        url,
        data=data,
        headers=headers
    )

    news_list = []

    for news in result.get("list", []):
        summary = re.sub(
            r"<[^>]+>",
            "",
            news.get("highlightContent", "")
        )

        news_list.append({
            "title": news.get("title", ""),
            "publish_time": news.get("publishTime", ""),
            "url": "",
            "source": "中国商报网",
            "summary": summary,
            "file_id": news.get("fileID")
        })

    return news_list


if __name__ == "__main__":

    news = search_news("银行")

    for item in news:
        print(item)

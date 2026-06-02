import requests
import time
import random


def get_json(url, params=None, headers=None, timeout=10):
    """
    通用 GET 请求
    """

    if headers is None:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            )
        }

    time.sleep(random.uniform(0.5, 1.5))

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=timeout
    )

    response.raise_for_status()

    return response.json()


def post_json(url, json_data=None, headers=None, timeout=10):
    """
    通用 POST 请求
    """

    if headers is None:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            ),
            "Content-Type": "application/json"
        }

    time.sleep(random.uniform(0.5, 1.5))

    response = requests.post(
        url,
        json=json_data,
        headers=headers,
        timeout=timeout
    )

    response.raise_for_status()

    return response.json()


def post_form(url, data=None, headers=None, timeout=10):
    """
    通用 POST Form 请求
    """

    if headers is None:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            )
        }

    time.sleep(random.uniform(0.5, 1.5))

    response = requests.post(
        url,
        data=data,
        headers=headers,
        timeout=timeout
    )

    response.raise_for_status()

    return response.json()


def get_html(url, params=None, headers=None, timeout=10):
    if headers is None:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            ),
            "Referer": url,
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/avif,"
                "image/webp,*/*;q=0.8"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9"
        }

    time.sleep(random.uniform(0.5, 1.5))

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=timeout
    )

    response.encoding = response.apparent_encoding

    response.raise_for_status()

    return response.text

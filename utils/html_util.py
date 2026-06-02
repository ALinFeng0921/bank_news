from bs4 import BeautifulSoup


def get_soup(html):
    return BeautifulSoup(html, "lxml")


def get_text(node):
    if node:
        return node.get_text(strip=True)
    return ""


def get_attr(node, attr):
    if node:
        return node.get(attr, "")
    return ""
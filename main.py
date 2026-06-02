import os
import sys
import importlib.util
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# =========================
# 配置
# =========================

KEYWORD = "银行"

QQ_EMAIL = os.environ["QQ_EMAIL"]
QQ_AUTH_CODE = os.environ["QQ_AUTH_CODE"]

RECEIVERS = [
    "805688330@qq.com",
]

OUTPUT_FILE = "银行资讯汇总.xlsx"


# =========================
# 时间解析
# =========================

def parse_time(time_str):
    if not time_str:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except:
            pass

    return None


# =========================
# 自动加载站点
# =========================

def load_modules():
    modules = []

    site_dir = Path("all_sites")

    for file in site_dir.glob("*.py"):

        module_name = file.stem

        try:

            spec = importlib.util.spec_from_file_location(
                module_name,
                file
            )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            modules.append(
                (
                    module_name,
                    module
                )
            )

            print(f"√ 加载成功: {module_name}")

        except Exception as e:

            print(f"× 加载失败: {module_name}")
            print(e)

    return modules


# =========================
# 采集新闻
# =========================

def crawl_all_news():
    all_news = []

    modules = load_modules()

    for module_name, module in modules:

        if not hasattr(module, "search_news"):
            continue

        try:

            print(f"开始采集: {module_name}")

            news_list = module.search_news(
                keyword=KEYWORD,
            )

            if news_list:
                print(
                    f"获取 {len(news_list)} 条"
                )

                all_news.extend(news_list)

        except Exception as e:

            print(f"采集失败: {module_name}")
            print(e)

    return all_news


# =========================
# 去重
# =========================

def remove_duplicate(news_list):
    seen = set()

    result = []

    for item in news_list:

        title = item.get(
            "title",
            ""
        ).strip()

        if title in seen:
            continue

        seen.add(title)

        result.append(item)

    return result


# =========================
# 保留近3天
# =========================

def keep_recent_news(news_list):
    result = []

    deadline = datetime.now() - timedelta(days=3)

    for item in news_list:

        dt = parse_time(
            item.get(
                "publish_time",
                ""
            )
        )

        if dt is None:
            continue

        if dt >= deadline:
            result.append(item)

    return result


# =========================
# 导出Excel
# =========================

def export_excel(news_list):
    df = pd.DataFrame(news_list)

    if len(df) == 0:
        df = pd.DataFrame(
            columns=[
                "title",
                "publish_time",
                "url",
                "source"
            ]
        )

    df.sort_values(
        by="publish_time",
        ascending=False,
        inplace=True
    )

    df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"输出完成：{OUTPUT_FILE}"
    )


# =========================
# 发送邮件
# =========================

# def send_email():
#     msg = MIMEMultipart()
#
#     msg["Subject"] = "银行资讯日报"
#
#     msg["From"] = QQ_EMAIL
#
#     msg["To"] = ",".join(
#         RECEIVERS
#     )
#
#     with open(
#             OUTPUT_FILE,
#             "rb"
#     ) as f:
#         part = MIMEBase(
#             "application",
#             "octet-stream"
#         )
#
#         part.set_payload(
#             f.read()
#         )
#
#         encoders.encode_base64(
#             part
#         )
#
#         part.add_header(
#             "Content-Disposition",
#             f'attachment; filename="{OUTPUT_FILE}"'
#         )
#
#         msg.attach(part)
#
#     smtp = smtplib.SMTP_SSL(
#         "smtp.qq.com",
#         465
#     )
#
#     smtp.login(
#         QQ_EMAIL,
#         QQ_AUTH_CODE
#     )
#
#     smtp.sendmail(
#         QQ_EMAIL,
#         RECEIVERS,
#         msg.as_string()
#     )
#
#     smtp.quit()
#
#     print("邮件发送成功")


def send_email(
        sender=QQ_EMAIL,
        password=QQ_AUTH_CODE,
        receivers=RECEIVERS,
        subject="银行资讯日报",
        content="",
        file_path=OUTPUT_FILE
):

    msg = MIMEMultipart()

    msg["From"] = sender
    msg["To"] = ",".join(receivers)
    msg["Subject"] = subject

    msg.attach(
        MIMEText(
            content,
            "plain",
            "utf-8"
        )
    )

    with open(file_path, "rb") as f:

        part = MIMEApplication(f.read())

        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=os.path.basename(file_path)
        )

        msg.attach(part)

    server = smtplib.SMTP_SSL(
        "smtp.qq.com",
        465
    )

    server.login(sender, password)

    server.sendmail(
        sender,
        receivers,
        msg.as_string()
    )

    server.quit()


# =========================
# 主程序
# =========================

def main():
    print("开始采集新闻...")

    news = crawl_all_news()

    print(f"原始新闻数: {len(news)}")

    news = remove_duplicate(news)

    print(f"去重后: {len(news)}")

    news = keep_recent_news(news)

    print(f"近三天: {len(news)}")

    export_excel(news)

    send_email()


if __name__ == "__main__":
    main()

from datetime import datetime

import pymongo
from slack import WebClient

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
hacker_news_db = mongo_client["hackernews"]
articles_collection = hacker_news_db["articles"]

slack_token = "<your own api key>"
slack_channel = "#hacker_news"
client = WebClient(token=slack_token)


def send_slack_messages():
    articles = articles_collection.find({"created_at": datetime.today().strftime("%Y-%m-%d")}).limit(1)
    header = {"type": "header", "text": {
        "type": "plain_text",
        "text": ":newspaper:  Hacker News Updates  :newspaper:"
    }}
    divider = {
        "type": "divider"
    }

    blocks = [header]

    for article in articles:
        markdown_text = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{article['title']}* \n\n{article['url']} \n\n"
            }
        }
        image_json = {
            "type": "image",
            "image_url": article['image_url'],
            "alt_text":"hacker_news"
        }

        blocks.append(markdown_text)
        blocks.append(image_json)
        blocks.append(divider)
        client.chat_postMessage(channel=slack_channel, blocks=blocks, username="jarvis")
        blocks.clear()


if __name__ == "__main__":
    send_slack_messages()

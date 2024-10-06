from flask import Flask, request
import json
from config import config

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    if data['action'] == 'opened':
        pr_url = data['pull_request']['html_url']
        # Trigger the bot to post the PR message on Discord
        # You can use a queue or shared state to communicate between Flask and Discord bot
        post_pr_to_discord(pr_url)
    return '', 200


def post_pr_to_discord(pr_url):
    # Use an internal mechanism to trigger the Discord bot to post the PR message
    pass

if __name__ == '__main__':
    app.run(port=config.WEBHOOK_PORT)
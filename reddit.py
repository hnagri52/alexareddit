from flask import Flask,render_template
from flask_ask import Ask,statement,question,session
import json
import requests
import unidecode
import time


app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def get_headlines():
    user_pass_dict = {
        "user": "momothebang",
        "passwd": "Hussein123",
        "api_type": "json"
    }

    sess = requests.Session()
    sess.headers.update({"User-Agent": "I am testing Alexa: Sentdex"})
    sess.post("https://reddit.com/api/login", data= user_pass_dict)
    time.sleep(1)
    url = "https://reddit.com/r/worldnews/.json?limit=10"
    html = sess.get(url)
    data = json.loads(html.content.decode("utf-8"))
    #rewrite the following 3 lines with: titles = [unicode.unicode(listing["data"]["title"]) for listing in data["data"]["children"]
    titles = []
    for listing in data["data"]["children"]:
        titles.append(unidecode.unidecode(listing["data"]["title"]))
    titles = "... ".join([i for i in titles])
    return titles

titles = get_headlines()
print(titles)







@app.route("/")
def homepage():
    return "Hi there, how are you doing?"

@ask.launch
def start_skill():
    welcome_msg = "Hello there, would you like the news?"
    return question(welcome_msg)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = "The current news headlines are {}".format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = "I am not sure why you asked to hear... but thank you and have a great day!"

    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=False)
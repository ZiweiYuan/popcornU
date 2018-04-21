from flask import Flask, send_from_directory, render_template, request, url_for
import config, urllib, json, requests, re, string
from firebase import firebase
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(config)
firebase = firebase.FirebaseApplication('https://popcornu-inf551.firebaseio.com', None)
Bootstrap(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/search")
def route_search():
    results = firebase.get('/Watchlists', None)
    return render_template('popcornU.html', results=results)


@app.route('/results', methods=['POST'])
def route_results():
    nums, keys, results = {}, [], []
    keywords = request.form['keywords']
    if keywords == "":
        results = firebase.get('/Watchlists', None)
        return render_template('popcornU.html', results=results)
    def parseToken(strings):
        strings = re.sub('[^a-zA-Z0-9]',' ',strings)
        strings = strings.lower()
        return strings.split()

    keywordToken = parseToken(keywords)
    for token in keywordToken:
        try:
            if token not in keys:
                keys.append(token)
                inums = firebase.get('/Keywords', token)
                for inum in inums:
                    if inum in nums.keys():
                        nums[inum] += 1
                    else:
                        nums[inum] = 1
        except:
            continue

    nums = sorted(nums.items(),key = lambda x:x[1],reverse = True)
    for num in nums:
        result = firebase.get('/Watchlists', num[0])
        results.append(result)

    return render_template('popcornU.html', results=results)


if __name__ == "__main__":
    app.run()

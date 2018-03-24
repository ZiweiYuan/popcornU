from flask import Flask, send_from_directory, render_template, request, url_for
import config, urllib, json, requests
from firebase import firebase

app = Flask(__name__)
app.config.from_object(config)
firebase = firebase.FirebaseApplication('https://popcornu-inf551.firebaseio.com', None)


@app.route("/")
def route_login():
    return render_template('login.html', userInfo = userInfo)

@app.route("/search")
def route_search():
    results = firebase.get('/Watchlists', None)
    return render_template('popcornU.html', results=results)

@app.route('/results', methods=['POST'])
def route_results():
    data = [{}]
    keywords = request.form['keywords']
    results = firebase.get('/Watchlists', keywords)
    temp = results
    # if firebase only return 1 json, it won't be stored as array (it is dict), so we need to convert it
    try:
        temp.extend(data)
    except:
        results = [temp]
    return render_template('popcornU.html', results=results)


if __name__ == "__main__":
    app.run()

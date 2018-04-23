from flask import Flask, send_from_directory, render_template, request, url_for, redirect
import config, urllib, json, requests, re, string
from firebase import firebase
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(config)
firebase = firebase.FirebaseApplication('https://popcornu-inf551.firebaseio.com', None)
Bootstrap(app)
types = sorted(firebase.get('/Types', None).keys())
genres = sorted(firebase.get('/Genres', None).keys())
years = sorted(firebase.get('/Years', None).keys())

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	url = 'https://popcornu-user.firebaseio.com/users.json'
	response = requests.get(url).json()
	return render_template('login.html', response=response)


@app.route("/search")
def route_search():
	results = firebase.get('/Watchlists', None)
	return render_template('popcornU.html', results=results, types=types, genres=genres, years=years)


@app.route('/results', methods=['POST'])
def route_results():
	nums, keys, results, keywordNum, filterNum = {}, [], [], [], []
	typeNum, genreNum, yearNum, filters = [], [], [], []

	keywords = request.form['keywords']
	typesSubmit = request.values.getlist("types")
	genresSubmit = request.values.getlist("genres")
	yearsSubmit = request.values.getlist("years")

	for x in typesSubmit:
		filters.append(x)
		if str(x) != "all types":
			typeNum.extend(firebase.get('/Types', str(x)))

	for genre in genresSubmit:
		filters.append(genre)
		if str(genre) != "all genres":
			genreNum.extend(firebase.get('/Genres', str(genre)))

	for year in yearsSubmit:
		filters.append(year)
		if str(year) != "all years":
			yearNum.extend(firebase.get('/Years', str(year)))

	if typeNum != []:
		filterNum.extend(typeNum)
	if filterNum != []:
		if genreNum != []:
			filterNum = list(set(filterNum).intersection(set(genreNum)))
	else:
		if genreNum != []:
			filterNum.extend(genreNum)
	if filterNum != []:
		if yearNum != []:
			filterNum = list(set(filterNum).intersection(set(yearNum)))
	else:
		if yearNum != []:
			filterNum.extend(yearNum)


	def parseToken(strings):
		strings = re.sub('[^a-zA-Z0-9]',' ',strings)
		strings = strings.lower()
		return strings.split()

	if keywords == "":
		if filterNum == []:
			results = firebase.get('/Watchlists', None)
		else:
			for y in filterNum:
				result = firebase.get('/Watchlists', y)
				results.append(result)
	else:
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
			# intersection of facets search and keyword search
			if filterNum == [] or num[0] in filterNum:
				result = firebase.get('/Watchlists', num[0])
				results.append(result)

	return render_template('popcornU.html', results=results, types=types, genres=genres, years=years, keywords=keywords, filters=filters)

@app.route('/history', methods=['POST'])
def route_history():
	nums, keys, results, keywordNum = {}, [], [], []
	keywords = request.form['history']
	def parseToken(strings):
		strings = re.sub('[^a-zA-Z0-9]',' ',strings)
		strings = strings.lower()
		return strings.split()

	if keywords == "":
		results = firebase.get('/Watchlists', None)
	else:
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

	return render_template('popcornU.html', results=results, types=types, genres=genres, years=years, keywords=keywords)


if __name__ == "__main__":
	app.run()

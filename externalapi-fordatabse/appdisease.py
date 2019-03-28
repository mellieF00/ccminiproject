from flask import Flask, request, render_template, jsonify,json
import requests

# PART ONE: Ultilize the api servise an external REST service to complement 
# Authentication: use config to ensure sensitive API-key authentication
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Authentication: access api key in config file
API_KEY = app.config['APIKEY']


# Application: main page, welcome message and introduction.
@app.route('/')
def hello():
    name = request.args.get("name","world")
    return("<h1>Hello, {}!</h1>".format(name) + "<h2>This is a doctor-info App by " + \
        "Lexigram and Mellie, this App has two applications.</h2>" + \
        "<h3>MengyuanFan, studentID:180122581.</h3>" + \
        "<h3>MiniProject-Cloud Computer.</h3>")

# Part One: using other API to get information for my database
# Fisrt application-GET: use keyword = "cancer" to search for information related to that terminology
@app.route('/appfirst/<keyword>',  methods=['GET'])
def Search(keyword):
    # define terminology you want to search
    # keyword = ""
    # define limit of the result you want show on the webpage
    limit = str(20)
    url = "https://api.lexigram.io/v1/lexigraph/search?q=" + keyword + "&limit=" + limit
    resp = requests.get(url, headers={'Authorization': API_KEY})
    # assign the result into variable info; print the reason of failuer if fail
    # if len(keyword) == 0:
    #     return (jsonify({'error':'keyword not given'}))
    if resp.ok:
        info = resp.json()
    else:
        print(resp.reason)

    #save the unorgonized result into a list to show in the webpage
    result = info.get("conceptSearchHits")
    if len(result) == 0:
        return jsonify({'error':'keyword not found in the database'}),404
    else:
        output = []
        for item in result:
            temp = []
            score = item.get("score")
            ide = item["concept"]["id"]
            label = item["concept"]["label"]
            types = item["concept"]["types"]
            temp.append([score, ide, label])
            output.append(temp)
        #give response in the web page in a designed style, html stored in style.html
        return render_template('style.html', my_list = output), 200

if __name__=="__main__":
    app.run(port=8080, debug=True)
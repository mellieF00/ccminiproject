from flask import Flask, request
from cassandra.cluster import Cluster
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

cluster = Cluster(['35.197.194.158'])
# cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)


# Mainpage main page, welcome message and introduction.
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return("<h1>Hello, {}!</h1>".format(name) + "<h2>This is a doctor-info App by " + \
        "Lexigram and Mellie, this App has two applications.</h2>" + \
        "<h3>MengyuanFan, studentID:180122581.</h3>" + \
        "<h3>MiniProject-Cloud Computer.</h3>")

# First application, GET method
@app.route('/get/<ide>') 
def get_score(ide):
    rows = session.execute( """Select * From disease.stats where id = '{}'""".format(ide))
    for row in rows:
        return('<h1>{} has ({}) score and the label is ({})!</h1>'.format(ide, row.score, row.label)),200
    return('<h1>That ID does not exist!</h1>'),404

# Second-application, POST method
@app.route('/post/<score>/<ide>/<label>')
def post_rescore(score, ide, label):
    session.execute( """INSERT INTO disease.stats (score, id, label) VALUES ({},'{}','{}');""".format(score,ide,label))
    return('<h1>your information is inserted successfully!</h1>'),200


# Third-application, DELETE method
@app.route('/delete/<ide>')
def delete_rescore(ide):
    rows = session.execute( """Select * From disease.stats where id = '{}'""".format(ide))
    if len(list(rows)) == 0:
        return('<h1>your id does not exist!</h1>'),404
    session.execute("""DELETE FROM disease.stats WHERE id = '{}'""".format(ide))
    return('<h1>your information is deleted successfully!</h1>'),200


# Fourth-application-1, New user Sign up: use hash to store password, store username
@app.route('/newuser/<user>/<password>')
def newuser_password(user, password):
    rows = session.execute( """Select * From username.data where username = '{}'""".format(user))
    if len(list(rows)) != 0:
        return('<h1>your username already exists!</h1>')
    else:
        pw_hash = generate_password_hash(password)
        session.execute( """INSERT INTO username.data (username, password) VALUES ('{}','{}')""".format(user,pw_hash)),200
        return ('You username and password is safely stored!')


# Fourth-application-2, Old user login: check the user name and password
@app.route('/olduser/<user>/<password>')
def olduser_password(user, password):
    rows = session.execute( """Select * From username.data where username = '{}'""".format(user))
    row = list(rows)
    if len(row) == 0:
        return('<h1>your username does not exist!</h1>')
    else:
        # for row in rows:
        check_hash = check_password_hash(row[0].password, password)
        if check_hash:
            return ('pass! your are logged in now!')
        return ('fail! your password for the username is not right!')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

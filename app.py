from flask import Flask, request
from cassandra.cluster import Cluster
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# cluster = Cluster(['35.197.194.158'])
cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)


# Mainpage, welcome message and introductions.
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return("<h1>Hello, {}!</h1>".format(name) + "<h2>This is a doctor-info App by " + \
        "Lexigram and Mellie, this App has two applications.</h2>" + \
        "<h3>MengyuanFan, studentID:180122581.</h3>" + \
        "<h3>MiniProject-Cloud Computer.</h3>")

'''
First application, GET method
Use id as the primary key, show the score and label of that id in my database
Parameters: id
return: your id, score and label or a message tells that your id does not exit
'''
@app.route('/get/<ide>') 
def get_score(ide):
    rows = session.execute( """Select * From disease.stats where id = '{}'""".format(ide))
    for row in rows:
        return('<h1>{} has ({}) score and the label is ({})!</h1>'.format(ide, row.score, row.label)),200
    return('<h1>That ID does not exist!</h1>'),404


'''
Second-application, POST method,
create a new row of data with id, score and label
Parameters: id, score and label
return: a message tells you that data is inserted succefully.
'''
@app.route('/post/<score>/<ide>/<label>')
def post_rescore(score, ide, label):
    session.execute( """INSERT INTO disease.stats (score, id, label) VALUES ({},'{}','{}');""".format(score,ide,label))
    return('<h1>Your information is inserted successfully!</h1>'),200


'''
Third-application, DELETE method
delete a row of data with id
Parameters: id
return: a message tells you that the row of data is deleted succefully, or tells you your id doesn't exist.
'''
@app.route('/delete/<ide>')
def delete_rescore(ide):
    rows = session.execute( """Select * From disease.stats where id = '{}'""".format(ide))
    if len(list(rows)) == 0:
        return('<h1>Your id does not exist!</h1>'),404
    session.execute("""DELETE FROM disease.stats WHERE id = '{}'""".format(ide))
    return('<h1>Your information is deleted successfully!</h1>'),200


'''
Fourth-application, New user Sign up: use hash to store password, store username in my database
Parameters: username, password
return: a message tells you that you are signed up succefully, or tells you your username already exists.
'''
@app.route('/newuser/<user>/<password>')
def newuser_password(user, password):
    rows = session.execute( """Select * From username.data where username = '{}'""".format(user))
    if len(list(rows)) != 0:
        return('<h1>Your username already exists!</h1>')
    else:
        pw_hash = generate_password_hash(password)
        session.execute( """INSERT INTO username.data (username, password) VALUES ('{}','{}')""".format(user,pw_hash)),200
        return ('<h1>Your username and password are safely stored!</h1>')

'''
Fourth-application, Old user login: check the username and password and login
Parameters: username, password
return: a message tells you that you are logged in succefully, or tells you your username doesn't exit or your password is not right.
'''
@app.route('/olduser/<user>/<password>')
def olduser_password(user, password):
    rows = session.execute( """Select * From username.data where username = '{}'""".format(user))
    row = list(rows)
    if len(row) == 0:
        return('<h1>Your username does not exist!</h1>')
    else:
        check_hash = check_password_hash(row[0].password, password)
        if check_hash:
            return ('<h1>Pass! your are logged in now!</h1>')
        return ('<h1>Fail! your password for the username is not right!</h1>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

from typing import Text
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    mood = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        self.date = self.date.strftime("%b %d %Y")
        return f"{self.name} registered a mood of {self.mood} on {self.date}."


@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('mood'))
    return render_template('login.html', error=error)

@app.route('/mood')
def mood():
    moods = Mood.query.all()

    output = []
    for mood in moods:
        mood_data = {'id':mood.id, 'name': mood.name, 'mood':mood.mood,'date':mood.date.strftime("%b %d %Y")}
        output.append(mood_data)
    
    return {"moods" : output}


@app.route('/mood/<name>')
def get_moods(name):
    streak = 0
    moods = Mood.query.filter(Mood.name.is_(name)).order_by(Mood.date).all()

    output = []
    for mood in moods:
        mood_data = {'date':mood.date, 'mood':mood.mood, 'name': mood.name }
        output.append(mood_data)
    
    if len(output) != 0:
        prevDate = None
        for index in range(0,len(output)):
            curr = output[index].get('date')
            if prevDate == None:
                prevDate = curr
                streak=1
            else:
                if is_consecutive(prevDate,curr):
                    streak+=1
                else:
                    streak=1
                prevDate = curr
    return {"name": name, "streak" : streak}

def is_consecutive(prev, date):
    return True if prev + datetime.timedelta(days=1) == date else False
    
@app.route('/mood', methods=['POST'])
def add_mood():
    mood = Mood(id=request.json["id"], name=request.json['name'], mood=request.json["mood"], date=datetime.date(request.json["year"], request.json["month"], request.json["day"]))
    db.session.add(mood)
    db.session.commit()
    return "mood added"

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Mood(db.Model):
    name = db.Column(db.String, primary_key=True)
    mood = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default = datetime.strftime(datetime.now(), "%m/%d/%Y"), nullable=False)

    def __repr__(self):
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
        mood_data = {'name': mood.name, 'mood':mood.mood, 'date':mood.date}
        output.append(mood_data)
    
    return {"moods" : output}

@app.route('/mood/<name>')
def get_mood(name):
    mood = Mood.query.get_or_404(name)

    return {"name": name, "streak" : 0}
    
@app.route('/mood', methods=['POST'])
def add_mood():
    mood = Mood(name=request.json['name'], mood=request.json["mood"])
    db.session.add(mood)
    db.session.commit()
    return "mood added"

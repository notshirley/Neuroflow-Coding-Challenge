This was the first time I have ever created an API (watched a few lectures that taught me how to begin). I had never used flask, sqlalchemy, or this much of python before. Because I had to learn a lot as I went I couldn't make it look very nice. However, as a production application I would definitely make a more secure login. I would make it so we could move through the endpoints without having to type it in the address bar as well. I also did not include deleting data, editing data, or other actions not included in the assessment prompt that I would in production.

I still have a lot to learn about APIs in general so as for handling more users, more data, etc., that's something I need to learn.

To run:
    I used Visual Studio Code.
    Run the API by:
        cd API
        set FLASK_APP=application.py <!--or whatever the equivalent of set is in your environment-->
        set FLASK_ENV=development <!--or whatever the equivalent of set is in your environment-->
        flask run <!--there may be an error telling you FLASK_APP or FLASK_ENV has not been set, I struggled and could only repeat the those commands until it worked -->
        ctrl+click the address
            username = admin
            password = password
        logging in directs you to the /mood
            to get streaks for each user go to /mood/<name>
    To POST
        I used Postman Agent.
        OR
        exit run with ctrl+c
        in the terminal:
            python
            from application import db
            from application import Mood
            db.session.add(Mood(id=0,name="",mood=0,date=datetime.date(year, month, day))) <!--add everything you wish before committing-->
            db.session.commit()
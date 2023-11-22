import json
import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import IntegrityError

secret_key = os.urandom(16)
app = Flask(__name__)
app.secret_key = secret_key

dir_path = os.path.dirname(os.path.realpath(__file__))

with open (os.path.join(dir_path,'secrets.json')) as f:
    secrets= json.load(f)['mysqlCredentials']

def get_db_connection():
    return mysql.connector.connect(
        host=secrets['host'],
        user=secrets['user'],
        password=secrets['password'],
        port=secrets['port'],
        database=secrets['db']
    )
# Home Page

@app.route('/')
def home():
    return render_template('HOME.html')

# Participants Page
@app.route('/participants', methods=['GET', 'POST'])
def show_participants():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        skill_level = request.form['skill_level']
        age = request.form['age']
        life_insurance = 0 # default value
        query = "INSERT INTO Participants (Name, Skill, Age, LifeInsurance) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, skill_level, age, life_insurance))
        connection.commit()

    # Fetch and display all adventurers
    cursor.execute("SELECT Name, Skill, Age, ID FROM Participants")
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('PARTICIPANTS.html', data=data)

# implement the update route for the participant table
@app.route('/update/<int:id>', methods=['GET','POST'])
def update_adventurer(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # POST request : Update the data
    if request.method == 'POST':
        name = request.form['name']
        skill_level = request.form['skill_level']
        age = request.form['age']
        query = "UPDATE Participants SET Name = %s, Skill = %s, Age = %s WHERE ID = %s"
        cursor.execute(query, (name, skill_level, age, id))
        connection.commit()
        return redirect(url_for('show_participants'))
    
    # GET request ; Fetch existing data and display in a form
    cursor.execute("SELECT Name, Skill, Age FROM Participants WHERE ID = %s", (id,))
    adventurer = cursor.fetchone()
    cursor.close
    connection.close
    return render_template('uPARTICIPANTS.html', adventurer=adventurer, id=id)

# implement the delete route for participant table
@app.route('/delete/<int:id>')
def delete_adventurer(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Participants WHERE ID = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('show_participants'))

# Location Page
@app.route('/locations', methods=['GET', 'POST'])
def show_locations():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        location_name = request.form['location_name']
        region = request.form['region']
        altitude_in_feet = request.form['altitude_in_feet']

        query = "INSERT INTO Location (LocationName, Region, AltitudeInFeet) VALUES (%s, %s, %s)"
        cursor.execute(query, (location_name, region, altitude_in_feet))
        connection.commit()

    cursor.execute("SELECT LocationName, Region, AltitudeInFeet, ID FROM Location")
    locations = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('LOCATIONS.html', locations=locations)

# esatablish update capabilities for location table
@app.route('/location/update/<int:id>', methods=['GET','POST'])
def update_location(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # POST request to update the data
    if request.method == 'POST':
        location_name = request.form['location_name']
        region = request.form['region']
        altitude_in_feet = request.form['altitude_in_feet']
        query = "UPDATE Location SET LocationName = %s, Region = %s, AltitudeInFeet = %s WHERE ID = %s"
        cursor.execute(query, (location_name, region, altitude_in_feet, id))
        connection.commit()
        return redirect(url_for('show_locations'))
    
    #GET request to fetch existing data to pre-fill the form
    cursor.execute("SELECT LocationName, Region, AltitudeInFeet FROM Location WHERE ID = %s", (id,))
    location =cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('uLOCATIONS.html', location=location, id=id)

# Delete from Location Table
@app.route('/locations/delete/<int:id>')
def delete_location(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Location WHERE ID = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('show_locations'))

# Activity Page
@app.route('/activities', methods=['GET', 'POST'])
def show_activities():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        activity_name = request.form['activity_name']
        difficulty_level = request.form['difficulty_level']

        query = "INSERT INTO Activity (ActivityName, DifficultyLevel) VALUES (%s, %s)"
        cursor.execute(query, (activity_name, difficulty_level))
        connection.commit()

    cursor.execute("SELECT ID, ActivityName, DifficultyLevel FROM Activity")
    activities = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('ACTIVITIES.html', activities=activities)

# Update capabilities for activity table
@app.route('/activities/update/<int:id>', methods=['GET','POST'])
def update_activity(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # POST request to update the data
    if request.method == 'POST':
        activity_name = request.form['activity_name']
        difficulty_level = request.form['difficulty_level']
        query = "UPDATE Activity SET ActivityName = %s, DifficultyLevel = %s WHERE ID = %s"
        cursor.execute(query, (activity_name, difficulty_level, id))
        connection.commit()
        return redirect(url_for('show_activities'))
    
    #GET request to fetch existing data to pre-fill the form
    cursor.execute("SELECT ActivityName, DifficultyLevel FROM Activity WHERE ID = %s", (id,))
    activity =cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('uACTIVITIES.html', activity=activity, id=id)

# Delete from Activity Table
@app.route('/activities/delete/<int:id>')
def delete_activity(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Activity WHERE ID = %s", (id,))
        connection.commit()
    except IntegrityError:
        # Handle the error by redirecting to an error page or showing a message
        # Here, we'll just flash a message and redirect back to the activities page
        flash("This activity can't be deleted right now because it is logged in the AdventureLog.")
        return redirect(url_for('show_activities'))

    cursor.close()
    connection.close()
    return redirect(url_for('show_activities'))




if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")


'''
# define the route for '/second_page', handling POST requests
@app.route('/second_page', methods=['POST'])
def second_page():
    print(request.form)
    name = request.form['name']
    skill_level = request.form['skill_level']
    age = request.form['age']
    life_insurance = 0 # default value for all entries
    #connect to the database and insert data
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO Participants (Name, Skill, Age, LifeInsurance) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, skill_level, age, life_insurance))
    connection.commit()
    cursor.close()
    connection.close()

   # return "data insterted"
    
    #now fetch the data to display in the table
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Name, Skill, Age FROM Participants")
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('second_page.html', data=data)
    
   # return "This is the second page"

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
'''
'''
app = Flask(__name__)

@app.route('/')
def first_page():
    return render_template('first_page.html')

@app.route('/second_page', methods=['POST'])
def second_page():
    name = request.form['name']
    skill_level = request.form['skill_level']
    age = request.form['age']
    return render_template('second_page.html', name=name, skill_level=skill_level, age=age)

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
'''
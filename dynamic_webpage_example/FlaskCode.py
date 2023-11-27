import json
import os
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import IntegrityError
from datetime import datetime, date

# secret_key = os.urandom(16)
app = Flask(__name__)
app.secret_key = 'your_mom_said_stay_static'

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
    connection = get_db_connection()
    cursor = connection.cursor()
    # Show the adventure log
    query= """SELECT 
        AdventureLog.ID, 
        AdventureLog.Date,
        AdventureLog.Time,
        Location.LocationName, 
        Activity.ActivityName, 
        GROUP_CONCAT(DISTINCT Participants.Name ORDER BY Participants.Name ASC SEPARATOR ', ') AS ParticipantsNames
    FROM AdventureLog
    JOIN Location ON AdventureLog.LocationID = Location.ID
    JOIN Activity ON AdventureLog.ActivityID = Activity.ID
    LEFT JOIN AdventureLog_Participant ON AdventureLog.ID = AdventureLog_Participant.LogID
    LEFT JOIN Participants ON AdventureLog_Participant.ParticipantID = Participants.ID
    GROUP BY AdventureLog.ID, AdventureLog.Date, AdventureLog.Time, Location.LocationName, Activity.ActivityName
   """

    cursor.execute(query)
    adventure_logs = cursor.fetchall()

    # define formatted_log here to collect the formatted log entries
    formatted_logs = []
    for log in adventure_logs:
        # check if the date is already a datetime.date object
        if isinstance(log[1], date):
            formatted_date = log[1].strftime('%m-%d-%Y')
        else:
            # if its a string, convert to date object then format
            formatted_date = datetime.strptime(log[1], '%Y-%m-%d').strftime('%m-%d-%Y')
        # create a new tuple with the formatted date and the rest of the log date
        formatted_log_entry = (log[0], formatted_date) + log[2:]
        formatted_logs.append(formatted_log_entry)

    cursor.close()
    connection.close()
    # pass the formatted logs to the template
    return render_template('HOME.html', adventure_logs=formatted_logs)

# Adventure Log
# Adventure Log page 

@app.route('/new_adventure')
def new_adventure():
    connection = get_db_connection()
    cursor = connection.cursor()

    # fetch participants
    cursor.execute("SELECT ID, Name FROM Participants")
    participants = cursor.fetchall()

    # fetch locations
    cursor.execute("SELECT ID, LocationName FROM Location")
    locations = cursor.fetchall()

    # fetch activities
    cursor.execute("SELECT ID, ActivityName FROM Activity")
    activities = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('uADVENTURE_LOG.html', participants=participants, locations=locations, activities=activities)

# Adventure Log
# / Create Adventure Log
@app.route('/create_adventure_log', methods=['POST'])
def create_adventure_log():
    # This function will handle creating a new Adventure Log entry
    # with the provided participant, location, activity, date, and time
    connection = get_db_connection()
    cursor = connection.cursor()

    # Extract the form data
    participant_ids = request.form.get('participant') # this will be a list if multiple participants are selected
    location_id = request.form.get('location')
    activity_id = request.form.get('activity')
    date = request.form.get('date')
    time = request.form.get('time')
    duration_in_hours = request.form.get('duration_in_hours')

    # Construct and execute the sql query to insert a new AdventureLog entry
    try:
        adventure_log_query = """
            INSERT INTO AdventureLog (Date, Time, LocationID, ActivityID, DurationInHours)
            VALUES (%s, %s, %s, %s, %s)
            """
        print("executing SQL query:", adventure_log_query)
        print("with parameters:", (date, time, location_id, activity_id, duration_in_hours))

        cursor.execute(adventure_log_query, (date, time, location_id, activity_id, duration_in_hours))
        adventure_log_id = cursor.lastrowid

        if not isinstance(participant_ids, list):
            participant_ids = [participant_ids]

        for participant_id in participant_ids:
            participant_id = int(participant_id) # ensure participant_id is an integer
            adventure_log_participant_query = """
                INSERT INTO AdventureLog_Participant (LogID, ParticipantID)
                VALUES (%s, %s)
            """
            cursor.execute(adventure_log_participant_query, (adventure_log_id, participant_id))
        
        connection.commit()
        flash('New Adventure Log enrty created successfully')

    except Exception as e:
        # if an error occurs, rollback the transaction and flash an error message
        connection.rollback()
        flash('An error occured while creating this Adventure Log entry: ' + str(e))
    finally: 
        cursor.close()
        connection.close()
    return redirect(url_for('new_adventure'))

# Adventure Log
# delete adventure log
@app.route('/delete_adventure_log/<int:log_id>')
def delete_adventure_log(log_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # First, delete associated entries in AdventureLog_Participant
        cursor.execute("DELETE FROM AdventureLog_Participant WHERE LogID = %s", (log_id,))

        # Then, delete the AdventureLog entry
        cursor.execute("DELETE FROM AdventureLog WHERE ID = %s", (log_id,))

        connection.commit()
        flash('Adventure Log entry deleted successfully')
        
    except Exception as e:
        connection.rollback()
        flash('An error occurred while deleting this Adventure Log entry: ' + str(e))
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('home'))


# Participants
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

# update
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

# delete
# implement the delete route for participant table

@app.route('/delete/<int:id>')
def delete_adventurer(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Participants WHERE ID = %s", (id,))
        connection.commit()
    except IntegrityError:
        # This block will run if a foreign key constraint prevents deletion
        flash('This Participant cannot be deleted because they are linked to one or more AdventureLogs!')
    except Exception as e:
        # this block will run for any other kind of unexpected database errors
        flash('An unexpected error occured: '+ str(e))
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('show_participants'))

# Location
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

# update
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

# delete
# Delete from Location Table

@app.route('/locations/delete/<int:id>')
def delete_location(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Location WHERE ID = %s", (id,))
        connection.commit()
    except IntegrityError:
        # This block will run if a foreign key constraing prevents deletion
        flash('This Location cannot be  deleted because it is linked to one or more AdventureLogs!')
    except Exception as e:
        # This block will run for any other kinds of unexpected errors
        flash('An unexpected error occured: ' + str(e))
    finally:
        cursor.close()
        connection.close()
    
    return redirect(url_for('show_locations'))

# Activity
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

# update
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

# delete
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
    except Exception as E:
        # this block will run for any other kind of unexpected database error
        flash('An unexpected error occured: ' + str(e))
    finally:
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
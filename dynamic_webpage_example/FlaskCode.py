import json
import os
import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

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
# define the root url route
@app.route('/')
def index():
    return render_template('first_page.html')
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
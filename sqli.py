#!/usr/bin/python3

from flask import Flask, render_template, request
import mysql.connector, os


app = Flask(__name__)


@app.route('/', methods=['GET'])
def showTable():
    """This is vulnerable to the following SQL injection:
    http://localhost:8000/?id=1' or 1=1 --%20"""
    connection = mysql.connector.connect(
        host="localhost",
        user="Ken",
        password="Ken",
        db="speakers"
    )
    mycursor = connection.cursor()

    id = request.args.get('id')
    

    # Fetch the value from the table with a matching ID

    # Here is the change. we are using a parameterized statement to hold the 
    # place of input. it is telling python to "just look at this as input"
    # nothing more, not sql, not html, just assume this is text.

    sqlstring = "Select * from speakers where id= %s"
    print(sqlstring)
    # here i dont really understand, but I know it needs a tuple
    # to work correctly? so i pass in the string we just made, with the
    # place holder %s as the search parameter.
    mycursor.execute(sqlstring, (id,))

    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    output = "<br />\n".join([str(row) for row in myresult])
    return output


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")
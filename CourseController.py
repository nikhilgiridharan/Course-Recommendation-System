from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "****",
    "password": "**********",
    "database": "coursecatalog"
}

@app.route("/")
def entry():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Execute a SELECT query
    query = "SELECT * FROM subjects"
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template("courseSelection.html", subjects=rows)


@app.route("/search", methods=['POST'])
def search():
    searchtext = request.form['courseSearch']
    # Create a connection
    connection = mysql.connector.connect(**db_config)

    # Create a cursor
    cursor = connection.cursor()

    # Execute a SELECT query
    query = "SELECT * FROM courses WHERE courseSubject = %s"
    args = searchtext,
    cursor.execute(query, args)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    for row in rows:
        print(row)

    return render_template("searchResults.html", courses=rows)

@app.route("/teacherSearch", methods=['GET'])
def searchTwo():
    searchtext = request.args.get('courseId')
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM coursecatalog.teachers WHERE courseId = %s";
    args = searchtext,
    cursor.execute(query, args)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    for row in rows:
        print(row)
    return render_template("teacherRatings.html", teachers=rows)

if __name__ == "__main__":
    app.run(debug=True)

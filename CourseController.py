from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "",
    "user": "",
    "password": "",
    "database": "coursecatalog"
}
subCategories = {}
courses = {}


@app.route("/")
def entry():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Execute a SELECT query
    query = "SELECT * FROM subjects"
    cursor.execute(query)

    # Fetch all rows
    global subCategories
    subCategories= cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return render_template("courseSelection.html", subjects=subCategories)


@app.route("/search", methods=['POST', 'GET'])
def search():
    global courses
    if request.method == 'GET':
        sortOption = request.args.get('sort')
        if sortOption == 'difficultyHighLow':
            sortedCourses = sorted(courses, key=lambda x: x[3], reverse=True)
        elif sortOption == 'difficultyLowHigh':
            sortedCourses = sorted(courses, key=lambda x: x[3])
        elif sortOption == 'teacherQualityHighLow':
            sortedCourses = sorted(courses, key=lambda x: x[4], reverse=True)
        elif sortOption == 'teacherQualityLowHigh':
            sortedCourses = sorted(courses, key=lambda x: x[4])
        else:
            # Default sorting or no sorting
            sortedCourses = courses
    else:
        args = {}
        searchSubject = request.form['subjectCategory']
        searchText = request.form['searchText']
        # Create a connection
        connection = mysql.connector.connect(**db_config)

        # Create a cursor
        cursor = connection.cursor()

        # Execute a SELECT query
        query = ("SELECT courses.courseId, courses.CourseName, teachers.TeacherName, " +
                 "teachers.difficulty, teachers.teacherQuality " +
                 "FROM courses INNER JOIN teachers ON courses.courseId = teachers.courseId ")

        if searchSubject != "":
            query = query + "AND courses.courseSubject = %(subject)s"
            args['subject'] = searchSubject
        if searchText != "":
            query = query + "AND (courses.courseName like %(text)s  OR courses.courseId like %(text)s)"
            args['text'] = "%" + searchText + "%"

        cursor.execute(query, args)

        # Fetch all rows
        courses = cursor.fetchall()

        cursor.close()
        connection.close()

        for row in courses:
            print(row)
        sortedCourses = courses
    global subCategories
    return render_template("courseSelection.html", courses=sortedCourses,  subjects=subCategories)


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

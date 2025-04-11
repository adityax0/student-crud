from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'host': 'suranardsdemo.cdtqd6jgia7i.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'test1234',
    'database': 'mysqldemo'
}


@app.route('/')
def home():
    return render_template('students.html')


@app.route('/students')
def view_students():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            students= cursor.fetchall()
    finally:
        connection.close()
    return render_template('view_students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact= request.form['contact']       
        section = request.form["section"]
        college = request.form['college']
        


        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (name, email, contact_number, section, collage ) VALUES (%s,  %s,%s,  %s,%s)"
                cursor.execute(sql, (name, email,  contact, section, college ))
            connection.commit()
        finally:
            connection.close()

        return redirect(url_for('view_students'))
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    
    connection = pymysql.connect(**db_config)

    if request.method == 'GET':
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
            student= cursor.fetchone()
            print("student::",student)
        return render_template('edit_customer.html', student=student)
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                name = request.form['name']
                email = request.form['email']
                contact= request.form['contact']       
                address = request.form['address']       
                section = request.form["section"]
                college = request.form['college']
 
                sql = "UPDATE students SET name=%s, email=%s, contact_number=%s, address=%s, section=%s, college=%s WHERE id=%s"
                cursor.execute(sql, (name, email, contact,address, section, college , id))
                connection.commit()
                return redirect(url_for('view_students'))
            else:
                cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
                student= cursor.fetchone()
                print("student::",student)
    finally:
        connection.close()
    return render_template('edit_student.html', student=student)
    

@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_customer(id):
    print("delete student::",id)
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id=%s", (id,))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('view_students'))




if __name__ == '__main__':
    app.run(port=5000, debug=True,host='0.0.0.0')

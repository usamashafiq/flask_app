#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2-binary 
import psycopg2.extras
 
app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"
 
DB_HOST = "localhost"
DB_NAME = "student_db"
DB_USER = "postgres"
DB_PASS = "123"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)
 
@app.route('/add_student', methods=['POST'])
def add_student():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        roll = request.form['roll']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        gender = request.form['gender']
        nationality = request.form['nationality']
        phone = request.form['phone']
        cur.execute("INSERT INTO students (roll,fname, lname, email,gender,nationality,phone) VALUES (%s,%s,%s,%s,%s,%s,%s)", (roll,fname, lname, email,gender,nationality,phone))
        conn.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))
 
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        roll = request.form['roll']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        gender = request.form['gender']
        nationality = request.form['nationality']
        phone = request.form['phone']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE students
            SET   roll = %s,
                 fname = %s,
                lname = %s,
                email = %s,
                gender = %s,
                nationality = %s,
                phone = %s
            WHERE id = %s
        """, (roll,fname, lname, email,gender,nationality,phone,id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    conn.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)
# </string:id></id></id>
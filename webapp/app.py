from flask import Flask, render_template, request, Blueprint
import sqlite3

app = Flask(__name__)

DB = "mienfoo.db"

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
@app.route('/index.html', methods = ['POST', 'GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select * from words")
    rows = cur.fetchall();
    return render_template('index.html', rows=rows)

@app.route('/create')
def new_word():
    ...
   #return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         name = request.form['name']
         definition = request.form['definition']
         with sql.connect(DB) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from students")
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0', port=3141)


from flask import Flask, render_template, json, request
import sqlite3


app = Flask(__name__)
con = sqlite3.connect('example.db', check_same_thread=False)
cur = con.cursor()


def initDB():
    try:
        # Create table
        cur.execute('''CREATE TABLE family (name text,age int)''')

    except:
        print("table already exist")

    # Save (commit) the changes
    con.commit()


initDB()


@app.route('/addtodb', methods=['GET', 'POST'])
def addToDB():
    # handle the POST request - run second
    if request.method == 'POST':
        femName = request.form.get('femName')
        femAge = request.form.get('femAge')
        sqlStr = f"INSERT INTO family VALUES ('{femName}',{int(femAge)})"
        print(sqlStr)
        cur.execute(sqlStr)
        con.commit()
        return render_template('index.html')
    # run first
    else:
        return render_template('addToDB.html')


@app.route('/showDB')
def showDB():
    SQL = "SELECT *  FROM family"
    cur.execute(SQL)
    res = []
    for i in cur:
        res.append({"name": i[0], "age": i[1]})
    return render_template('showDB.html', jsonDB=json.dumps(res))


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    myname = request.args.get('name')
    return render_template('about.html', name=myname)


@app.route('/contact', methods=['get'])
def contact():
    myname = request.args.get('name')
    return render_template('contact.html', name=myname)


if __name__ == '__main__':
    app.run(debug=True, port=9000)

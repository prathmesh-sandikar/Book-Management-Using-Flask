from flask import Flask, render_template,request,session
from flask_session import Session

import sqlite3

from werkzeug.utils import redirect

app1 = Flask(__name__)
app1.config["SESSION_PERMANENT"] = False
app1.config["SESSION_TYPE"] = "filesystem"
Session(app1)

con = sqlite3.connect("bookmngsys.db",check_same_thread=False)

listOfTables1 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOKS' ").fetchall()

if listOfTables1!=[]:
    print("Table 1 Exists ! ")

else:
    con.execute(''' CREATE TABLE BOOKS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    BOOKNAME TEXT,
    AUTHOR TEXT,
    CATEGORY TEXT,
    PRICE TEXT,
    PUBLISHER TEXT); ''')
    print("Table has created")

listOfTables2 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='USERBOOKS' ").fetchall()

if listOfTables2!=[]:
    print("Table 2 Exists ! ")

else:
    con.execute(''' CREATE TABLE USERBOOKS(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    UNAME TEXT,
    UMOBNO TEXT,
    UEMAIL TEXT,
    UADDRESS TEXT,
    UPASSWORD TEXT); ''')
    print("Table has created")

cur2 = con.cursor()
cur2.execute("SELECT UEMAIL,UPASSWORD FROM USERBOOKS")
res2 = cur2.fetchall()
print(res2)


@app1.route("/")
def home():
    return render_template("home.html")


@app1.route("/adminlogin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUname = request.form["username"]
        getppass = request.form["password"]

        if getUname == "admin":
            if getppass == "9875":
                return redirect("/bookentry")
    return render_template("login.html")


@app1.route("/bookentry", methods=["GET", "POST"])
def entry():
    if request.method == "POST":
        getBookName = request.form["name"]
        getAuthor = request.form["author"]
        getCategory = request.form["cat"]
        getPrice = request.form["price"]
        getPublisher = request.form["pub"]
        print(getBookName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)
        try:
            con.execute("INSERT INTO BOOKS(BOOKNAME,AUTHOR,CATEGORY,PRICE,PUBLISHER) VALUES('"+getBookName+"','"+getAuthor+"','"+getCategory+"','" +getPrice+"','"+getPublisher+"')")
            print("successfully inserted !")
            con.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)
    return render_template("bookentry.html")


@app1.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getBOOKName = request.form["bname"]
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM BOOKS WHERE BOOKNAME = '"+getBOOKName+"' ")
        res2 = cur2.fetchall()
        return render_template("viewall.html", bookss=res2)
    return render_template("search.html")


@app1.route("/edit", methods=["GET","POST"])
def edit():
    if request.method == "POST":
        getNewname = request.form["newname"]
        getNewAuthor = request.form["newauthor"]
        getNewCategory = request.form["newcat"]
        getNewPrice = request.form["newprice"]
        getNewPublisher = request.form["newpub"]
        con.execute("UPDATE BOOKS SET BOOKNAME = '"+getNewname+"',AUTHOR = '"+getNewAuthor+"',CATEGORY ='"+getNewCategory+"',PRICE = '"+getNewPrice+"',PUBLISHER = '"+getNewPublisher+"'  ")
        print("successfully Updated !")
        con.commit()
        return redirect("/viewall")
    return render_template("edit.html")


@app1.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        getNAMEDEL = request.form["namedel"]
        cur3 = con.cursor()
        cur3.execute("DELETE FROM BOOKS WHERE BOOKNAME = '"+getNAMEDEL+"' ")
    return render_template("delete.html")


@app1.route("/viewall")
def view():
    cur = con.cursor()
    cur.execute("SELECT * FROM BOOKS")
    res = cur.fetchall()
    return render_template("viewall.html", bookss=res)


@app1.route("/cardview")
def cardview():
    cur3 = con.cursor()
    cur3.execute("SELECT * FROM BOOKS")
    res6 = cur3.fetchall()
    return render_template("cardview.html", books3=res6)


@app1.route("/userreg", methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        getUName = request.form["usname"]
        getUmobno = request.form["mobileno"]
        getEmail = request.form["email"]
        getAdd = request.form["address"]
        getPass = request.form["pass"]
        con.execute("INSERT INTO USERBOOKS(UNAME,UMOBNO,UEMAIL,UADDRESS,UPASSWORD) VALUES('" + getUName + "','" + getUmobno + "','" + getEmail + "','" + getAdd + "','" + getPass + "')")
        print("successfully inserted !")
        con.commit()
        return redirect("/userlogin")
    return render_template("regis.html")


@app1.route("/userview")
def usview():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        cur = con.cursor()
        cur.execute("SELECT * FROM BOOKS")
        res = cur.fetchall()
        return render_template("userview.html", bookss=res)


@app1.route("/userlogin", methods=["GET", "POST"])
def ulog():
    if request.method == "POST":
        getuseremail = request.form["Uname"]
        getuserpass = request.form["Upass"]
        print(getuseremail)
        print(getuserpass)
        cur2 = con.cursor()
        cur2.execute("SELECT * FROM USERBOOKS WHERE UEMAIL = '"+getuseremail+"' AND UPASSWORD = '"+getuserpass+"'")
        res2 = cur2.fetchall()
        if len(res2) > 0:
            for i in res2:
                getName = i[1]
                getid = i[0]

            session["name"] = getName
            session["id"] = getid

            return redirect("/userview")
    return render_template("userlogin.html")


@app1.route("/usersearch", methods=["GET", "POST"])
def ussearch():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        if request.method == "POST":
            getBOOKName = request.form["ubname"]
            cur2 = con.cursor()
            cur2.execute("SELECT * FROM BOOKS WHERE BOOKNAME = '" + getBOOKName + "' ")
            res2 = cur2.fetchall()
            return render_template("userview.html", bookss=res2)
        return render_template("usersearch.html")


@app1.route("/userlogout", methods=["GET", "POST"])
def uslogout():

    if not session.get("name"):
        return redirect("/userlogin")
    else:
        session["name"] = None
        return redirect("/")


if __name__ == "__main__":
    app1.run()
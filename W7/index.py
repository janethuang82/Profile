from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import mysql.connector
app=Flask(__name__)
app.secret_key=b'\xa8\x90\xba\x9e\x95\xbfh\x15\xee:\x14;'


mydatabase = mysql.connector.connect(
    host = "127.0.0.1",
    username = "root",
    
    database = "website"
)

mycursor = mydatabase.cursor()


@app.route("/")
def index():
    return render_template("signin.html")
    

@app.route("/signup",methods=["POST"])
def signup():

    mycursor.execute (f"SELECT * FROM user where username ='{request.values['username']}'")
    signup_table = mycursor.fetchone()

    if signup_table:
        return redirect("/error/?message=帳號已被註冊過")
    else:
        sql = "INSERT INTO user (name, username, password) VALUES (%s, %s, %s)"
        val = (str(request.values["name"]),str(request.values["username"]),str(request.values["password"]))
        mycursor.execute(sql.val)
        mydatabase.commit()
        return render_template("signin.html")
        

@app.route("/member")
def member():
    if session.get("username"):
        return render_template("member.html",titlename = session["name"])
    else:
        return redirect("/")
    
@app.route("/error／")
def error():
    msg = request.args.get("message")
    return render_template("error.html")
   
@app.route("/signin",methods=["POST"])
def signin():
    session["username"] = request.values["username"] 
    session["password"] = request.values["password"]

    mycursor.execute(f"SELECT * FROM user where username='{request.form['username']}'")
    signin_table = mycursor.fetchone()

    if signin_table[2] == request.values["username"] and signin_table[3] == request.values["password"]:
        session["name"] = signin_table[1]
        return redirect("/member")
    else:
        return redirect("/error/?message=帳號或密碼錯誤")

    
@app.route("/signout")
def signout():
    session.pop("user", None)
    return redirect(url_for("index"))
    

@app.route("/api/user")
def finding():

    finding_name = request.args.get("username", None)
    mycursor.execute(f"SELECT * from user where username ='{finding_name}'")

    finding_table = mycursor_fetchone()

    if finding_table is None:
    
        dic = {}
        dic['data'] = "null"
        return json.dumps(dic, ensure_ascii=False)

    else:
        dic = {}

        id = finding_table[0]
        name = finding_table[1]
        username = finding_table[2]

        dic['data'] = {'id': id, 'name': name, 'username': username}
        return json.dumps(dic, ensure_ascii = False)


    app.run(port='3000')

from flask import Flask,render_template,session,redirect,request,flash
import mysql.connector
app=Flask(__name__)
con=mysql.connector.connect(host="localhost",user="root",password="yash" ,database="chat",auth_plugin='mysql_native_password')
cursor=con.cursor()
app.secret_key="super-secret-key"
@app.route('/login',methods=["GET","POST"])
def login():
    if (request.method == "POST"):
        username = request.form.get('uname')
        password = request.form.get('pass')
        cursor.execute("""SELECT * FROM `auth` WHERE `uname` LIKE '{}' AND `pwd` LIKE '{}'""".format(username, password))
        users = cursor.fetchall()

        if (len(users)>0):
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
@app.route('/signup',methods=["GET","POST"])
def signup():
    if (request.method == "POST"):
        username = request.form.get('uname')
        password = request.form.get('pass')
        cursor.execute("""SELECT * FROM `auth` WHERE `uname` LIKE '{}' AND `pwd` LIKE '{}'""".format(username, password))
        users = cursor.fetchall()
        if(len(users)>0):
            flash('Login into existing account')
            session['user'] = username
            return redirect('/')
        cursor.execute(
            """SELECT * FROM `auth` WHERE `uname` LIKE '{}'""".format(username))
        users = cursor.fetchall()
        if (len(users) > 0):
            flash('User already exists , try another username')
            return redirect('/signup')
        cursor.execute("""Insert into `auth` (`uname`,`pwd`) values('{}','{}')""".format(username, password))
        
        con.commit()
        session['user'] = username
        return redirect('/')

    return render_template('signup.html')
@app.route('/')
def home():
    
    if ('user' in session):
        cursor.execute("""SELECT * FROM `chats`""")
        cHs = cursor.fetchall()
        return render_template("index.html",cHs=cHs,us=session['user'])
    else :
         return redirect('/login')
@app.route('/pass',methods=["POST","GET"])
def mspass():
    usr=session['user']
    msg=request.form.get('msg')
    cursor.execute(
            """INSERT INTO `chats` (`uname`,`msg`) values('{}','{}')""".format(usr,msg))
    con.commit()
    return redirect('/')

@app.route('/del/<string:sno>',methods=["POST","GET"])
def delmess(sno):
    cursor.execute("""DELETE FROM `chats` WHERE `sno` LIKE '{}'""".format(sno))
    con.commit()
    return redirect('/')
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/login')
app.run(debug=True)
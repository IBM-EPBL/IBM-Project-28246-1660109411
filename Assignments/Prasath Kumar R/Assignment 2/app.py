from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from markupsafe import escape
from os import urandom


conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.clou;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=bqw81992;PWD=fEqs8mKciKoCvTJ;",'','')

app=Flask(__name__)
app.secret_key=urandom(24)

@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        sqll= f"SELECT username, password from user_login where username= '{escape(username)}'"
        stmt=ibm_db.exec_immediate(conn,sqll)
        dictionary=ibm_db.fetch_assoc(stmt)
        if dictionary:
            while dictionary != False:
                db_username=dictionary['USERNAME']
                db_password=dictionary['PASSWORD']
                dictionary=ibm_db.fetch_assoc(stmt)

            if username==db_username and password==db_password:
                session['login_status']=True
                session['username']=username
                return render_template("index.html",msg=username)
            else:
                return render_template("login.html",msg="Login Invalid")
        else:
            return render_template("login.html",msg="Login Invalid")

    
    
    return render_template("login.html")

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=='POST':
        username_reg=request.form['username']
        password_reg=request.form['password']
        email_reg=request.form['email']

        sqlr="SELECT * from user_login WHERE username=?"
        stmt=ibm_db.prepare(conn,sqlr)
        ibm_db.bind_param(stmt,1,username_reg)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)

        if account:
            render_template('login.html',msg="You are already a member.")
        else:
            sqlreg="INSERT into user_login VALUES (?,?,?)"
            prep_stmt=ibm_db.prepare(conn,sqlreg)
            ibm_db.bind_param(prep_stmt,1,username_reg)
            ibm_db.bind_param(prep_stmt,2,password_reg)
            ibm_db.bind_param(prep_stmt,3,email_reg)
            ibm_db.execute(prep_stmt)
        return render_template("login.html",msg="Account Created. Login Now!!")
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('login_status',None)
    session.pop('username',None)
    username=""
    passsword=""
    return redirect(url_for('login'))
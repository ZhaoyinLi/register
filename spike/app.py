from flask import Flask, render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.sql import select
from sqlalchemy.orm import scoped_session,sessionmaker
from passlib.hash import sha256_crypt
import pymysql

engine= create_engine("mysql+pymysql://root:12345678@localhost/me5")
conn = engine.connect()
                     #(mysql+pymysql://root:12345678@localhost/databasename)
db=scoped_session(sessionmaker(bind=engine))
username = ""
app=Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

# register form
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name = request.form.get("name")
        global username
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        favclass = request.form.get("favclass")
        goal = request.form.get("goal")
        fun = request.form.get("fun")
        other = request.form.get("other")
        interest = request.form.get("interest")
        pic = request.form.get("pic")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute ( "INSERT INTO users(name,username,password,favclass,goal,fun,other,interest,pic) VALUES(:name,:username,:password,:favclass,:goal,:fun,:other,:interest,:pic)",
                                {"name":name,"username":username,"password":password,"favclass":favclass,"goal":goal,"fun":fun,"other":other,"interest":interest,"pic":pic})
            db.commit()
            return redirect(url_for('login'))
     
        else:
            flash("Password doesn't match","danger") 
            return render_template("register.html")

    return render_template("register.html")
#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password =request.form.get("password")

        usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        passworddata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()
        uid = db.execute("SELECT id FROM users WHERE username=:username",{"username":username}).fetchone()
        if usernamedata is None:
            flash("No username," "danger")
            return render_template("login.html")
        else:
            for passwor_data in passworddata:
                #if sha256_crypt.verify(password,passwor_data):
                if password==passwor_data:
                    session["log"]=True

                    flash("You are now login ","success")
                    # res = [int(i) for i in uid.split() if i.isdigit()]
                    res = str(uid).split(",")[0]
                    return redirect(url_for("photo", id=str(res[1])))
                else:
                     flash("incorrect password","danger")
                     return render_template("login.html")

    return render_template("login.html")



#photo

@app.route("/photo",methods=["GET","POST"])
def photo():
    id=str(request.args.get("id"))
    d={}
    if request.method=="GET":
        result = db.execute("SELECT username, name, password,favclass,goal,fun,other,interest FROM users WHERE id = " + id)
        for rowproxy in result:
            for col, val in rowproxy.items():
                d[col]=val
        return render_template("photo.html",usernamedata=d)
    if request.method=="POST":
        name = request.form.get("name")
        global username
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("password")
        favclass = request.form.get("favclass")
        goal = request.form.get("goal")
        fun = request.form.get("fun")
        other = request.form.get("other")
        interest = request.form.get("interest")
        secure_password = sha256_crypt.encrypt(str(password))
        db.execute ( "UPDATE users set name=:name,username=:username,password=:password,favclass=:favclass,goal=:goal,fun=:fun,other=:other,interest=:interest where id=:id",
                    {"name":name,"username":username,"password":password,"favclass":favclass,"goal":goal,"fun":fun,"other":other,"interest":interest,"id":id})
        db.commit()
        # usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
        # passworddata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()
        # favclassdata = db.execute("SELECT favclass FROM users WHERE username=:username",{"username":username}).fetchone()
        # goaldata = db.execute("SELECT goal FROM users WHERE username=:username",{"username":username}).fetchone()
        # fundata = db.execute("SELECT fun FROM users WHERE username=:username",{"username":username}).fetchone()
        # otherdata = db.execute("SELECT other FROM users WHERE username=:username",{"username":username}).fetchone()
        # interestdata = db.execute("SELECT interest FROM users WHERE username=:username",{"username":username}).fetchone()    
        flash("Edited","sucess")
        return redirect(url_for("photo", id=id))
    
#passworddata=passworddata,favclassdata=favclassdata,goaldata=goaldata,fundata=fundata,otherdata=otherdata,interestdata=interestdata
#logout
@app.route("/logout")
def logout():
    session.clear()
    flash("You are now log out","sucess")
    return redirect(url_for('login'))


if __name__=="__main__":
    app.secret_key="1234567dailywebcoding"
    app.run(debug=True)
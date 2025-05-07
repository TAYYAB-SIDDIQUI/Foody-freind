from flask import Flask,render_template,request,session,flash,redirect,url_for
import sqlite3
import datetime
import numpy as np
con=sqlite3.connect("Database/foodyfreind.db",check_same_thread=False)
cursor=con.cursor()
cursor.execute("""
create table if not exists orderstable(
                id int primary key,
                name text not null,
                location text not null,
                quantity int not null,
                contact int not null
               )
""")

cursor.execute("""
create table if not exists booktable (
                id int primary key,
                name text not null,
                Tablecount text not null,
                location text not null,
                date text not null,
                time text not null
               )
""")
signedin=0
app=Flask(__name__)
app.secret_key="tayyab1234"
@app.route("/home")
def index():
    user=session.get('username')
    st=session.get('status')
    veg=["Panner (Cottage cheese)","Tofu","Rajma","Chole","Palak Paneer","Dal Tadka","Aloo Gobi","Vegetable Pulao","Idli","Dosa",
     "Upma","Bhindi Masala (Okra)","Baigan Bharta","Sambar","Matar Paneer","khichdi","Veg Biryani","Moong Dal","Mixed Vegetable Curry",
     "Khandvi"]
    nonveg=["Butter Chicken","Chicken Biryani","Mutton Rogan Josh","Fish Curry","Egg Curry","Chicken Tikka","Prawn Masala",
        "Keema (Minced Meat)","Chicken 65","Grilled Chicken","Tanddori Chicken","Mutton Biryani","Fish Fry","Crab Curry",
        "Chicken Korma","Boiled Eggs","Omelette","Chicken Soup","Prawn Biryani","Tuna Sandwich"]
    veginfo=""
    for i in veg:
        code=f"<p>{i}</p>"
        veginfo=veginfo+code
    nonveginfo=""
    for i in nonveg:
        code=f"<p>{i}</p>"
        nonveginfo=nonveginfo+code
    if st==None:
        si="""<a href="/Signpage" style="position: fixed; right: 80px; text-decoration: none; color: White; font-size: 25px; top: 20px; cursor: pointer; z-index: 1001;">Sign In</a>"""
        si2=""
    if st==1:
        si=f"""<a href="/records" style="position: fixed; right: 80px; text-decoration: none; color: White; font-size: 25px; top: 20px; cursor: pointer; z-index: 1001;">{user}</a>"""
        si2="<li><a href='/logout'>Logout</a></li>"
    return render_template("home.html",status=si,veg=veginfo,nonveg=nonveginfo,logout=si2)

@app.route("/Signpage")
def signpage():
    return render_template("Signpage.html")

@app.route("/Signininfo", methods=["GET","POST"])
def Signs():
    username=request.form.get("Username")
    password=request.form.get("Password")
    cursor.execute("select * from userinfo where username=? and password=?",(username,password))
    data=cursor.fetchall()
    print(data[0][0])
    if username!=data[0][0]:
        print("invelid username or password")
        return render_template("Signpage.html")
    if password!=data[0][1]:
        print("invaid username or password")
        return render_template("Signpage.html")
    session["username"]=username
    session["status"]=1
    return redirect(url_for("index"))
@app.route("/Signupinfo")
def Signup():
    return render_template("Signuppage.html")

@app.route("/Signupinfo", methods=["GET","POST"])
def Signupinfo():
    username=request.form.get("Username")
    password=request.form.get("Password")
    conpass=request.form.get("ConPassword")
    if conpass==password:
        global conuser,cursoruser
        conuser=sqlite3.connect(f"Database/users/{username}.db",check_same_thread=False)
        cursoruser=conuser.cursor()
        cursoruser.execute("""
                create table if not exists orderstableuser(
                id int primary key,
                name text not null,
                location text not null,
                quantity int not null,
                contact int not null)
                """)
        cursoruser.execute("""
                create table if not exists booktableuser(
                id int primary key,
                name text not null,
                Tablecount text not null,
                location text not null,
                date text not null,
                time text not null)
                """)
        cursor.execute("""
            create table if not exists userinfo(
                       username varchar(30) unique not null,
                       password varchar(30) not null,
                       db varchar(50) unique not null)
    """)
        cursor.execute("insert into userinfo(username,password,db) values (?,?,?)",(username,password,f"{username}.db"))
        con.commit()
        session["username"]=username
        session["status"]=1
        return redirect(url_for("index"))
    else:
        return "nothing"
@app.route("/logout",methods=["GET","POST"])
def logout():
    session["status"]=None
    session["username"]=None
    return redirect(url_for("index"))
@app.route("/orderfunc", methods=["GET","POST"])
def order():
    foods=np.array(["Panner (Cottage cheese)","Tofu","Rajma","Chole","Palak Paneer","Dal Tadka","Aloo Gobi","Vegetable Pulao","Idli","Dosa",
     "Upma","Bhindi Masala (Okra)","Baigan Bharta","Sambar","Matar Paneer","khichdi","Veg Biryani","Moong Dal","Mixed Vegetable Curry",
     "Khandvi","Butter Chicken","Chicken Biryani","Mutton Rogan Josh","Fish Curry","Egg Curry","Chicken Tikka","Prawn Masala",
        "Keema (Minced Meat)","Chicken 65","Grilled Chicken","Tanddori Chicken","Mutton Biryani","Fish Fry","Crab Curry",
        "Chicken Korma","Boiled Eggs","Omelette","Chicken Soup","Prawn Biryani","Tuna Sandwich"])
    orderfoodlist=""
    for i in foods:
        option=f"<option value='{i}' style='color: white; background-color:grey;'>{i}</option>"
        orderfoodlist=orderfoodlist+option
    page=f"""<select name="food", id="food" style='margin-left: 5%; border-radius: 7.5px; font-size: 20px; padding: 0.25%; width: max-content;'>
                {orderfoodlist}
</select>"""
    return render_template("orderfood.html",foods=page)

@app.route("/bookfunc",methods=["GET","POST"])
def book():
    return render_template("book.html")

@app.route("/orderform",methods=["GET","POST"])
def orderdetail():
    name=request.form.get("food")
    quantity=int(request.form.get("quantityEnter"))
    location=request.form.get("Locationinfo")
    contact=int(request.form.get("Contactno"))
    details=[name,quantity,location,contact]
    cursor.execute("select COUNT(*) from orderstable")
    length=cursor.fetchone()[0]
    print(length)
    if length==0:
        id=f"o{1}"
    else:
        id=f"o{length+1}"
    username=session.get("username")
    if username==None:
        return render_template("Signpage.html")
    conuser=sqlite3.connect(f"Database/users/{username}.db")
    cursoruser=conuser.cursor()
    cursor.execute("insert into orderstable (id,name,quantity,location,contact) values (?,?,?,?,?)",(id,name,quantity,location,contact))
    con.commit()
    cursoruser.execute("insert into orderstableuser (id,name,quantity,location,contact) values (?,?,?,?,?)",(id,name,quantity,location,contact))
    conuser.commit()
    cursoruser.execute("select * from orderstableuser")
    rows=cursoruser.fetchall()
    for row in rows:
        print(row)
    cursor.execute("select * from orderstable")
    rows=cursor.fetchall()
    for row in rows:
        print(row)
    return f"""<p>Thank you! <br> Your order of {name} has been recieved we will send delivery at {location}.</p>"""

@app.route("/booking", methods=["GET","POST"])
def bookinginfo():
    name=request.form.get("name")
    phone=int(request.form.get("phoneno"))
    Table=request.form.get("Table")
    location=request.form.get("Location")
    dateinfo=request.form.get("dateinfo")
    timeinfo=request.form.get("timeinfo")
    cursor.execute("select COUNT(*) from booktable")
    length=cursor.fetchone()[0]
    print(length)
    if length==0:
        id=f"p{1}"
    else:
        id=f"p{length+1}"
    username=session.get("username")
    if username==None:
        return render_template("Signpage.html")
    conuser=sqlite3.connect(f"Database/users/{username}.db")
    cursoruser=conuser.cursor()
    cursor.execute("insert into booktable(id,name,tablecount,location,date,time) values (?,?,?,?,?,?)",(id,name,Table,location,dateinfo,timeinfo))
    con.commit()
    cursoruser.execute("insert into booktableuser(id,name,tablecount,location,date,time) values (?,?,?,?,?,?)",(id,name,Table,location,dateinfo,timeinfo))
    conuser.commit()
    cursor.execute("select * from booktable")
    rows=cursor.fetchall()
    for row in rows:
        print(row)
    cursoruser.execute("select * from booktableuser")
    rows=cursoruser.fetchall()
    for row in rows:
        print(row)
    details=[name,phone,Table,location,dateinfo,timeinfo]
    return f"""<p>Thank you {name}! <br> Your table has been booked for {Table} at {location} on {dateinfo} at {timeinfo}.</p>"""
@app.route("/records", methods=["GET","POST"])
def record():
    username=session.get("username")
    conuser=sqlite3.connect(f"Database/users/{username}.db")
    cursoruser=conuser.cursor()
    cursoruser.execute("select * from orderstableuser")
    Dataord=cursoruser.fetchall()
    html1,html2="",""
    for i in Dataord:
        ord=f"""
        <label>Order</label><br>
        <label>{i[1]}</label><br>
        <label>{i[2]}</label><br>
        <label>{i[3]}</label><br><br><hr><br>
        """
        html1=html1+ord
    cursoruser.execute("select * from booktableuser")
    databook=cursoruser.fetchall()
    for i in databook:
        book=f"""
        <label>book</label><br>
        <label>{i[1]}</label><br>
        <label>{i[2]}</label><br>
        <label>{i[3]}</label><br><br><hr><br>
        """
        html2=html2+book
    page=f"""<body style="display:flex; background-color:black; color:white; width:100%; justify-items:center; font-size:20px;">
                <section style='width:50%; justify-items:center; font-size:20px;'>{html1}</section>
                <section style='width:50%; justify-items:center; font-size:20px;'>{html2}</section>
            </body>
        """
    return  page
if __name__=="__main__":
    app.run(debug=True)
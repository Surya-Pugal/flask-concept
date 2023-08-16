from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "surya@2023$"

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config["SQLALACHEMY_TRACT_MODIFICATIONS"] = False
# app.permanent_session_lifetime = timedelta(days = 5)
app.permanent_session_lifetime = timedelta(minutes = 5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# @app.route("/<name>")
# def helloworld(name):
#     return render_template('index.html', content=name, r=2)

# @app.route("/index")
# def index():
#     return "<p>This is the index page</p>"

@app.route("/home")
def home():
    return render_template("home.html")

# @app.route("/string/<string:value>)")
# def string(value):
#     return f"<p>This is the string {value}</p>"

# @app.route("/<listname>")
# def user(listname):
#     return render_template("list.html", content=["abi", "sam", "arun"])

# @app.route("/admin")
# def admin():
#     return render_template("loop.html")

# @app.route("/<address>")
# def student_address(address):
#     return render_template("list.html", content=["chennai", "Kovai", "salem"])

# @app.route("/newinheritance")
# def newinheritance():
#     return render_template("newinheritance.html")


# @app.route("/test")
# def test():
#     return render_template("new.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         user = request.form["nm"]
#         return redirect(url_for("user", usr = user))
    
#     return render_template("login.html")

# @app.route("/<usr>")
# def user(usr):
#     return f"<h1>{usr}</h1>" 

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        
        found_user = users.query.filter_by(name=user).first()
        
        # more than one result return by this query.. use this code
        # found_user = users.query.filter_by(name=user).all()
        # If you want to delete one entry..use this code
        # found_user = users.query.filter_by(name=user).delete()
        # for deleting multiple objects
        # for user in found_user:
        #     user.delete()
        
        
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
            
        
        flash("Login Successful!")

        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
    return render_template("login.html")


# @app.route("/user")
# def user():
#     if "user" in session:
#         user = session["user"]
#         return render_template("user.html", user=user) 
#     else:
#         flash("you are not logged in!")
#         return redirect(url_for("login"))

@app.route("/user", methods=["POST","GET"])
def user():
    # email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved successfully")
        else:
            email = session.get("email", "")
            # if email in session:
            #     email = session["email"]
                
        return render_template("user.html", email=email) 
    else:
        flash("you are not logged in!")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

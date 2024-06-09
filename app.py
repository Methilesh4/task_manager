from flask import Flask, request, render_template,session
import pyrebase
import firebase_admin
from firebase_admin import credentials,db

firebaseConfig = {
  "apiKey": "AIzaSyDnr5layCizYdJhd6LYBQrfl_hSalFCaH8",
  "authDomain": "task-manager-6f3ab.firebaseapp.com",
  "projectId": "task-manager-6f3ab",
  "storageBucket": "task-manager-6f3ab.appspot.com",
  "messagingSenderId": "171082244368",
  "appId": "1:171082244368:web:d2ad1e321c955d74358595",
  "databaseURL":"https://task-manager-6f3ab-default-rtdb.firebaseio.com/"
};

firebase=pyrebase.initialize_app(firebaseConfig);
auth=firebase.auth()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# session(app)

cred=credentials.Certificate("task-manager-6f3ab-firebase-adminsdk-xldyc-55afa9f4d4.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://task-manager-6f3ab-default-rtdb.firebaseio.com/"})

ref=db.reference('/')
@app.route('/', methods=['GET', 'POST'])
def render():
    return  render_template("login.html")
@app.route('/signup', methods=['GET', 'POST'])
def render_signup():
     return  render_template("signup.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
        email=request.form["mail"]
        # session["email"]=email
        password=request.form["password"]
        doc_ref=ref.child("methilesh").get()
        print(doc_ref)
        # session["info"]=doc_ref
        try:

            login=auth.sign_in_with_email_and_password(email,password)
            return  render_template("index.html",info=doc_ref)
            # if doc_ref:
            #     return  render_template("index.html",info=jsonify(doc_ref))
            # else:
            #      return("database Error")
        except:
            res="wrong credentials!!!"
            return  render_template("login.html",result=res)
@app.route('/sign_up', methods=['GET', 'POST'])
def signup():
        email=request.form["mail"]
        password=request.form["password"]
        try:
            login=auth.create_user_with_email_and_password(email,password)
            return  render_template("login.html",result="Sucessfully created account now Login")
        except:
            res="Mail already Exist"
            return  render_template("signup.html",result=res)
@app.route('/update', methods=['GET', 'POST'])
def update():
     due=request.form["due"]
     time=request.form["time"]
     details=request.form["details"]
     tname=request.form["tname"]
     data={tname:{"details":details,"due":due,"time":time}}
    
     if(data):
        ref.child("methilesh").update(data)
        return render_template("index.html",info=ref.child("methilesh").get(),updation="Sucessfully Updated")
     else:
          return  render_template("index.html",updation="error Occured in updation")
if __name__ == '__main__':
    app.run(debug=True)

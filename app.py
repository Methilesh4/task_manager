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
app.secret_key = "abc" 


cred=credentials.Certificate("task-manager-6f3ab-firebase-adminsdk-xldyc-55afa9f4d4.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://task-manager-6f3ab-default-rtdb.firebaseio.com/"})

ref=db.reference('/users')
@app.route('/', methods=['GET', 'POST'])
def render():
   
        return  render_template("login.html")
@app.route('/signup', methods=['GET', 'POST'])
def render_signup():
      
        return  render_template("signup.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
        email=request.form["mail"]
        session["email"]=email.split("@")[0]
        password=request.form["password"]
        print(session["email"])
        if 'email' in session:  
            doc_ref=ref.child(session["email"]).get()
            print(doc_ref)
            # session["info"]=doc_ref
            
            try:

                login=auth.sign_in_with_email_and_password(email,password)
                if doc_ref:
                    return  render_template("index.html",info=doc_ref)
                else:
                     return render_template("index.html")
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
            ref.update({email.split("@")[0]:{}})
            return  render_template("login.html",result="Sucessfully created account now Login")
        except:
            res="Mail already Exist"
            return  render_template("signup.html",result=res)
@app.route('/update', methods=['GET', 'POST'])
def update():
     if 'email' in session:  
            due=request.form["due"]
            time=request.form["time"]
            details=request.form["details"]
            tname=request.form["tname"]
            data={tname:{"details":details,"due":due,"time":time,"status":"ongoing"}}
            
            if(data):
                ref.child(session["email"]).update(data)
                return render_template("index.html",info=ref.child(session["email"]).get(),updation="Sucessfully Updated")
            else:
                return  render_template("index.html",updation="error Occured in updation")
@app.route('/delete', methods=['GET', 'POST'])
def delete():
     if 'email' in session:  
            deln=request.form["del"]
            print(deln)
            ref.child(session["email"]+"/"+deln).delete()
            info=ref.child(session["email"]).get()
            if info:
                    return  render_template("index.html",info=info)
            else:
                     return render_template("index.html")
            
@app.route('/update_status', methods=['GET', 'POST'])
def update_status():
     if 'email' in session:  
            tname=request.form["del"]
            data={"status":"completed"}
            
            if(data):
                ref.child(session["email"]+"/"+tname).update(data)
                return render_template("index.html",info=ref.child(session["email"]).get(),updation="Sucessfully Updated")
            else:
                return  render_template("index.html",updation="error Occured in updation")
@app.route('/logout')  
def logout():  
    if 'email' in session:  
        session.pop('email',None)  
        return render_template('login.html');  
    else:  
        return '<p>user already logged out</p>'  

if __name__ == '__main__':
    app.run(debug=True)

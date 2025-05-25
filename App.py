from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ============== SQL ==============#

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.secret_key = 'YourSecretKey'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(200), nullable=False, unique=True)
    Password = db.Column(db.String(200), nullable=False)
    
# ============= End_SQL =============#


# ============== Sign_In ==============#

@app.route('/', methods=['POST', 'GET'])
def Sign_In():
    Error_Message = ''
    if request.method == 'POST':
        Your_Email = request.form['Email']
        Your_Pass = request.form['Password']
        
        user = User.query.filter_by(Email=Your_Email).first()

        if user and check_password_hash(user.Password, Your_Pass):
            session['Name'] = user.Name
            return redirect('/MainPage')
        else:
            Error_Message = 'The Email Or Password is Wrong'
        

    return render_template('Sign_In.html', Error_Message=Error_Message)

# ============ End_Sign_In ============#


# ============= Sign_Up =============#

@app.route('/Sign_Up', methods=['POST', 'GET'])
def Sign_Up():
    Error_Message = ''
    if request.method == 'POST':
        New_Name = request.form['Name']
        New_Email = request.form['Email']
        New_Pass = request.form['Password']
        hashed_password = generate_password_hash(New_Pass)
        New_User = User(Name=New_Name, Email=New_Email, Password=hashed_password)

        try:
            db.session.add(New_User)
            db.session.commit()
            return redirect('/')
        except:
            Error_Message = 'This email is already in use.'
    return render_template('Sign_Up.html',Error_Message=Error_Message)
    
# =========== End_Sign_Up ===========#


# ============= MainPage =============#

@app.route('/MainPage', methods=['POST', 'GET'])
def MainPage():
    name = session.get('Name', 'Guest')
    if request.method == 'POST':
    	LogOut = request.form['LogOut']
    	if LogOut:
    		session.clear()
    		return redirect('/')
    		
    
    return render_template('MainPage.html', name=name)

# =========== EndMainPage ===========#


# ============== Run ==============#

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

# ============ End_Run ============#
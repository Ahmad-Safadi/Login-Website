from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

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
    Error_Message1 = ''
    Error_Message2 = ''
    if request.method == 'POST':
        Your_Email = request.form['Email']
        Your_Pass = request.form['Password']
        
        user = User.query.filter(User.Email == Your_Email, User.Password == Your_Pass).first()

        if user:
            session['Name'] = user.Name
            return redirect('/MainPage')
        else:
            Error_Message1 = 'The Email is Wrong'
            Error_Message2 = 'The Password is Wrong'

    return render_template('Sign_In.html',Error_Message1=Error_Message1,Error_Message2=Error_Message2)

# ============ End_Sign_In ============#


# ============= Sign_Up =============#

@app.route('/Sign_Up', methods=['POST', 'GET'])
def Sign_Up():
    if request.method == 'POST':
        New_Name = request.form['Name']
        New_Email = request.form['Email']
        New_Pass = request.form['Password']
        New_User = User(Name=New_Name, Email=New_Email, Password=New_Pass)

        try:
            db.session.add(New_User)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    return render_template('Sign_Up.html')
    
# =========== End_Sign_Up ===========#


# ============= MainPage =============#

@app.route('/MainPage', methods=['POST', 'GET'])
def MainPage():
    name = session.get('Name', 'Guest')
    
    return render_template('MainPage.html', name=name)


# =========== EndMainPage ===========#


# ============== Run ==============#

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

# ============ End_Run ============#
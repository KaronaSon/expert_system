from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL  
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash  


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  

app.config['MYSQL_HOST'] = '127.0.0.1' 
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'smart_city'  

mysql = MySQL(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return cls(id=user[0], username=user[1], email=user[2], password=user[3])
        return None

    @classmethod
    def create(cls, username, email, password):
        hashed_password = generate_password_hash(password)  # Hash the password
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return cls(id=cursor.lastrowid, username=username, email=email, password=hashed_password)

    @classmethod
    def get(cls, user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return cls(id=user[0], username=user[1], email=user[2], password=user[3])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form['email_or_username']
        password = request.form['password']
        
        # First, try to find the user by username
        user = User.get_by_username(email_or_username)
        
        # If not found by username, try to find by email
        if not user:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email_or_username,))
            user = cursor.fetchone()
            cursor.close()
        
        # If user is found and password matches
        if user and check_password_hash(user[3], password):  # Verify hashed password
            user_obj = User(id=user[0], username=user[1], email=user[2], password=user[3])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.create(username, email, password)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/smart-governance')
@login_required
def smart_governance():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM smart_governance LIMIT 1")
    governance = cursor.fetchone()
    cursor.close()  # Close the cursor
    return render_template('smart_governance.html', governance=governance)


@app.route('/smart-economy')
@login_required
def smart_economy():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM smart_economy LIMIT 1")
    economy = cursor.fetchone()
    cursor.close()  # Close the cursor
    return render_template('smart_economy.html', economy=economy)


@app.route('/smart-mobility')
@login_required
def smart_mobility():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM smart_mobility LIMIT 1")
    mobility = cursor.fetchone()
    cursor.close()  # Close the cursor
    return render_template('smart_mobility.html', mobility=mobility)


@app.route('/smart-environment')
@login_required
def smart_environment():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM smart_environment LIMIT 1")
    environment = cursor.fetchone()
    cursor.close()  # Close the cursor
    return render_template('smart_environment.html', environment=environment)


@app.route('/smart-living')
@login_required
def smart_living():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM smart_living LIMIT 1")
    living = cursor.fetchone()
    cursor.close()  
    return render_template('smart_living.html', living=living)


@app.route('/smart-people')
@login_required
def smart_people():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM smart_people LIMIT 1")
    people = cursor.fetchone()
    cursor.close()  
    return render_template('smart_people.html', people=people)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

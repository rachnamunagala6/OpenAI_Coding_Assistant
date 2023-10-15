from flask import Flask, render_template, redirect, url, request
import openai
from openai.error import RateLimitError
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User  # Import the User model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Change this to your preferred database
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login route



openai.api_key = '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'

@app.route('/')
def home():
    # Render the React index.html file
    return render_template('index.html')

# route for home page
@app.route('/')
def home():
    return render_template('code_generation.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

# route for handling code generation based on user choice
@app.route('/generate-code', methods=['POST'])
def generate_code():
    try:
        # Get user-submitted code snippet and generation type
        user_code = request.form['code']
        generation_type = request.form['generation_type']

        prompt = user_code

        if generation_type == 'explain':
           prompt = f"Explain the following code:\n{user_code}"
        elif generation_type == 'syntax-check':
            prompt = f"Check the syntax of this code: \n{user_code}"
        elif generation_type == 'optimize':
            prompt = f"Check how to optimize this code: \n{user_code}"
        elif generation_type == 'complete':
            prompt= f"Complete this code: \n{user_code}"
        elif generation_type == 'format':
            prompt = f"Format this code: \n{user_code}"

        # OpenAI API call
        response = openai.Completion.create(
            engine= 'text-davinci-003',
            prompt=prompt,
            max_tokens=300  # Adjust as needed
        )

        # Extract the result rom the OpenAI response
        generated_code = response['choices'][0]['text']

        # Render the template with the generated code
        return render_template('generation_result.html', generated_code=generated_code)

    except RateLimitError as e:
        return render_template('rate_limit_error.html', error_message=str(e))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

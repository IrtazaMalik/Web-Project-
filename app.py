from flask import Flask,render_template, request, redirect , jsonify
import random
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['user_database']
users_collection = db['users']


# Dummy database to store user information
users = {}

# Dummy question bank for each topic
chemistry_questions = [
    {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Fe", "Hg"], "answer": "Au"},
    {"question": "What is the atomic number of oxygen?", "options": ["8", "6", "12", "16"], "answer": "8"},
    {"question": "Which gas is known as laughing gas?", "options": ["Nitrogen", "Oxygen", "Carbon dioxide", "Nitrous oxide"], "answer": "Nitrous oxide"},
    {"question": "What is the chemical formula for water?", "options": ["H2O", "CO2", "NaCl", "C6H12O6"], "answer": "H2O"},
    {"question": "What is the chemical symbol for silver?", "options": ["Ag", "Au", "Fe", "Hg"], "answer": "Ag"},
    {"question": "Which gas do plants use during photosynthesis?", "options": ["Oxygen", "Carbon dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon dioxide"},
    {"question": "What is the pH value of a neutral substance?", "options": ["7", "0", "14", "1"], "answer": "7"},
    {"question": "What is the chemical formula for table salt?", "options": ["NaCl", "H2O", "CO2", "C6H12O6"], "answer": "NaCl"},
    {"question": "What is the chemical symbol for iron?", "options": ["Fe", "Au", "Ag", "Hg"], "answer": "Fe"},
    {"question": "Which element is used as a fuel in nuclear reactors?", "options": ["Uranium", "Hydrogen", "Oxygen", "Carbon"], "answer": "Uranium"}
]

physics_questions = [
    {"question": "What is the SI unit of force?", "options": ["Newton", "Watt", "Joule", "Kilogram"], "answer": "Newton"},
    {"question": "What is the acceleration due to gravity on Earth?", "options": ["9.8 m/s^2", "8.2 m/s^2", "10.5 m/s^2", "7.6 m/s^2"], "answer": "9.8 m/s^2"},
    {"question": "What is the SI unit of electric current?", "options": ["Ampere", "Volt", "Ohm", "Coulomb"], "answer": "Ampere"},
    {"question": "What is the SI unit of energy?", "options": ["Joule", "Watt", "Newton", "Coulomb"], "answer": "Joule"},
    {"question": "Which law states that every action has an equal and opposite reaction?", "options": ["Newton's third law of motion", "Newton's first law of motion", "Newton's second law of motion", "Law of inertia"], "answer": "Newton's third law of motion"},
    {"question": "What is the speed of light in vacuum?", "options": ["299,792,458 m/s", "300,000,000 m/s", "285,000,000 m/s", "350,000,000 m/s"], "answer": "299,792,458 m/s"},
    {"question": "What is the SI unit of power?", "options": ["Watt", "Joule", "Newton", "Ampere"], "answer": "Watt"},
    {"question": "Which scientist proposed the theory of relativity?", "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Stephen Hawking"], "answer": "Albert Einstein"},
    {"question": "What is the SI unit of pressure?", "options": ["Pascal", "Newton", "Joule", "Watt"], "answer": "Pascal"},
    {"question": "Which instrument is used to measure electric current?", "options": ["Ammeter", "Voltmeter", "Ohmmeter", "Wattmeter"], "answer": "Ammeter"}
]

maths_questions = [
    {"question": "What is the value of Pi (π) to two decimal places?", "options": ["3.14", "3.12", "3.16", "3.18"], "answer": "3.14"},
    {"question": "What is the square root of 64?", "options": ["8", "6", "10", "12"], "answer": "8"},
    {"question": "What is the value of 'e' (Euler's number) rounded to two decimal places?", "options": ["2.71", "2.65", "3.00", "2.50"], "answer": "2.71"},
    {"question": "What is the value of 5! (factorial of 5)?", "options": ["120", "20", "25", "100"], "answer": "120"},
    {"question": "What is the result of 2^3 (2 raised to the power of 3)?", "options": ["8", "6", "10", "12"], "answer": "8"},
    {"question": "What is the value of log10(100)?", "options": ["2", "1", "10", "100"], "answer": "2"},
    {"question": "What is the value of sin(90°)?", "options": ["1", "0", "-1", "0.5"], "answer": "1"},
    {"question": "What is the area of a circle with radius 5 units (rounded to two decimal places)?", "options": ["78.54 sq units", "75.36 sq units", "50.24 sq units", "31.42 sq units"], "answer": "78.54 sq units"},
    {"question": "What is the value of tan(45°)?", "options": ["1", "0", "√2", "√3"], "answer": "1"},
    {"question": "What is the result of 3/4 expressed as a decimal (rounded to two decimal places)?", "options": ["0.75", "0.70", "0.80", "0.85"], "answer": "0.75"}
]


# Dummy score tracking dictionary
scores = {}


# User Registration
# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    if username in users:
        return jsonify({"message": "Username already exists"}), 400
    users[username] = password
    scores[username] = 0 # Initialize score for the user
    # Redirect to the sign-in page after successful registration
    return redirect('/signin')

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    
    # Hardcoded credentials
    if username != 'irtaza' or password != 'suaaa':
        return jsonify({"message": "Invalid username or password"}), 401
    
    return redirect('/topics')  

# Question Bank
def get_random_question(topic):
    if topic == 'chemistry':
        return random.choice(chemistry_questions)
    elif topic == 'physics':
        return random.choice(physics_questions)
    elif topic == 'maths':
        return random.choice(maths_questions)
    else:
        return None

# Score Tracking
@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    username = data['username']
    score = data['score']
    scores[username] += score
    return jsonify({"message": "Score updated successfully"}), 200


# Route for the root URL
@app.route('/')
def home():
    return render_template('homepage.html')

# Route for serving the signup.html file
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Route for serving the signin.html file
@app.route('/signin')
def signin():
    return render_template('signin.html')

# Route for serving the topics.html file
@app.route('/topics')
def topics():
    return render_template('topics.html')

# Route for serving the chemistry page
@app.route('/chemistry')
def chemistry():
    return render_template('chemistry.html')

# Route for serving the maths page
@app.route('/maths')
def maths():
    return render_template('math.html')

# Route for serving the physics page
@app.route('/physics')
def physics():
    return render_template('physics.html')

app.static_folder = 'static'

if __name__ == '__main__':
    app.run(debug=True)

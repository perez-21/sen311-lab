from flask import Flask, redirect, url_for, request, render_template
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/success')
def success():
	return render_template('success.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']

		clean_username = validate_username(username)
		clean_password = validate_password(password)

		hashed_password = hash_password(clean_password)

		with sqlite3.connect('users.db') as conn:
			cursor = conn.cursor()
			cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (clean_username, hashed_password))


		return redirect(url_for('success'))
	

def validate_username(username):
	norm_username = str.strip(username)
	if (len(norm_username) < 2):
		raise ValueError('Username cannot be shorter than 2 characters')
	if (len(norm_username) > 30):
		raise ValueError('Username cannot be longer than 30 characters')
	return norm_username

def validate_password(password):
	norm_password = str.strip(password)
	if (len(norm_password) < 8 or len(norm_password) > 20):
		raise ValueError('Password length must be 8 - 20 characters')
	return norm_password
	

def hash_password(password):
	return bcrypt.generate_password_hash(password).decode()

def init_db():
	with sqlite3.connect('users.db') as conn:
		cursor = conn.cursor()

		try:
			cursor.execute('''
				CREATE TABLE users (
						id INTEGER PRIMARY KEY,
						username TEXT UNIQUE NOT NULL,
						password TEXT NOT NULL
					)
			''')
		except sqlite3.OperationalError: 
			print('table already created')

if __name__ == '__main__':
	init_db()
	app.run()

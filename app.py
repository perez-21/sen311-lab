from flask import Flask, redirect, url_for, request, render_template
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
	return render_template('login.html')

@app.route('/signup/success')
def success():
	return render_template('success.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		user = request.form['nm']
		print(user)

		username = request.form['username']
		password = request.form['password']

		clean_username = validate_username(username)
		clean_password = validate_password(password)

		hashed_password = hash_password(clean_password)

		#save to my sql database


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
	

def hash_password(password):
	return bcrypt.generate_password_hash(password).decode()

if __name__ == '__main__':
	app.run()

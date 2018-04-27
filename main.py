from flask import Flask, request, redirect, session, flash, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Launchcode@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class User(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120))
	blogs = db.relationship('Blogpost', backref='owner')

	def __init__(self, username, password):
		self.username = username
		self.password = password

class Blogpost(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.String(500))
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	#owner = db.Column(db.Integer, db.ForeignKey('user.username'))


	def __init__(self, title, body, owner):
		self.title = title
		self.body = body
		self.owner = owner
		
@app.before_request
def require_login():
	not_allowed_routes = ['newpost']
	if request.endpoint in not_allowed_routes and 'username' not in session:
		return redirect('/login')
app.secret_key = 'DougisGilfoyle'

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
	error = None
	title = ''
	body = ''
	owner = User.query.filter_by(username=session['username']).first()

	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		if title == '' or body == '':
			error = "Please add content before submitting"
		else:
			new_post = Blogpost(title, body, owner)
			db.session.add(new_post)
			db.session.commit()
			return redirect('/blog?id='+ str(new_post.id))
			db.session.username()

	return render_template('newpost.html', error=error)

@app.route('/login', methods=['POST', 'GET'])
def login():
	error = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username).first()
		if user and user.password == password:
			session['username'] = username
			return redirect('/newpost')
		else:
			error = 'User password incorrect, or user does not exist'

	return render_template('login.html', error=error)

#@app.route('/signup', methods=['POST'])

		
		
@app.route('/signup', methods=['POST', 'GET'])
def signup():
	error = ''
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		verify = request.form['verify']
		un_db_count = User.query.filter_by(username=username).count()
		if un_db_count > 0:
			error = 'Duplicate user'
		#username_list = []
		if username == '' or password == '':
			error = "Please fill out all fields"
		#if username in  
		#	error = "Duplicate User"
		if password != verify:
			error = "Passwords do not match"
		if error == '':
			new_user = User(username, password)
			db.session.add(new_user)
			db.session.commit()
			session['username'] = username
			return redirect('/')

	return render_template('signup.html', error=error)
	

@app.route('/logout')
def logout():
	del session['username']
	return redirect('/blog')

@app.route('/', methods=['POST', 'GET'])
def index():
	users = User.query.all()
	return render_template('index.html', users=users)


@app.route('/blog')
def show_blogs():
	
	blog_id = request.args.get('id')
	blog_user_id = request.args.get('user')
	if blog_id != None:
		blogposts = Blogpost.query.filter_by(id=blog_id)
	elif blog_user_id != None:
		blogposts = Blogpost.query.filter_by(owner_id=blog_user_id)
	else:
		blogposts = Blogpost.query.all()

	return render_template('blog.html',title="Current Blogposts!", blogposts=blogposts)


if __name__ == '__main__':
	app.run()
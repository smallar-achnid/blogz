from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Launchcode@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blogpost(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120))
	body = db.Column(db.String(500))

	def __init__(self, title, body):
		self.title = title
		self.body = body
		


@app.route('/', methods=['POST', 'GET'])
def index():
	error = None
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		if title == '' or body == '':
			error = "Please add content before submitting"
		else:
			new_post = Blogpost(title, body)
			db.session.add(new_post)
			db.session.commit()
			return redirect('/blog')

	#posts = Blogpost.query.all()
	
	return render_template('newpost.html',title="Add New Post!", error=error)


@app.route('/blog')
def show_blogs():
	
	blog_id = request.args.get('id')
	if blog_id != None:
		blogposts = Blogpost.query.filter_by(id=blog_id)
	else:
		blogposts = Blogpost.query.all()
	
	return render_template('blog.html',title="Current Blogposts!", blogposts=blogposts)#completed_tasks=completed_tasks)


if __name__ == '__main__':
	app.run()
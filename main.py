from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build77blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def welcome():
    return render_template('welcome.html',title="Welcome to Build a Blog")

@app.route('/blog', methods=['POST', 'GET'])
def index():

    blog_id = request.args.get('param_name')
    if blog_id != ""
        post = Blog.query.filter_by(id=blog_id)
        return render_template('postview.html', post)
    posts = Blog.query.all()
    return render_template('blog.html',title="Build a Blog!", 
        posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_text = request.form['blog_text']
        new_post = Blog(blog_title, blog_text)
        db.session.add(new_post)
        db.session.commit()

        posts = Blog.query.all()
        return redirect('/blog')

    return render_template('newpost.html',title="Build a Blog!")


if __name__ == '__main__':
    app.run()
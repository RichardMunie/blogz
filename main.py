from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogger69@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username , password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',title="Blogz!", 
        users=users)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        # todo validate

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            # make better respose
            return "<h1>Duplicate User!</h1>"

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("logged in")
            print(session)
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html',title="Blogz!")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blog():

    if request.args.get('id'):
        blog_id = request.args.get('id')
        post = Blog.query.get(int(blog_id))
        return render_template('postview.html',title="Blogz!", post=post)

    if request.args.get('user'):
        user = request.args.get('user')
        userguy = User.query.filter_by(username=user).first()
        user_id = userguy.id
        posts = Blog.query.filter_by(owner_id=user_id)
        return render_template('blog.html', title="Blogz", posts=posts)

    posts = Blog.query.all()
    return render_template('blog.html',title="Blogz!" , 
        posts=posts)


@app.route('/newpost', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        title_error = ""
        text_error = ""
        blog_title = request.form['title']
        if blog_title == "":
             title_error = "Your blog must include a title."
        blog_text = request.form['blog_text']
        if blog_text == "":
             text_error = "Your blog must include some content."
        if title_error != "" or text_error != "":
            return render_template('newpost.html', title="Blogz!", title_error=title_error, text_error=text_error,
             blog_title = blog_title, blog_text=blog_text)
        owner = User.query.filter_by(username=session['username']).first()
        new_post = Blog(blog_title, blog_text, owner)
        db.session.add(new_post)
        db.session.commit()
        
        posts = Blog.query.all()
        last = posts[len(posts)-1]
        return redirect('/blog?id=' + str(last.id)) 

    return render_template('newpost.html', title="Blogz!")


if __name__ == '__main__':
    app.run()
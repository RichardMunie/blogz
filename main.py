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

@app.route('/blog', methods=['GET'])
def index():

    if request.args.get('id'):
        blog_id = request.args.get('id')
        post = Blog.query.get(int(blog_id))
        return render_template('postview.html', title="Build a Blog!", post=post)

    posts = Blog.query.all()
    return render_template('blog.html', title="Build a Blog!", 
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
            return render_template('newpost.html', title_error=title_error, text_error=text_error,
             title = blog_title, blog_text=blog_text)
        new_post = Blog(blog_title, blog_text)
        db.session.add(new_post)
        db.session.commit()

        posts = Blog.query.all()
        last = posts[len(posts)-1]
        return redirect('/blog?id=' + str(last.id)) 

    return render_template('newpost.html',title="Build a Blog!")


if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)

# Form Initialization
ckeditor = CKEditor(app)
class PostForm(FlaskForm):
    title = StringField(label='Blog Post Title', validators=[DataRequired()])
    subtitle = StringField(label='Subtitle', validators=[DataRequired()])
    author = StringField(label='Your Name', validators=[DataRequired()])
    img_url = StringField(label='Blog Image URL', validators=[DataRequired()])
    body = CKEditorField(label='Blog Content', validators=[DataRequired()])
    submit = SubmitField(label='Submit Post')

# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = []

    result = db.session.execute(db.Select(BlogPost))
    every_blog_post = result.scalars()
    for post in every_blog_post:
        posts.append(post)

    print(posts)

    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show-post/<post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=['POST', 'GET'])
def add_new_post():
    create_post_form = PostForm()
    if create_post_form.validate_on_submit():
        today_month = date.today().strftime("%B")
        today_date = date.today().day
        today_year = date.today().year

        new_post = BlogPost(
            title = create_post_form.title.data,
            subtitle = create_post_form.subtitle.data,
            date = f"{today_month} {today_date}, {today_year}",
            body = create_post_form.body.data,
            author = create_post_form.author.data,
            img_url = create_post_form.img_url.data
        )

        # FLAG: Cleanup this test
        print(f"Test title: {new_post.title}\n"
              f"Test subtitle: {new_post.subtitle}\n"
              f"Test date: {new_post.date}\n"
              f"Test body: {new_post.body}\n"
              f"Test author: {new_post.author}\n"
              f"Test img_url: {new_post.img_url}")


    return render_template("make-post.html", form=create_post_form)

# TODO: edit_post() to change an existing blog post

# TODO: delete_post() to remove a blog post from the database

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)

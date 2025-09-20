from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap5
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import markdown
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from forms import BlogPostForm, LoginForm, RegisterForm, ProfileForm, UserForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tajni_kljuc')
bootstrap = Bootstrap5(app)
client = MongoClient('mongodb://localhost:27017/')
db = client['pzw_blog_database']
posts_collection = db['posts']
users_collection = db['users']
comments_collection = db['comments']
fs = gridfs.GridFS(db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(email):
    user_data = users_collection.find_one({"email": email})
    if user_data:
        return User(user_data['email'], user_data.get('is_admin', False), user_data.get('theme', ''))
    return None

class User(UserMixin):
    def __init__(self, email, admin=False, theme=''):
        self.id = email
        self.admin = admin
        self.theme = theme

    @property
    def is_admin(self):
        return self.admin

@app.route("/", methods=["GET"])
def index():
    published_posts = posts_collection.find({"status": "published"}).sort('date', -1)
    return render_template('index.html', posts=published_posts)

@app.route('/blog/create', methods=["GET", "POST"])
@login_required
def post_create():
    form = BlogPostForm()
    if form.validate_on_submit():
        image_id = save_image_to_gridfs(request, fs)
        post = {
            'title': form.title.data,
            'content': form.content.data,
            'author': current_user.get_id(),
            'status': form.status.data,
            'date': datetime.combine(form.date.data, datetime.min.time()),
            'tags': form.tags.data,
            'image_id': image_id,
            'date_created': datetime.utcnow()
        }
        posts_collection.insert_one(post)
        flash('Članak je uspješno upisan.', 'success')
        return redirect(url_for('index'))
    return render_template('blog_edit.html', form=form)

@app.route('/blog/<post_id>', methods=["GET", "POST"])
def post_view(post_id):
    post = posts_collection.find_one({'_id': ObjectId(post_id)})
    if not post:
        flash("Članak nije pronađen!", "danger")
        return redirect(url_for('index'))
    comments = comments_collection.find({"post_id": post_id}).sort('date', 1)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = {
            "post_id": post_id,
            "author": current_user.get_id(),
            "content": form.content.data,
            "date": datetime.utcnow()
        }
        comments_collection.insert_one(comment)
        flash("Komentar dodan!", "success")
        return redirect(url_for('post_view', post_id=post_id))
    return render_template('blog_view.html', post=post, comments=comments, form=form)

@app.route('/blog/edit/<post_id>', methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post['author'] != current_user.get_id() and not current_user.is_admin:
        abort(403, "Nemate dozvolu za uređivanje ovog članka.")
    form = BlogPostForm()
    if request.method == 'GET':
        form.title.data = post['title']
        form.content.data = post['content']
        form.date.data = post['date']
        form.tags.data = post['tags']
        form.status.data = post['status']
    elif form.validate_on_submit():
        posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {
                'title': form.title.data,
                'content': form.content.data,
                'date': datetime.combine(form.date.data, datetime.min.time()),
                'tags': form.tags.data,
                'status': form.status.data,
                'date_updated': datetime.utcnow()
            }}
        )
        image_id = save_image_to_gridfs(request, fs)
        if image_id:
            posts_collection.update_one(
                {"_id": ObjectId(post_id)},
                {"$set": {'image_id': image_id}}
            )
        flash('Članak je uspješno ažuriran.', 'success')
        return redirect(url_for('post_view', post_id=post_id))
    else:
        flash('Dogodila se greška!', category='warning')
    return render_template('blog_edit.html', form=form)

@app.route('/blog/delete/<post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post['author'] != current_user.get_id() and not current_user.is_admin:
        abort(403, "Nemate dozvolu za brisanje ovog posta.")
    posts_collection.delete_one({"_id": ObjectId(post_id)})
    comments_collection.delete_many({"post_id": post_id})
    flash('Članak je uspješno obrisan.', 'success')
    return redirect(url_for('index'))

def save_image_to_gridfs(request, fs):
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            return fs.put(image, filename=image.filename)
    return None

@app.route('/image/<image_id>')
def serve_image(image_id):
    image = fs.get(ObjectId(image_id))
    return image.read(), 200, {'Content-Type': 'image/jpeg'}

@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_data = users_collection.find_one({"email": email})
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data['email'], user_data.get('is_admin', False))
            login_user(user, form.remember_me.data)
            flash('Uspješno ste se prijavili!', category='success')
            return redirect(url_for('index'))
        flash('Neispravno korisničko ime ili zaporka!', category='warning')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Odjavili ste se.', category='success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            flash('Korisnik već postoji', category='error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({
            "email": email,
            "password": hashed_password,
            "is_admin": False
        })
        flash('Registracija uspješna. Sad se možete prijaviti', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

def update_user_data(user_data, form):
    if form.validate_on_submit():
        users_collection.update_one(
        {"_id": user_data['_id']},
        {"$set": {
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "bio": form.bio.data,
            "theme": form.theme.data
        }}
        )
        if form.image.data:
            if user_data.get('image_id'):
                fs.delete(user_data['image_id'])
            image_id = save_image_to_gridfs(request, fs)
            if image_id:
                users_collection.update_one(
                    {"_id": user_data['_id']},
                    {"$set": {'image_id': image_id}}
                )
        flash("Podaci uspješno ažurirani!", "success")
        return True
    return False

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_data = users_collection.find_one({"email": current_user.get_id()})
    form = ProfileForm(data=user_data)
    title = "Vaš profil"
    if update_user_data(user_data, form):
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form, image_id=user_data.get("image_id"), title=title)

@app.route('/users', methods=['GET'])
@login_required
def users():
    if not current_user.is_admin:
        abort(403, "Samo admin može vidjeti korisnike.")
    users = users_collection.find().sort("email")
    return render_template('users.html', users=users)

@app.errorhandler(403)
def access_denied(e):
    return render_template('403.html', description=e.description), 403

if __name__ == '__main__':
    app.run(debug=True)
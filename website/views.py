from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .models import Post,User,Log
from . import db
views=Blueprint("views",__name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts=Post.query.all()
    return render_template('home.html', user=current_user,posts=posts) 

@views.route('/create-post', methods=['GET','POST'])
@login_required
def create_post():
    if request.method=='POST':
        text=request.form.get('text')
        tracker_type = request.form.get('type')
        if not text:
            flash('post cannot be empty',category='error')
        else:
            post=Post(text=text,tracker_type=tracker_type,author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('post successfully created',category='success')  
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

@views.route('/profile')
def profile():
    return "<h1>Profile</h1>"  

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    
    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/edit-post/<id>",methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to edit this post.', category='error')
    else:
        try:
            if request.method == 'POST':
                text = request.form.get('text')
                tracker_type = request.form.get('type')
                post = Post.query.filter_by(id=id).first()
                post.text = text
                post.tracker_type = tracker_type
                db.session.commit()
                flash('Tracker Updated Successfully.', category='success')
                return redirect(url_for('views.home'))
        except Exception as e:
            print(e)
            flash('Something went wrong.', category='error')

    return render_template("edit_post.html", user=current_user, Post=post)


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route('/add-log-page/<id>', methods=['GET', 'POST'])
@login_required
def add_log(id):
    from .models import Post, Log
    this_tracker = Post.query.get(id)
    import datetime
    now = datetime.datetime.now()
    try:
        if request.method == 'POST':
            when = request.form.get('date')
            notes = request.form.get('notes')
            from . import db
            new_log = Log(timestamp=when, notes=notes , user=current_user.id,
                          added_date_time=now)
            db.session.add(new_log)
            db.session.commit()
            flash('New Log Added', category='success')
            return redirect(url_for('views.home'))
    except Exception as e:
        print(e)
        flash('Something went wrong.', category='error')
    return render_template("add_log_page.html", user=current_user, Post=this_tracker, now=now)

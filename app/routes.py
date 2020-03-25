from flask import render_template,redirect,request,flash,session,url_for
from flask_login import logout_user,current_user, login_user, login_required
from app import app,db
from app.models import User
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html',title='home')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash('Invalid username or password','danger')
                return redirect(url_for('login'))
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In')

    
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        cpassword = request.form.get('cpassword')
        password = request.form.get('password')
        print(cpassword, password, cpassword==password)
        if username and password and cpassword and email:
            if cpassword != password:
                flash('Password do not match','danger')
                return redirect('/register')
            else:
                if User.query.filter_by(email=email).first() is not None:
                    flash('Please use a different email address','danger')
                    return redirect('/register')
                elif User.query.filter_by(username=username).first() is not None:
                    flash('Please use a different username','danger')
                    return redirect('/register')
                else:
                    user = User(username=username, email=email)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
                    flash('Congratulations, you are now a registered user!','success')
                    return redirect(url_for('login'))
        else:
            flash('Fill all the fields','danger')
            return redirect('/register')

    return render_template('register.html', title='Sign Up page')


@app.route('/forgot',methods=['GET', 'POST'])
def forgot():
    if request.method=='POST':
        email = request.form.get('email')
        if email:
            pass
    return render_template('forgot.html', title='Password reset page')
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user, title=f'{user.username} profile')


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method=='POST':
        current_user.username = request.form.get('username')
        current_user.about_me = request.form.get('aboutme')
        db.session.commit()
        flash('Your changes have been saved.','success')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html', title='Edit Profile',user=user)
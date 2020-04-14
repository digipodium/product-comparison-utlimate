from flask import render_template,redirect,request,flash,session,url_for, jsonify
from flask_login import logout_user,current_user, login_user, login_required
from app import app,db
from app.models import User,ScrapedData
import os
import pandas as pd
from datetime import datetime
from app.scrapers import snapdeal,flipcart
from app import preprocessing as pp
from app import visualizer as vis

@app.route('/',)
@app.route('/index')
@login_required
def index():
    try:
        del session['keyword']
        del session['sort_order']
        del session['page_limit']
        del session['delay'] 
        del session['executing']
    except :pass
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
        # print(cpassword, password, cpassword==password)
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
            flash('password sent to email, please check your inbox')
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

@app.route('/scraper_run',methods=['GET','POST'])
def scraper_run_api():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        sort_order = request.form.get('sort')
        page_limit = request.form.get('page_limit')
        delay =request.form.get('delay')
        if keyword and sort_order and page_limit:
            session['keyword'] = keyword
            session['sort_order'] = sort_order
            session['page_limit'] = page_limit
            session['delay'] = delay
            return render_template('search.html',title="Search to Compare")
        else:
            flash("please enter an item category to search and compare using scraper",'danger')
            return redirect('/')
    else:
        return redirect('/')
    
@app.route('/execute',methods=['POST'])
def execute_scrapers():
    if request.method == 'POST':
        with open('scraper.log','w') as f:
            f.write(f"starting scraper\n")
        keyword = session['keyword']
        sort_order = session['sort_order']
        page_limit = session['page_limit']
        delay = session['delay'] 
        # print(session)
        sop = snapdeal.sort_options.get(sort_order)
        message = flipcart.collect_n_store(query=keyword,count=int(page_limit),delay=int(delay),sorting=sop)
        print(message)
        message = snapdeal.collect_n_store(query=keyword,count=int(page_limit),delay=int(delay),sorting=sop)
        print(message)
        session['executing'] = False
        return jsonify(status='success',scraper_status = session['executing'])
    
@app.route('/scraper_status')
def scraper_status_api():
    if os.path.exists('scraper.log'):
        try:
            f = open('scraper.log')
            for size,last_line in enumerate(f):
                pass
            f.close()
            session['log'] = last_line
            return jsonify(size=size,last_line=last_line)
        except Exception as e:
            print(e)
            return jsonify(size='unknown',last_line='unknown')

@app.route('/view_results')
def view_results():
    keyword = session['keyword']
    page = request.args.get('page',1,type=int)
    data = ScrapedData.query.filter_by(keyword=keyword).order_by(ScrapedData.created_on).paginate(page,app.config['DATASET_SIZE'] ,False)

    prev_url = url_for('view_results',page=data.prev_num) if data.has_prev else None
    next_url = url_for('view_results',page=data.next_num) if data.has_next else None
    return render_template('search_results.html',scraped_data=data.items, next_url=next_url,prev_url=prev_url)


@app.route('/history')
def history():
    page = request.args.get('page',1,type=int)
    data = ScrapedData.query.paginate(page,app.config['DATASET_SIZE'] ,False)
    prev_url = url_for('history',page=data.prev_num) if data.has_prev else None
    next_url = url_for('history',page=data.next_num) if data.has_next else None
    return render_template('history.html',scraped_data = data.items, next_url=next_url,prev_url=prev_url)

@app.route('/visualize')
def visualize():
    keyword = request.args.get('keyword','bottles')
    dataset = vis.load_data(db)
    kList = dataset.keyword.unique()
    price_barplot_data = vis.bar_polar_price_distribution(dataset, kw=keyword,title=f'{keyword} price distribution on eccomerce websites'.upper())
    comp_item_prices = vis.hist_comparison_of_item_prices(dataset, kw=keyword,title=f'{keyword} price comparison'.upper())
    comp_item_tot_rating = vis.hist_comparison_of_item_total_ratings(dataset, kw=keyword, title =f'{keyword} total ratings comparison'.upper() )
    comp_item_tot_reviews = vis.hist_comparison_of_item_total_reviews(dataset,kw=keyword, title =f'{keyword} total reviews comparison'.upper() )
    comp_item_rating = vis.hist_comparison_of_item_rating( dataset,kw=keyword, title =f'{keyword} rating comparison'.upper() )
    
    return render_template('visualize.html', 
                            price_barplot_data=price_barplot_data,
                            comp_item_prices = comp_item_prices,
                            comp_item_tot_reviews = comp_item_tot_reviews,
                            comp_item_tot_rating = comp_item_tot_rating,
                            comp_item_rating = comp_item_rating,
                            keywordList=kList, )
from flask import Flask, render_template, request, redirect, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

# repair some error
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
app = Flask(__name__)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.secret_key = 'super-secret-key'
db = SQLAlchemy(app)



class add_category(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    c = db.Column(db.String(200), nullable=True)
    c1 = db.Column(db.String(200), nullable=True)
    c2 = db.Column(db.String(200), nullable=True)
    c3 = db.Column(db.String(200), nullable=True)
    c4 = db.Column(db.String(200), nullable=True)
    c5 = db.Column(db.String(200), nullable=True)

class add_special_category(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    desc = db.Column(db.String(500), nullable=True)
    img = db.Column(db.String(200), nullable=True)

class add_shopping_card(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    desc = db.Column(db.String(500), nullable=True)
    reviews = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Integer)
    img1 = db.Column(db.String(200), nullable=True)
    img2 = db.Column(db.String(200), nullable=True)
    img3 = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(200), nullable=True)
    sub_category = db.Column(db.String(200), nullable=True)


class payment_method(db.Model):
    # first page
    sno = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(12), nullable=True)
    first_name = db.Column(db.String(200), nullable=True)
    second_name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    date_of_birth = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(200), nullable=True)
    country = db.Column(db.String(200), nullable=True)
    state = db.Column(db.String(200), nullable=True)
    postle_code = db.Column(db.String(200), nullable=True)
    # second page
    full_name = db.Column(db.String(200), nullable=True)
    card_number = db.Column(db.String(500), nullable=True)
    cvv = db.Column(db.String(200), nullable=True)
    #  third page
    product = db.Column(db.String(200), nullable=True)

class contact_us(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(500), nullable=True)
    msg = db.Column(db.String(500), nullable=True)
  

# class user_data(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200))
#     desc = db.Column(db.String(1000))
#     price = db.Column(db.String(200))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150))
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     user = db.relationship('user_data')








@app.route('/', methods=['GET', 'POST'])
def home():
    all_special_category = add_special_category.query.all() 
    return render_template('home-pages/index.html', all_special_category=all_special_category)


@app.route('/user-profile')
def user_profile():
    return render_template('home-pages/user-profile.html')


@app.route('/category')
def category():
    return render_template('home-pages/category.html')

@app.route('/category_product_view/<int:sno>', methods=['GET'])
def category_product(sno):
    special_category = add_special_category.query.filter_by(sno =sno).first()
    shopping_card = add_shopping_card.query.all() 
    return render_template('home-pages/view-special-category-product.html', special_category=special_category, shopping_card=shopping_card)


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    shopping_card = add_shopping_card.query.all() 

    special_category = add_special_category.query.all() 
    all_category = add_category.query.all() 
    price = ""
    if(request.method=='POST'):
        price = request.form.get('price')  
    return render_template('home-pages/shop.html', shopping_card=shopping_card, special_category=special_category, all_category=all_category, price=price)


@app.route('/shop-view')
def shop_view(sno):
    
    return render_template('home-pages/shop-view.html')


@app.route('/about')
def about():
    return render_template('home-pages/about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if(request.method=='POST'):
            name = request.form.get('name')
            email = request.form.get('email')
            msg = request.form.get('msg')
            entry = contact_us(name=name, email=email, msg=msg)
            db.session.add(entry)
            db.session.commit()
    return render_template('home-pages/contact.html')

@app.route('/search')
def search():
    return render_template('home-pages/search.html')    






# dashboard start

@app.route('/dashboard-home')
def dashboard():
    if ('user' in session and session['user'] == params['admin_user']):
        return render_template('dashboard/dashboard-home.html')    
    else:
        return redirect('/')    


# @app.route('/dashboard-posts')
# def dashboard_posts():
#     if ('user' in session and session['user'] == params['admin_user']):
#         return render_template('dashboard/dashboard-posts.html')    
#     else:
#         return redirect('/')

@app.route('/dashboard-category', methods=['GET', 'POST'])
def dashboard_category():
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method=='POST'):
            c = request.form.get('c')
            c1 = request.form.get('c1')
            c2 = request.form.get('c2')
            c3 = request.form.get('c3')
            c4 = request.form.get('c4')
            c5 = request.form.get('c5')
            entry = add_category(c=c, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5 )
            db.session.add(entry)
            db.session.commit()
        return render_template('dashboard/dashboard-category.html')    
    else:
        return redirect('/')    

@app.route('/dashboard-special-category', methods=['GET', 'POST'])
def dashboard_special_category():
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method=='POST'):
            name = request.form.get('name')
            desc = request.form.get('desc')
            f = request.files['img']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename) ))
            img = f.filename
            entry = add_special_category(name=name, desc=desc, img=img)
            db.session.add(entry)
            db.session.commit()
        return render_template('dashboard/dashboard-special-category.html')    
    else:
        return redirect('/')    

@app.route('/dashboard-shop-item', methods=['GET', 'POST'])
def dashboard_shop_item():
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method=='POST'):
            name = request.form.get('name')
            desc = request.form.get('desc')
            reviews = request.form.get('reviews')
            price = request.form.get('price')
            category = request.form.get('category')
            sub_category = request.form.get('sub-category')
            f1= request.files['img1']
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f1.filename) ))
            img1 = f1.filename
            f2= request.files['img2']
            f2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f2.filename) ))
            img2 = f2.filename
            f3= request.files['img3']
            f3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f3.filename) ))
            img3 = f3.filename
            entry = add_shopping_card(name=name, desc=desc, reviews=reviews, price=price, category=category, sub_category=sub_category, img1=img1, img2=img2, img3=img3)
            db.session.add(entry)
            db.session.commit()
        category = add_category.query.all()    
        special_category = add_special_category.query.all() 
        return render_template('dashboard/dashboard-shop-item.html', category=category, special_category=special_category)  
    else:
        return redirect('/')    
    
@app.route('/dashboard-shop-item-view')
def dashboard_shop_item_view():
    if ('user' in session and session['user'] == params['admin_user']):
        all_shopping_card = add_shopping_card.query.all() 
        return render_template('dashboard/dashboard-shop-item-view.html', all_shopping_card=all_shopping_card)
    else:
        return redirect("/")    


@app.route('/dashboard-shop-card-edit/<string:sno>', methods=['GET', 'POST'])
def dashboard_shop_card_edit(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method=='POST'):
            all_shopping_card = add_shopping_card.query.filter_by(sno =sno).first()
            all_shopping_card.name = request.form.get('name')
            all_shopping_card.desc = request.form.get('desc')
            all_shopping_card.reviews = request.form.get('reviews')
            all_shopping_card.price = request.form.get('price')
            img1 = request.form.get('img1')
            if img1 != None:
                img1 = request.files['img1']
                all_shopping_card.img1 = img1.filename
                img1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img1.filename) ))
            img2 = request.form.get('img2')
            if img2 != None:
                img2 = request.files['img2']
                all_shopping_card.img2 = img1.filename
                img2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img2.filename) ))
            img3 = request.form.get('img3')
            if img3 != None:
                img3 = request.files['img3']
                all_shopping_card.img3 = img1.filename
                img3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img3.filename) ))
            all_shopping_card.category = request.form.get('category')
            all_shopping_card.sub_category = request.form.get('sub_category')
            db.session.commit()
            return redirect('/dashboard-shop-card-edit/'+sno)
        all_shopping_card = add_shopping_card.query.filter_by(sno=sno).first()
        return render_template('dashboard/dashboard-shop-card-edit.html', all_shopping_card=all_shopping_card) 
    else:
        return redirect('/')    




 
    


@app.route('/dashboard-special-category-view')
def dashboard_special_category_view():
    if ('user' in session and session['user'] == params['admin_user']):
        all_special_category = add_special_category.query.all() 
        return render_template('dashboard/dashboard-special-category-view.html', all_special_category=all_special_category)   
    else:
        return redirect('/')    


@app.route('/dashboard-category-view')
def dashboard_category_view():
    if ('user' in session and session['user'] == params['admin_user']):
        all_category = add_category.query.all() 
        return render_template('dashboard/dashboard-category-view.html', all_category=all_category) 
    else:
        return redirect('/')     

@app.route('/dashboard-special-category-edit/<string:sno>', methods=['GET', 'POST'])
def dashboard_special_category_edit(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method=='POST'):
            all_special_category = add_special_category.query.filter_by(sno =sno).first()
            all_special_category.name = request.form.get('name')
            all_special_category.desc = request.form.get('desc')
            img = request.form.get('img')
            if img != None:
                img = request.files['img']
                all_special_category.img3 = img.filename
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img.filename) ))
            db.session.commit()
            return redirect('/dashboard-special-category-edit/'+sno)
        all_special_category = add_special_category.query.filter_by(sno=sno).first()
        return render_template('dashboard/dashboard-special-category-edit.html', all_special_category=all_special_category) 
    else:
        return redirect('/')    

@app.route('/dashboard-category-edit/<string:sno>', methods=['GET', 'POST'])
def dashboard_category_edit(sno):
    if ('user' in session and session['user'] == params['admin_user']):
        if(request.method=='POST'):
            all_category = add_category.query.filter_by(sno =sno).first()
            all_category.c = request.form.get('c')
            all_category.c1 = request.form.get('c1')
            all_category.c2 = request.form.get('c2')
            all_category.c3 = request.form.get('c3')
            all_category.c4 = request.form.get('c4')
            all_category.c5 = request.form.get('c5')
            db.session.commit()
            return redirect('/dashboard-category-edit/'+sno)
        all_category = add_category.query.filter_by(sno=sno).first()
        return render_template('dashboard/dashboard-category-edit.html', all_category=all_category) 
    else:
        return redirect('/')


# payment method


@app.route('/payment-method-shipping/<string:sno>', methods=['GET', 'POST'])
def payment_method_shipping(sno):
    if(request.method=='POST'):
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        email = request.form.get('email')
        date_of_birth = request.form.get('date_of_birth')
        contact_number = request.form.get('contact_number')
        country = request.form.get('country')
        state = request.form.get('state')
        postle_code = request.form.get('postle_code')
        entry = payment_method(first_name=first_name, date= datetime.now(), second_name=second_name, email=email, date_of_birth=date_of_birth, contact_number=contact_number, country=country, state=state, postle_code=postle_code)
        db.session.add(entry)
        db.session.commit()
        return redirect('/payment-method-card/'+sno)
    return render_template('payment-method/payment-method-shipping.html', sno=sno)   
# shipping edit
@app.route('/payment-method-shipping-edit', methods=['GET', 'POST'])
def payment_method_shipping_edit():
    paymentMethod= payment_method.query.all() 
    sno = 0
    for i in paymentMethod:
        sno +=1 
    addSecondPage = payment_method.query.filter_by(sno =sno).first()
    if(request.method=='POST'):
        addSecondPage.first_name = request.form.get('first_name')
        addSecondPage.second_name = request.form.get('second_name')
        addSecondPage.email = request.form.get('email')
        addSecondPage.date_of_birth = request.form.get('date_of_birth')
        addSecondPage.contact_number = request.form.get('contact_number')
        addSecondPage.country = request.form.get('country')
        addSecondPage.state = request.form.get('state')
        addSecondPage.postle_code = request.form.get('postle_code')
        db.session.commit()
        return redirect('/payment-method-overview')
    return render_template('payment-method/payment-method-shipping-edit.html', addSecondPage=addSecondPage)   

@app.route('/payment-method-card/<string:sno>', methods=['GET', 'POST'])
def payment_method_card(sno):
    paymentMethod= payment_method.query.all() 
    no = 0
    for i in paymentMethod:
        no +=1 
    addSecondPage = payment_method.query.filter_by(sno =no).first()
    if(request.method=='POST'):
        addSecondPage.full_name = request.form.get('full_name')
        addSecondPage.card_number = request.form.get('card_number')
        addSecondPage.cvv = request.form.get('cvv')
        db.session.commit()
        sno = str(sno)
        return redirect('/payment-method-overview/'+sno)
    return render_template('payment-method/payment-method-card.html', sno=sno)   

@app.route('/payment-method-card-edit', methods=['GET', 'POST'])
def payment_method_card_edit():
    paymentMethod= payment_method.query.all() 
    sno = 0
    for i in paymentMethod:
        sno +=1 
    addSecondPage = payment_method.query.filter_by(sno =sno).first()
    if(request.method=='POST'):
        addSecondPage.full_name = request.form.get('full_name')
        addSecondPage.card_number = request.form.get('card_number')
        addSecondPage.cvv = request.form.get('cvv')
        db.session.commit()
        return redirect('/payment-method-overview')
    return render_template('payment-method/payment-method-card-edit.html', addSecondPage= addSecondPage)   


@app.route('/payment-method-overview/<string:sno>', methods=['GET', 'POST'])
def payment_method_overview(sno):
    paymentMethod= payment_method.query.all() 
    no = 0
    for i in paymentMethod:
        no +=1 
    addSecondPage = payment_method.query.filter_by(sno =no).first()
    shopping_card = add_shopping_card.query.filter_by(sno =sno).first()
    if(request.method=='POST'):
        sno = shopping_card.sno
        name = shopping_card.name
        price = shopping_card.price
        category = shopping_card.category
        sub_category = shopping_card.sub_category
        addSecondPage.product = f"sno = {sno}, name = {name}, price = {price}, category = {category}, sub_category = {sub_category}"
        db.session.commit()
        return redirect('/payment-method-finish')
    return render_template('payment-method/payment-method-overview.html', addSecondPage=addSecondPage, shopping_card=shopping_card, sno=sno)   

@app.route('/payment-method-finish')
def payment_method_finish():
    return render_template('payment-method/payment-method-finish.html')   





# Signin / signup
# will be come later 

@app.route('/shop09', methods=['GET', 'POST'])
def sign_in():
    if request.method=='POST':
        username = request.form.get('username')
        userpass = request.form.get('password')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            #set the session variable
            session['user'] = username
            return redirect('/dashboard-home')
        # email = request.form.get('email')
        # password = request.form.get('password')

        # user = user_data.query.filter_by(email=email).first()
        # if user:
        #     if check_password_hash(user.password, password):
        #         flash('Logged in successfully!', category='success')
        #         login_user(user, remember=True)
        #         return redirect('/')
        #     else:
        #         flash('Incorrect password, try again.', category='error')
        # else:
        #     flash('Email does not exist.', category='error')    
    return render_template('signin-signup/signin.html')   

# @app.route('/signup', methods=['GET', 'POST'])
# def sign_up():
#     error = ""
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             error= 'Email already exists.'
#         elif len(email) < 4:
#             error = 'Email must be greater than 3 characters.'
#         elif len(username) < 2:
#             error = 'First name must be greater than 1 character.'
#         elif password1 != password2:
#             error = 'Passwords don\'t match.'
#         elif len(password1) < 7:
#             error = 'Password must be at least 7 characters.'
#         else:
#             new_user = User(email=email, username=username, password=password1)
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             return redirect('/')
#     return render_template('signin-signup/signup.html', error=error)   








# delete category
@app.route("/delete-category/<string:sno>", methods = ['GET', 'POST'])
def delete_category(sno):
    category = add_category.query.filter_by(sno=sno).first()
    db.session.delete(category)
    db.session.commit()
    return redirect('/dashboard-category-view')
# delete special category
@app.route("/delete-special-category/<string:sno>", methods = ['GET', 'POST'])
def delete_special_category(sno):
    special_category = add_special_category.query.filter_by(sno=sno).first()
    db.session.delete(special_category)
    db.session.commit()
    return redirect('/dashboard-special-category-view')
# delete shop card category
@app.route("/delete-shop-card/<string:sno>", methods = ['GET', 'POST'])
def delete_shop_card(sno):
    shopping_card = add_shopping_card.query.filter_by(sno=sno).first()
    db.session.delete(shopping_card)
    db.session.commit()
    return redirect('/dashboard-shop-item-view')


# admin logout
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')










if __name__ == '__main__':
    app.run(debug=True)
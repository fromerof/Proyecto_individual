from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import render_template,request,redirect,flash,session,url_for
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_app.models.comment import Comment


@app.route('/')
def index():
    comments = Comment.get_allcomments()
    return render_template('index.html',comments=comments)

@app.route('/indexloggedin')
def indexloggedin():
    data = {
        "id": session['user_id']
    }
    comments = Comment.get_allcomments()
    return render_template('indexlogged.html',comments=comments,user = User.get_by_id(data))

@app.route('/add_user')
def add_user():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/add_user')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/iniciar_sesion')

@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = User.get_by_email(request.form)
    if not user_id:
        flash("Invalid Email/password")
        return redirect('/iniciar_sesion')
    if not bcrypt.check_password_hash(user_id.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/iniciar_sesion')
    session['user_id'] = user_id.id
    return redirect("/indexloggedin")

@app.route('/messages', methods=['POST'])
def messages():
    # if not Message.validate_message(request.form):
    #     return redirect('/')
    # user_id = User.get_by_email(request.form)
    # session['user_id'] = user_id.id
    data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "message": request.form["message"],
    }
    message = Message.message(data)
    return redirect('/indexloggedin')

@app.route('/comment', methods=['POST'])
def comment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "comment": request.form["comment"],
        "user_id":session['user_id']
    }
    comment = Comment.saveComment(data)
    return redirect('/indexloggedin')

@app.route('/edit/comment/<int:user_id>')
def edit_comment(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id":user_id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("editcomment.html",edit=Comment.get_one(data),user=User.get_by_id(user_data),comment=Comment.get_one(data))

@app.route('/update/comment/',methods=['POST'])
def update_comment():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "comment": request.form["comment"],
        "id": request.form['id']
    }
    Comment.update(data)
    return redirect('/indexloggedin')

@app.route('/delete/comment/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Comment.delete(data)
    return redirect('/indexloggedin')



# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id": session['user_id']
#     }
#     user = User.get_by_id(data)
#     tvshows = Tvshow.get_all()
#     return render_template("dashboard.html",user = user, tvshows = tvshows)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
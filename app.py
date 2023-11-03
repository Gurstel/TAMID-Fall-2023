from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from create_card import create_card

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    profession = StringField("profession", validators=[DataRequired()])
    hobby = StringField("hobby", validators=[DataRequired()])
    situation = StringField("situation", validators=[DataRequired()])
    difficulties = StringField("difficulties", validators=[DataRequired()])
    communication = StringField("communication", validators=[DataRequired()])
    additional = StringField("additional", validators=[DataRequired()])

    submit = SubmitField("Login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        profession = form.profession.data
        hobby = form.hobby.data
        situation = form.situation.data
        difficulties = form.difficulties.data
        communication = form.communication.data
        additional = form.additional.data

    #     if user and user.password == form.password.data:
    #         login_user(user)
    #         return redirect(url_for('secret'))

    #     print("wrong")
    #     flash('Invalid username or password')
        content = create_card(name = name,profession = profession, hobby = hobby, situation=situation,difficulties=difficulties,
        communication=communication,additional=additional)
        return render_template('secret.html', content=content)

    return render_template('login.html', form=form)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

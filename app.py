from flask import Flask, render_template, redirect, url_for, session, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from flask_session import Session
from create_card import create_card

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
app.config["SESSION_TYPE"] = "filesystem"  # Use filesystem-based sessions

Session(app)

# Form for user information


class InfoForm(FlaskForm):
    name = StringField("First Name")
    profession = StringField("Profession")
    hobby = StringField("Hobby")
    situation = StringField("Situation")
    difficulties = StringField("Difficulties")
    communication = StringField("Communication")
    additional = StringField("Additional")
    submit = SubmitField("Next")


# Form for background style selection


class BackgroundForm(FlaskForm):
    background_style = SelectField(
        "Background Style",
        choices=[
            ("style1", "Flowers"),
            ("style2", "Red Carpet"),
            ("style3", "Formal"),
        ],  # Add your styles here
    )
    submit = SubmitField("Create Card")


@app.route("/form", methods=["GET", "POST"])
def form():
    form = InfoForm()
    if form.validate_on_submit():
        # Save the form data to the session
        session["form_data"] = {
            name: field.data for name, field in form._fields.items() if field.data
        }
        return redirect(url_for("background"))

    return render_template("form.html", form=form)


@app.route("/background", methods=["GET", "POST"])
def background():
    form = BackgroundForm()
    if form.validate_on_submit():
        # Retrieve the saved form data
        form_data = session.get("form_data", {})
        # Add the selected background style to the form data
        form_data["background_style"] = form.background_style.data
        # Save the complete form data back to the session
        session["form_data"] = form_data
        # Redirect to the image serving route
        return redirect(url_for("create_card_route"))
    return render_template("background_form.html", form=form)


@app.route("/create_card")
def create_card_route():
    form_data = session.get("form_data", {})
    if form_data:
        image_io = create_card(**form_data)
        return send_file(image_io, mimetype="image/png", as_attachment=False)
    return "No card information provided", 400


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)

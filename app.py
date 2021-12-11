"""Flask Application for Paws Rescue Center."""
from flask import Flask, render_template, abort
from forms import SignUpForm, LoginForm, EditPetForm,GetPet
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
db = SQLAlchemy(app)

"""Model for Pets."""


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    bio = db.Column(db.String)
    posted_by = db.Column(db.String, db.ForeignKey('user.id'))


"""Model for Users."""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    pets = db.relationship('Pet', backref='user')


db.create_all()

# Create "team" user and add it to session
team = User(full_name="Pet  Team",
            email="team@petteam.co", password="adminpass")
db.session.add(team)

# Create all pets
lkd = Pet(name="lkd", bio="dfdfasdfdsf")

# Add all pets to the session
db.session.add(lkd)


# Commit changes in the session
try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
finally:
    db.session.close()


@app.route("/")
def homepage():
    """View function for Home Page."""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")


@app.route("/details/<int:pet_id>", methods=["POST", "GET"])
def pet_details(pet_id):
    #to show all the particualr pet details 
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.bio = form.bio.data
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("details.html", pet=pet, form=form, message="A Pet with this name already exists!") #someday repeates a pet name
    return render_template("details.html", pet=pet, form=form)

@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    if 'user' in session:
        pet = Pet.query.get(pet_id)
        if pet is None:
            abort(404, description="No Pet was Found with the given ID")
        db.session.delete(pet)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return redirect(url_for('homepage', _scheme='http', _external=True))
    else:
        abort(404, description="not allowed") 
        return render_template('details.html', form=form)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(full_name=form.full_name.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form, message="This Email already exists in the system! Please Login instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data, password=form.password.data).first()
        if user is None:
            return render_template("login.html", form=form, message="Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.id
            return render_template("login.html", message="Successfully Logged In!")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('homepage', _scheme='http', _external=True))


@app.route("/addpet", methods=["GET", "POST"])
def addnew():
    if 'user' in session:
        form=GetPet()
        if form.validate_on_submit():
            new_pet = Pet(name=form.name.data,bio=form.bio.data)
            db.session.add(new_pet)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return render_template("addpet.html", form=form, message="This pet already exists in the system! Please try again.")
            finally:
                db.session.close()
            return render_template("addpet.html", message="Successfully put up")
        return render_template("addpet.html", form=form)
    else:
        abort(404, description="not allowed")
        return render_template('addpet.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
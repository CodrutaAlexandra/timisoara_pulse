import os

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/timipulse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
SECRET_CODE = "CodSecret123"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    location = db.Column(db.String(150), nullable=True)
    date = db.Column(db.DateTime)
    description = db.Column(db.String(500))

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    hours = db.Column(db.String(100), nullable=False)
    # cui = db.Column(db.String(50), nullable=False)
    # image_file = db.Column(db.String(100), nullable=False, default='default.jpg')


@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        secret_code = request.form.get('secretCode')

        if secret_code != SECRET_CODE:
            return jsonify({"error": "Cod secret incorect"}), 403

        new_event = Event(
            name=request.form.get('name'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d'),
            description=request.form.get('description'),
            location=request.form.get('location', 'Nespecificat')
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({"success": True, "message": "Eveniment adăugat"})
    else:
        all_events = Event.query.all()
        return render_template('events.html', events=all_events)


@app.route('/')
def index():
    return render_template('index.html')

# Map Route
@app.route('/map')
def map():
    return render_template('map.html')

# Local Businesses Route
@app.route('/businesses', methods=['GET', 'POST'])
def businesses():
    if request.method == 'POST':
        # Extrage doar datele necesare din formular
        name = request.form.get('name')
        description = request.form.get('description')
        address = request.form.get('address')
        hours = request.form.get('hours')

        # Crează o instanță nouă pentru afacere fără CUI și imagine
        new_business = Business(
            name=name,
            description=description,
            address=address,
            hours=hours
        )
        # Adaugă și salvează afacerea în baza de date
        db.session.add(new_business)
        db.session.commit()
        return redirect(url_for('businesses'))
    else:
    # Pentru GET request, obține toate afacerile și le trimite la template
        all_businesses = Business.query.all()
        return render_template('businesses.html', businesses=all_businesses)


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


# # Multilingual support
# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(['en', 'ro', 'hu', 'de', 'sr'])

@app.route('/explore_3d')
def explore_3d():
    # Serve the 3D images for exploration
    return render_template('explore_3d.html', images=[])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creați tabelele în baza de date
    app.run(debug=True)



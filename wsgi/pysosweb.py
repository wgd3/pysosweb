from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort

app = Flask(__name__)

app.config.from_pyfile('pysosweb.cfg')
db = SQLAlchemy(app)

class rpmdb(db.Model):
	__tablename__ = 'rpms'
	id = db.Column('rpm_id', db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	version = db.Column(db.String(60))
	warning = db.Column(db.String(200))
	kcs = db.Column(db.Integer)

	def __init__(self, name, version, warning, kcs):
		self.name = name
		self.version = version
		self.warning = warning
		self.kcs = kcs

@app.route("/")
def hello():
    return render_template('list.html')

@app.route('/new')
def new():
    if request.method == 'POST':
        entry = rpmdb(request.form['name'],request.form['version'],request.form['warning'],request.form['kcs'])
	db.session.add(entry)
	db.session.commit()
	return redirect(url_for('list'))    

    return render_template('new.html')

if __name__ == "__main__":
    app.run()


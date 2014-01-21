from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort
from  datetime import date

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
	bz = db.Column(db.Integer)
	reporter = db.Column(db.String(15))
	report_time = db.Column(db.Date)

	def __init__(self, name, version, warning, kcs, bz, report_time, reporter):
		self.name = name
		self.version = version
		self.warning = warning
		self.kcs = kcs
		self.bz = bz
		self.report_time = report_time
		self.reporter = reporter

@app.route("/")
def list():
    return render_template('list.html',
			list = rpmdb.query.all())

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
	try:
		# Set time
		newDate = date.today()

		entry = rpmdb(request.form['name'],request.form['version'],request.form['warning'],request.form['kcs'],request.form['bz'],newDate.isoformat(),request.form['reporter'])
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('list'))    
	except Exception as e:
		flash("Something went wrong with your request")
		
    return render_template('new.html')

if __name__ == "__main__":
    app.run()


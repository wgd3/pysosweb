from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort, jsonify
from  datetime import date
#from wtforms import Form, TextField, IntegerField, validators

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
    
    error = None
    invalidKCS = False
    invalidBZ = False

    if request.method == 'POST':
	try:
		# Set time
		newDate = date.today()
		
		if request.form['kcs'] == '':
			invalidKCS = True

		if request.form['bz'] == '':
			invalidBZ = True


		entry = rpmdb(request.form['name'],request.form['version'],request.form['warning'],request.form['kcs'],request.form['bz'],newDate.isoformat(),request.form['reporter'])
		db.session.add(entry)
		db.session.commit()
		return redirect(url_for('list'))    
	except Exception as e:
		flash("Something went wrong with your request")
		
    return render_template('new.html')

@app.route('/rpm/<name>')
def rpm_overview(name):
	# Find each unique rpm in db
	distinct_rpms = rpmdb.query(rpms.name).distinct()
	
	# Make list to store all json objects
	jsonList = []
	# For each unique rpm
	for drpm in distinct_rpms:
		# Find each version
		tempStr = ""
		
		versions = rpmdb.query.filter_by(name=drpm.name).all()
		for v in versions:
			tempStr = tempStr + "'version':"+v.version+","
			# Find each warning
			for w in v.warning:
				tempStr = tempStr + "'warning':"+w+","

		print "String for current DB: " + tempStr
		jsonList.append(str("{"+tempStr+"}"))
	
	return render_template('overview.html',rpm=jsonify({'name':u'Test Package','version':u'1.2.3','warning':u'Test warning 1','warning',u'Test warning 2'}))


@app.route('/check/<rpm>/<version>')
def check(rpm, version):

	# Check user agent to decide between JSON data and HTML response
	userAgentString = request.headers.get('User-Agent')
	print "Found " + userAgentString +" as user agent."

	isJSONRequest = False
	if "python" in userAgentString:
		isJSONRequest = True

	validRPM = False
	query = rpmdb.query.filter_by(name=rpm).first()	

	if query is not None:
		print "Found valid rpm, switching to True"
		validRPM = True

	if validRPM:
		print "Setting version query"
		versionQuery = rpmdb.query.filter_by(name=rpm).all()
		for v in versionQuery:
			print "looking for matching version"
			if v.version == version:
				print "Found valid RPM AND valid version"
				# return template with version warnings
				return jsonify( { 'status': u'success','kcs':query.kcs,'bz':query.bz,'warning':query.warning } )
			else:
				print "Found valid RPM without a valid version"
				# return page saying version doesn't exist, but RPM is valid
				return jsonify( { 'status': u'fail - no entries' } )
	else:
		print "RPM not found in database"
		# return template with invalid RPM syntax
		return jsonify( { 'status':u'fail - invalid rpm'} )

	return redirect(url_for('list'))

#class WarningForm(Form):
#	name = StringField(u'Name', [validators.InputRequired()])
#	version = StringField(u'Version', [validators.InputRequired()])
#	warning = TextAreaField(u'Warninig', [validators.InputRequired()])
#	kcs = IntegerField(u'KCS', [])

if __name__ == "__main__":
    app.run()


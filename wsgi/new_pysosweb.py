from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, flash, url_for, redirect, render_template, abort, jsonify
from  datetime import date
#from wtforms import Form, TextField, IntegerField, validators

app = Flask(__name__)

app.config.from_pyfile('pysosweb.cfg')
db = SQLAlchemy(app)

class VWarning(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	version = db.relationship('Version', backref='warnings', lazy='dynamic')
	bz = db.Column(db.Integer)
	kcs = db.Column(db.Integer)
	reporter = db.Column(db.String(50))
	report_date = db.Column(db.DateTime)

class Version(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rpm_name = db.Column(db.String(50), db.ForeignKey('rpm.id'))
	version_number = db.Column(db.String(50))
	warnings = db.relationship('VWarning', backref='versions', lazy='dynamic')

	def __init__(self, 

class RPM(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	versions = db.relationship('Version', backref='rpm', lazy='dynamic')
	
	def __init__(self, name):
		self.name = name

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

@app.route('/rpm/<rpm_name>')
def rpm_overview(rpm_name):
	'''
	Need to pass 2 variables to the template: rpm (with name and version count), versions (with warnings and associated version number
	'''

	# Init variable
	summary = ""
	versions = []
	warnings = ""
	formattedVersions = []
	debugVersions = ''
	# Return all db rows with 'name' matching 'rpm_name'
	rpm_query = rpmdb.query.filter_by(name=rpm_name).all()

	# Add all versions
	for r in rpm_query:
		# find unique versions
		if r.version not in versions:
			print "Found version "+r.version+" not already in version list"
			versions.append(r.version)
	
	# find warnings for each version
	for v in versions:
		print "Looking for version "+v
		for r in rpm_query:
			print "Evaluating RPM "+r.name+" which has version "+r.version
			# Look for matching version number in each original db query
			if v in r.version:
				print "found entry for version "+v+" adding warning: "+r.warning
				warnings = warnings = "'"+r.warning+"',"
				print warnings
				
		summary = "{'version':u'"+v+"','warnings':["+warnings+"]}"
		print summary
		formattedVersions.append(summary)
	# for debugging
	debugStr = "["
	for s in formattedVersions:
		debugStr = debugStr + ","+s
	print "debugStr: " + debugStr	

	print str(formattedVersions)
		
	# Below is test data for use during development
	test_rpm = {'name':u'Test Packages','versions':u'3'}

	rpm_versions = [{'version':u'1.0','warnings':['test warning 1','test warning 2']},{'version':u'2.0','warnings':['test warning 1','test warning 2','test warning 3','test warning 4','test warning 5']}]
	
	return render_template('overview.html',rpm=rpm_name,versions=formattedVersions)


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
			print "looking for matching version: "+str(v.version)
			if v.version == version:
				print "Found valid RPM AND valid version"
				# return template with version warnings
				return jsonify( { 'status': u'success','kcs':v.kcs,'bz':v.bz,'warning':v.warning } )
		
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


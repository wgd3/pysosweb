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
   
    validRecord = True
	 
    if request.method == 'POST':
	try:
		# Form validation and error reporting via flashed messages

		# Set time automatically
		newDate = date.today()
		
		pkgName = ' '
		if request.form['name'] == '':
			flash(u'Not a valid package name','error')
			# attempting to break the loop, preventing the record from being added
			validRecord=False
		else:
			pkgName = request.form['name']

		pkgVer = ' '
		if request.form['version'] == '':
			flash(u'Not a valid package version','error')
			# attempting to break the loop, preventing the record from being added
			validRecord = False
		else:
			pkgVer = request.form['version']

		pkgWarning = ' '
		if request.form['warning'] == '':
			flash(u'No warning entered','error')
			validRecord=False
		else:
			pkgWarning = request.form['warning']

		kcsNumber = ' '
		if request.form['kcs'] == '':
			#invalidKCS = True
			flash(u'Did not find valid KCS number','error')
			validRecord = False
		else:
			kcsNumber = request.form['kcs']

		bzNumber = ' '
		if request.form['bz'] == '':
			#invalidBZ = True
			flash(u'Did not find vald BZ number','error')
			validRecord = False
		else:
			bzNumber = request.form['bz']

		if validRecord:
			entry = rpmdb(pkgName,pkgVer,pkgWarning,kcsNumber,bzNumber,newDate.isoformat(),request.form['reporter'])
			db.session.add(entry)
			db.session.commit()
			flash(u'Added record successfully','message')
		else:
			flash(u'One or more errors found, not saving record','error')
	# if the above fails, then something outside of invalid fields has happened	
	except Exception as e:
		flash(u'Unknown exception caught, not adding record','error')
        
	# no matter what, reload the page with whatever flashed messages have been reported
	return render_template('new.html')
    
    # check to see if this is the initial request to the page (no flahsed messages)
    elif request.method == 'GET':		
        # Passing no flashes to page, just render template
	return render_template('new.html')

    # for safety's sake I'm leaving this in here, though there shouldn't ever be a reason for this line to run
    return render_template('new.html')

@app.route('/update/<rpm_name>/<new_name>/<version>/<warning>')
def update(rpm_name,new_name,version,warning):
	'''
	Take variables in URL
	'''
	try:
		rpm_record = rpmdb.query.filter_by(name=rpm_name).first()
		if rpm_record is None:
			print "No records returned for package " + rpm_name
			flash(u'Can\'t update record, no rpm named '+rpm_name+' was found.','error')
		else:
			print "Found record for package " + rpm_name
			# updating only the fields that are not null
			# this means the url could look like '/update/rpm_name/null/new_version/new_warning'
			if new_name != 'null':
				# If a new name is found (not null) then update the record's 'name' field with the new name
				rpm_record.name = new_name
				print "Updating rpm name..."
			if version != 'null':
				rpm_record.version = version
				print "Updating rpm version..."
			if warning != 'null':
				rpm_record.warning = warning
				print "Updating rpm warning..."
			
			db.session.commit()
			flash(u'Updated package '+rpm_name+'\'s properties successfully','message')
	except:
		print "Something went wrong trying to update the database"
		flash(u'Something went wrong when trying to update the record for '+rpm_name,'error')

	return redirect(url_for('list'))


@app.route('/delete/<rpm_name>')
def delete(rpm_name):
	'''
	Need to find a way to prevent scripting in such a way that the database could be emptied
	'''
	try:
		package_record = rpmdb.query.filter_by(name=rpm_name).first()
		if package_record is None:
			print "No records returned from your query using package named: " + rpm_name
			flash(u'Did not delete any records, nothing matched your query for '+rpm_name,'error')
		else:
			print "Found record for package: " + package_record.name
			db.session.delete(package_record)
			db.session.commit()
			flash(u'Successfully deleted the package '+rpm_name+' from the database.','message')
	except:
		print "Ran into issue querying database"
		flash(u'Ran into issue connecting to database, no action taken','error')
		
	return redirect(url_for('list'))

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


if __name__ == "__main__":
    app.run()


from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('pysosweb.cfg')
db = SQLAlchemy(app)

class rpmdb(db.Model):
	__tablename__ = 'rpms'
	id = db.Column('rpm_id', db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	version = db.Column(db.String(60))
	warning = db.Column(db.String(200))

	def __init__(self, name, version, warning)
		self.name = name
		self.version = version
		self.warning = warning

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()


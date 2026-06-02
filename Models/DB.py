import os
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


class DB(object):
	"""Initialize mysql database """
	host = os.environ.get("DB_HOST", "localhost")
	user = os.environ.get("DB_USER", "root")
	password = os.environ.get("DB_PASSWORD", "")
	db = os.environ.get("DB_NAME", "lms")
	table = ""
	port = int(os.environ.get("DB_PORT", 18945))

	def __init__(self, app):
		app.config["MYSQL_DATABASE_HOST"] = self.host;
		app.config["MYSQL_DATABASE_USER"] = self.user;
		app.config["MYSQL_DATABASE_PASSWORD"] = self.password;
		app.config["MYSQL_DATABASE_DB"] = self.db;
		app.config["MYSQL_DATABASE_PORT"] = self.port;

		self.mysql = MySQL(app, cursorclass=DictCursor)

	def cur(self):
		return self.mysql.get_db().cursor()

	def query(self, q):
		h = self.cur()
	
		if (len(self.table)>0):
			q = q.replace("@table", self.table)

		h.execute(q)

		return h

	def commit(self):
		self.query("COMMIT;")
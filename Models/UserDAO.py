class UserDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "users"


	def list(self):
		users = self.db.query("select users.id,users.name,users.email,users.bio,users.mob,users.lock,users.created_at,count(reserve.book_id) as books_owned from users LEFT JOIN reserve ON reserve.user_id=users.id GROUP BY reserve.user_id").fetchall()

		return users

	def getById(self, id):
		q = self.db.query("select * from users where id='{}'".format(id))

		user = q.fetchone()

		return user

	def getUsersByBook(self, book_id):
		q = self.db.query("select * from users LEFT JOIN reserve ON reserve.user_id = users.id WHERE reserve.book_id={}".format(book_id))

		user = q.fetchall()

		return user

	def getByEmail(self, email):
		q = self.db.query("select * from users where email='{}'".format(email))

		user = q.fetchone()

		return user

	def add(self, user):
		name = user['name']
		email = user['email']
		password = user['password']

		q = self.db.query("INSERT INTO users (name, email, password) VALUES('{}', '{}', '{}');".format(name, email, password))
		
		return q


	def update(self, user, _id):
		name = user['name']
		email = user['email']
		password = user['password']
		bio = user['bio']

		q = self.db.query("UPDATE users SET name = '{}', email='{}', password='{}', bio='{}' WHERE id={}".format(name, email, password, bio, _id))
		
		return q

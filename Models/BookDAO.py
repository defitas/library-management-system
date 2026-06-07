class BookDAO():
	def __init__(self, DAO):
		self.db = DAO
		self.db.table = "books"

	def delete(self, id):
		q = self.db.query("DELETE FROM books where id={}".format(id))

		return q


	def reserve(self, user_id, book_id):
		if not self.available(book_id):
			return "err_out"

		q = self.db.query("INSERT INTO reserve (user_id, book_id) VALUES('{}', '{}');".format(user_id, book_id))
		
		self.db.query("UPDATE books set count=count-1 where id={};".format(book_id))

		return q

	def getBooksByUser(self, user_id):
		q = self.db.query("select * from books left join reserve on reserve.book_id = books.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBooksCountByUser(self, user_id):
		q = self.db.query("select count(reserve.book_id) as books_count from books left join reserve on reserve.book_id = books.id where reserve.user_id={}".format(user_id))

		books = q.fetchall()

		print(books)
		return books

	def getBook(self, id):
		q = self.db.query("select * from books where id={}".format(id))

		book = q.fetchone()

		print(book)
		return book

	def available(self, id):
		book = self.getById(id)
		count = book['count']

		if count < 1:
			return False

		return True

	def getById(self, id):
		q = self.db.query("select * from books where id='{}'".format(id))

		book = q.fetchone()

		return book

	def list(self, availability=1):
		query = "SELECT * FROM books"
		if availability == 1:
			query += " WHERE availability = %s"
			books = self.db.query(query, (availability,))
		else:
			books = self.db.query(query)
		
		return books.fetchall()

	def getReserverdBooksByUser(self, user_id):
		query="select concat(book_id,',') as user_books from reserve WHERE user_id={}".format(user_id)
		
		books = self.db.query(query)
		
		books = books.fetchone()


		return books

	def search_book(self, name, availability=1):
		query="select * from books where name LIKE '%{}%'".format(name)

		# Usually when no-admin user query for book
		if availability==1: query= query+"  AND availability={}".format(availability)

		q = self.db.query(query)
		books = q.fetchall()
		
		return books
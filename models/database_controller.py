import sqlite3
from .metaclasses.singleton import SingletonMeta

class UniqueError(Exception):
	def __str__(self):
		return 'Ошибка, такая запись уже есть'
	
class DatabaseConfig:
	unique_error = 'UNIQUE constraint failed'

	create_table = '''CREATE TABLE IF NOT EXISTS panels (
					id INTEGER PRIMARY KEY,
					url TEXT NOT NULL,
					api_key TEXT NOT NULL,
					work BOOLEAN DEFAULT true,
					valid_api_key BOOLEAN DEFAULT true)'''

	add_panel = '''INSERT INTO panels (url, api_key) VALUES (?, ?)'''
	edit_panel = '''UPDATE panels SET url=?, api_key=?, work=?, valid_api_key=? WHERE id=?'''
	edit_panel_work = '''UPDATE panels SET work=? WHERE id=?'''
	edit_panel_valid_api_key = '''UPDATE panels SET valid_api_key=? WHERE id=?'''
	get_panels = '''SELECT * FROM panels'''
	get_panel_by_id = '''SELECT * FROM panels WHERE id=?'''
	delete_panel_by_id = '''DELETE FROM panels WHERE id=?'''
	get_panels_by_work = '''SELECT * FROM panels WHERE work=?'''
	get_panels_by_worked_keys_sites = '''SELECT * FROM panels WHERE valid_api_key=?'''


class Database(metaclass=SingletonMeta):
	__classobj = None
	__db_name = 'panels.db'
	__connection: sqlite3.Connection = None
	__cursor: sqlite3.Cursor = None



	def __del__(self) -> None:
		try: Database.close()
		except sqlite3.ProgrammingError: pass

	@classmethod
	def connect(cls) -> None:
		if cls.__connection is None:
			cls.__connection = sqlite3.connect(cls.__db_name, check_same_thread=False)
			print(f'Создал connection, теперь {cls.__connection=}')
	
	@classmethod
	def cursor(cls) -> None:
		if cls.__connection:
			if cls.__cursor is None:
				cls.__cursor = cls.__connection.cursor()
				print(f'Создал cursor, теперь {cls.__cursor=}')
	
	@classmethod
	def close(cls) -> None:
		if cls.__connection is not None:
			if cls.__cursor is not None:
				cls.__cursor = cls.__cursor.close()
				print(f'Закрыл cursor, теперь {cls.__cursor=}')
			cls.__connection = cls.__connection.close()
			print(f'Закрыл connection, теперь {cls.__connection=}')
	
	@classmethod
	def execute(cls, *args) -> list | None:
		if cls.__connection is not None and cls.__cursor is not None:
			res = cls.__cursor.execute(*args)
			for key in ['CREATE', 'INSERT', 'UPDATE', 'DELETE']:
				if key in args[0]:
					cls.__connection.commit()
			if 'SELECT' in args[0]:
				return res.fetchall()
	
	@classmethod
	def create_table(cls) -> None:
		cls.execute(DatabaseConfig.create_table)

	def add_panel(self, url, api_key) -> None:
		try:
			Database.execute(DatabaseConfig.add_panel, (url.strip(), api_key.strip(),))
		except Exception as err:
			if DatabaseConfig.unique_error in str(err):
				raise UniqueError
			raise err

	def edit_panel(self, url, api_key, id, work, valid_api_key) -> None:
		try:
			Database.execute(DatabaseConfig.edit_panel, (url.strip(), api_key.strip(), work, valid_api_key, id))
		except Exception as err:
			if DatabaseConfig.unique_error in str(err):
				raise UniqueError
			raise err

	def get_panels(self) -> list:
		return Database.execute(DatabaseConfig.get_panels)
	
	def get_panel_by_id(self, id) -> list:
		try:
			return Database.execute(DatabaseConfig.get_panel_by_id, (id,))
		except Exception as err:
			print(f"Неизвестная ошибка при получении записи по id({id=}) из бд\n", err)
	
	def delete_panel_by_id(self, id) -> None:
		try:
			Database.execute(DatabaseConfig.delete_panel_by_id, (id,))
		except Exception as err:
			print(f"Неизвестная ошибка при получении записи по id({id=}) из бд\n", err)

	def get_panels_by_work(self, is_work=False) -> list:
		try:
			return Database.execute(DatabaseConfig.get_panels_by_work, (is_work, ))
		except Exception as err:
			print(f"Неизвестная ошибка при получении нерабочих панелей из бд\n", err)
	
	def get_panels_by_worked_keys_sites(self, is_worked_keys_sites=False) -> list:
		try:
			return Database.execute(DatabaseConfig.get_panels_by_worked_keys_sites, (is_worked_keys_sites, ))
		except Exception as err:
			print(f"Неизвестная ошибка при получении нерабочих панелей из бд\n", err)
	
		
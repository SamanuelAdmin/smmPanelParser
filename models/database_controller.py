import sqlite3
from models.metaclasses.singleton import SingletonMeta

class UniqueError(Exception):
	def __str__(self):
		return 'Ошибка, такая запись уже есть'
	

class DatabaseConfig:
	@classmethod
	def handle_value(cls, v):
		if isinstance(v, bool): return int(v)
		elif isinstance(v, str): return f'"{v.strip()}"'
		else: return v

	@classmethod
	def generate_params_string(cls, **kwargs) -> str:
		res = ', '.join([f'{k}={cls.handle_value(v)}' for k, v in kwargs.items() if v != None])
		return res

class PanelsDatabaseConfig:
	unique_error = 'UNIQUE constraint failed'

	create_table = '''CREATE TABLE IF NOT EXISTS panels (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					url TEXT NOT NULL,
					api_key TEXT NOT NULL,
					work BOOLEAN DEFAULT true,
					valid_api_key BOOLEAN DEFAULT true)'''

	add_panel = '''INSERT INTO panels (url, api_key) VALUES (?, ?)'''
	# edit_panel = '''UPDATE panels SET url=?, api_key=?, work=?, valid_api_key=? WHERE id=?'''
	edit_panel = '''UPDATE panels SET {params} WHERE id={id}'''
	edit_panel_work = '''UPDATE panels SET work=? WHERE id=?'''
	edit_panel_valid_api_key = '''UPDATE panels SET valid_api_key=? WHERE id=?'''
	get_panels = '''SELECT * FROM panels'''
	get_panel_by_id = '''SELECT * FROM panels WHERE id=?'''
	delete_panel_by_id = '''DELETE FROM panels WHERE id=?'''
	get_panels_by_work = '''SELECT * FROM panels WHERE work=?'''
	get_panels_by_worked_keys_sites = '''SELECT * FROM panels WHERE valid_api_key=?'''

class ServicesDatabaseConfig:
	create_table = '''CREATE TABLE IF NOT EXISTS services (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					service_id INTEGER NOT NULL,
					url TEXT NOT NULL,
					name TEXT NOT NULL,
					max INTEGER NOT NULL,
					min INTEGER NOT NULL,
					price REAL DEFAULT 0,
					currency TEXT DEFAULT "$",
					currency_to_usd REAL DEFAULT 0,
					dns TEXT NOT NULL,
					average_time TEXT DEFAULT "no average",
					balance REAL DEFAULT "не смог получить")'''
	
	get_services = '''SELECT * FROM services'''

	@staticmethod
	def generate_query_by_data(data: dict, query_type: str = 'insert'):
		'''
		:param data: Dict
		:param query_data: "insert" / "select" / "select_by"
		'''
		if query_type == 'insert':
			columns = ', '.join(data.keys())
			placeholders = ', '.join([f":{key}" for key in data.keys()])
			return f'INSERT INTO services ({columns}) VALUES ({placeholders})'
		elif query_type == 'select_by':
			where_clause = " AND ".join([f"{key} = :{key}" for key in data.keys()])
			
			return f'SELECT * FROM services WHERE {where_clause}'
		
	get_service_by = 'SELECT * FROM services WHERE {column}={value}'

	# add_service = f'''INSERT INTO services ({", ".join([column for column in columns])}) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
	# add_service = f'''
	# INSERT INTO services ({', '.join([column for column in columns])}) 
	# VALUES ({[', '.join(['?' for _ in columns])]})'''

	edit_service = '''
	UPDATE services SET {params} 
	WHERE id={id}
	'''


class Database(metaclass=SingletonMeta):
	__classobj = None
	__db_name = 'database.db'
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
		cls.execute(PanelsDatabaseConfig.create_table)
		cls.execute(ServicesDatabaseConfig.create_table)

	def add_panel(self, url: str, api_key: str) -> None:
		try:
			Database.execute(
				PanelsDatabaseConfig.add_panel,
				(url.strip(), api_key.strip(), )
			)
		except Exception as err:
			raise err
		
	def add_service(self, data: dict) -> None:
		try:
			Database.execute(ServicesDatabaseConfig.generate_query_by_data(data, 'insert'), data)
		except Exception as err:
			raise err
		
	def get_service_by(self, **kwargs):
		try:
			return Database.execute(ServicesDatabaseConfig.generate_query_by_data(kwargs, 'select_by'), kwargs)
		except Exception as err:
			raise err
	# def edit_service(self, data: dict) -> None:
	# 	try:
	# 	except Exception as err:

		
	def edit_panel(self, id: int, url: str=None, api_key: str=None, work: bool=None, valid_api_key: bool=None) -> None:
		try:
			Database.execute(
				PanelsDatabaseConfig.edit_panel.format(
					params=DatabaseConfig.generate_params_string(url=url, api_key=api_key, work=work, valid_api_key=valid_api_key),
					id=id
				)
			)
		except Exception as err:
			raise err

	def get_panels(self) -> list:
		return Database.execute(PanelsDatabaseConfig.get_panels)
	
	def get_panel_by_id(self, id) -> list:
		try:
			return Database.execute(PanelsDatabaseConfig.get_panel_by_id, (id,))
		except Exception as err:
			print(f"Неизвестная ошибка при получении записи по id({id=}) из бд\n", err)
	
	def delete_panel_by_id(self, id) -> None:
		try:
			Database.execute(PanelsDatabaseConfig.delete_panel_by_id, (id,))
		except Exception as err:
			print(f"Неизвестная ошибка при получении записи по id({id=}) из бд\n", err)

	def get_panels_by_work(self, is_work=False) -> list:
		try:
			return Database.execute(PanelsDatabaseConfig.get_panels_by_work, (is_work, ))
		except Exception as err:
			print(f"Неизвестная ошибка при получении нерабочих панелей из бд\n", err)
	
	def get_panels_by_worked_keys_sites(self, is_worked_keys_sites=False) -> list:
		try:
			return Database.execute(PanelsDatabaseConfig.get_panels_by_worked_keys_sites, (is_worked_keys_sites, ))
		except Exception as err:
			print(f"Неизвестная ошибка при получении нерабочих панелей из бд\n", err)

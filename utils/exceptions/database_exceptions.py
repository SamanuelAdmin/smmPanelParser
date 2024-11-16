class UniqueError(Exception):
	def __str__(self):
		return 'Ошибка, такая запись уже есть'
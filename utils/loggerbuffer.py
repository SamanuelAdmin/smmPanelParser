from abc import abstractmethod, ABC
import os


class ILoggerBuffer(ABC):
	@abstractmethod
	def info(self, message : str) -> None: pass

	@abstractmethod
	def error(self, message : str) -> None: pass

	@abstractmethod
	def getLogsAsString(self) -> str: pass


class LoggerBuffer(ILoggerBuffer):
	def __init__(self, filename, logdir='logs'):
		self.filename = os.path.join(logdir, filename)
		self.buffer = []

		if not os.path.exists(os.path.dirname(self.filename)):
			os.makedirs(os.path.dirname(self.filename))

		with open(self.filename, 'w') as file: file.write('')


	def info(self, message : str) -> None:
		self.buffer.append(message)

		with open(self.filename, 'a', encoding='utf-8') as file:
			file.write(message)


	def error(self, message : str) -> None:
		# self.buffer.append(('error', message))
		pass

	def getLogsAsString(self):
		return '\n'.join(self.buffer).replace('\n\n\n', '\n')

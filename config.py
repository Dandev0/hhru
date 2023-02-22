from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import logging


bot = Bot(token='6126808491:AAFbN4ASJShRVoXHCWudHbasEitjsQzAh5k')
dp = Dispatcher(bot, storage=MemoryStorage())                      #memory_storaage нужен для хранения машины состояний


logging.basicConfig(level=logging.INFO, filename="bot_selenium.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")
py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)


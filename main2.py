import time
from config import dp, py_logger
from aiogram.types import Message
from aiogram import executor
import asyncio
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium import webdriver
from selenium.webdriver.common.by import By
from test import main


@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    await message.answer(text='Запускаю спам hh.ru')
    await login()


async def get_chrome_options():
    options = chrome_options()
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('_ignore_local_proxy')
    options.add_argument('--headless')
    return options


async def get_webdriver():
    try:
        options = await get_chrome_options()
        driver = webdriver.Chrome(options=options, executable_path=r"chromedriver_linux64/chromedriver")
        url = 'https://hh.ru/account/login'
        driver.get(url)
        return driver
    except Exception as ex:
        py_logger.warning(ex)


async def login():
    from resume import send_resumes
    try:
        driver = await get_webdriver()
        time.sleep(1)
        driver.find_element(By.NAME, "login").send_keys("dan02050121@gmail.com")
        driver.find_element(By.XPATH, "//button[@class='bloko-button bloko-button_kind-primary']").click()
        time.sleep(10)
        code_email = main()
        driver.find_element(By.NAME, "otp-code-input").send_keys(code_email)
        driver.find_element(By.CSS_SELECTOR, ".verification-submit").click()
        time.sleep(3)
        await send_resumes(driver=driver)
    except Exception as ex:
        py_logger.warning(ex)


if __name__ == '__main__':
    py_logger.warning('Bot is starting!')
    loop = asyncio.new_event_loop()
    loop.run_until_complete(executor.start_polling(dp, skip_updates=True))
    loop.run_forever()

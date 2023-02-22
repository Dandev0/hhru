from selenium.webdriver.common.by import By
from main2 import get_webdriver
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from config import py_logger


class Locators:
    message_about_me = '//*[@id="RESPONSE_MODAL_FORM_ID"]/div/div/textarea'
    button_fal = '//*[@id="RESPONSE_MODAL_FORM_ID"]/div[6]/div[2]/button'  # Локатор кнопки отправить с формой ответов.
    button_fall2 = '/html/body/div[11]/div/div[1]/div[4]/button' #еще 1 дебильная форма без выбора резюме
    button_send_resume = "(//button[@form='RESPONSE_MODAL_FORM_ID'][1])"
    close_frame = '/html/body/div[11]/div/div[2]'
    close_frame2 = '/html/body/div[12]/div/div[2]'


async def check_elem_in_list(driver, locator):
    try:
        return driver.find_element(By.XPATH, locator)
    except NoSuchElementException:
        return False


async def send_resumes(driver):
    url = f'https://perm.hh.ru/search/vacancy?schedule=remote&search_field=name&search_field=description&enable_snippets=false&salary=100000&text=python+developer&ored_clusters=true&page=0'
    driver.get(url)
    time.sleep(1)
    locator = Locators()
    start_url = driver.current_url
    for i in range(1, 35):
        try:
            time.sleep(2)
            locator_send_on_main_page = fr"(//a[@class='bloko-button bloko-button_kind-primary bloko-button_scale-small'])[{i}]"
            send_on_main_page = await check_elem_in_list(driver, locator_send_on_main_page)
            if send_on_main_page is not False:
                send_on_main_page.click()
                time.sleep(1.5)
                button_fal2 = await check_elem_in_list(driver, locator.button_fall2)
                after_click_url = driver.current_url
                if start_url == after_click_url:
                    if button_fal2 is False:
                        send_resume = await check_elem_in_list(driver, locator.button_send_resume)
                        loc_button_fal = await check_elem_in_list(driver, locator.button_fal)
                        if loc_button_fal is False:
                            if send_resume is not False:
                                driver.find_element(By.XPATH,
                                                    f'//*[@id="RESPONSE_MODAL_FORM_ID"]/div/div/div[2]/div[2]/div/div/label/span[1]').click()
                                time.sleep(1)
                                loc_message_about_me = await check_elem_in_list(driver, locator.message_about_me)
                                if loc_message_about_me is not False:
                                    loc_message_about_me.send_keys(
                                        "Целеустремленный и ответственный. В it кручусь 3 года, а данное сообщение и резюме направлено моим скриптом, который состоит из следущих технологий: selenium, aiogram, google api's. А также настроено хорошее логгирование.")

                                    time.sleep(2)
                                driver.find_element(By.XPATH,
                                                    locator.button_send_resume).click()
                                time.sleep(1.5)

                        else:
                            driver.back()

                    else:
                        time.sleep(1)
                        loc_cl1 = await check_elem_in_list(driver, locator.close_frame)
                        time.sleep(.6)
                        if loc_cl1 is not False:
                            loc_cl1.click()
                        else:
                            driver.find_element(By.XPATH, locator.close_frame2).click()

                else:
                    driver.back()


        except Exception as ex:
            py_logger.warning(ex)

    driver.close()


from faker import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

fake = Faker()

URL = 'http://95.182.122.183:3000/login'

email_l = (By.CSS_SELECTOR, '#email')
password_l = (By.CSS_SELECTOR, '#password')
alert_sms = (By.XPATH, '//div[@role="alert"]')
enter_btn = (By.XPATH, '//button[@type="submit"]')

class Login:
    def __init__(self, driver, url):
        self.driver = driver
        self.fake = Faker()
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def fill_email(self, email_value=''):
        field = self.driver.find_element(*email_l)
        field.clear()
        field.send_keys(email_value)

    def fill_password(self, password):
        field = self.driver.find_element(*password_l)
        field.clear()
        field.send_keys(password)

    def click_enter_button(self, timeout: int = 10):
        button = wait(self.driver, timeout).until(EC.element_to_be_clickable(enter_btn))
        button.click()


    def is_enter_button_enabled(self):
        try:
            btn = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            return btn.is_enabled()
        except NoSuchElementException:
            return False

    def is_clickable(self, locator: tuple, timeout: int = 10) -> WebElement:
        return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def is_enter_button_visible(self):
        return self.driver.find_element(By.XPATH, '//button[@type="submit"]').is_displayed()

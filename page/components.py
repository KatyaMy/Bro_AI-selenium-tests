from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

URL = 'http://95.182.122.183/sign_up'


class Register:
    def __init__(self, driver):
        self.driver = driver
        self.fake = Faker()

    def open_page(self):
        self.driver.get(URL)

    def generate_fixed_length_email(self, length):
        name = self.fake.user_name()
        while len(name) < length:
            name += self.fake.user_name()
        email = name[:length] + '@gmail.com'
        return email

    def generate_user_data(self, email_length, password_length, empty_field=None):
        email = '' if empty_field == 'email' else self.generate_fixed_length_email(email_length)
        password = '' if empty_field == 'password' else self.fake.password(password_length, upper_case=True,
                                                                           digits=True, special_chars=True)
        name = '' if empty_field == 'name' else self.fake.first_name()
        return email, password, name

    @staticmethod
    def transform_email(email, uppercase_email=False):
        if uppercase_email:
            return email.upper()
        return email

    def registration_new_user(self, wait, email_length, password_length, empty_field=None, uppercase_email=False):
        email, password, name = self.generate_user_data(email_length, password_length, empty_field)
        email = self.transform_email(email, uppercase_email)

        self.driver.find_element(By.ID, 'email').send_keys(email)
        self.driver.find_element(By.ID, 'pass1').send_keys(password)
        self.driver.find_element(By.ID, 'pass2').send_keys(password)
        self.driver.find_element(By.ID, 'name').send_keys(name)
        register_btt = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='ui button blue']")))
        register_btt.click()
        wait.until(EC.url_changes(self.driver.current_url))

        return email, password, name

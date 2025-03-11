from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class RegistrationPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def fill_email(self, email):
        self.driver.find_element(By.ID, 'email').send_keys(email)

    def fill_password(self, password):
        self.driver.find_element(By.ID, 'pass1').send_keys(password)
        self.driver.find_element(By.ID, 'pass2').send_keys(password)

    def fill_name(self, name):
        self.driver.find_element(By.ID, 'name').send_keys(name)

    def click_register_button(self):
        register_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@class='ui button blue']")
        ))
        register_btn.click()

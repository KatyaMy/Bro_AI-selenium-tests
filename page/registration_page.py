from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def fill_email(wait, email):
    field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    field.clear()
    field.send_keys(email)


def fill_password(wait, password):
    pass1 = wait.until(EC.presence_of_element_located((By.ID, 'pass1')))
    pass2 = wait.until(EC.presence_of_element_located((By.ID, 'pass2')))
    pass1.clear()
    pass1.send_keys(password)
    pass2.clear()
    pass2.send_keys(password)


def fill_name(wait, name):
    field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    field.clear()
    field.send_keys(name)


def click_register_button(wait):
    register_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'ui button blue')]")
    ))
    register_btn.click()


def get_alert_element(wait, locator):
    return wait.until(
        EC.visibility_of_element_located(locator)
    )

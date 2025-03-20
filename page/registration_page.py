from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
fake = Faker()

def fill_email(wait, email):
    field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    field.clear()
    field.send_keys(email)


def fill_password(wait, password_1, password_2):
    pass1 = wait.until(EC.presence_of_element_located((By.ID, 'pass1')))
    pass2 = wait.until(EC.presence_of_element_located((By.ID, 'pass2')))
    pass1.clear()
    pass1.send_keys(password_1)

    pass2.clear()
    pass2.send_keys(password_2)


def fill_name(wait, name):
    field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    field.clear()
    field.send_keys(name)


def click_register_button(wait):
    register_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class, 'ui button blue')]")
    ))
    register_btn.click()


def get_error_message(wait, locator):
    return wait.until(
        EC.visibility_of_element_located(locator)
    )


def empty_password_field(wait, password, field_empty=True):
    pass1 = wait.until(EC.presence_of_element_located((By.ID, 'pass1')))
    pass2 = wait.until(EC.presence_of_element_located((By.ID, 'pass2')))

    pass1.clear()
    pass2.clear()

    if field_empty:
        pass1.send_keys('')
        pass2.send_keys(password)
    else:
        pass1.send_keys(password)
        pass2.send_keys('')


def enter_length(length: int) -> str:
    return fake.password(length=length, upper_case=True, digits=True, special_chars=True)

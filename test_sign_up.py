from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


URL = 'http://95.182.122.183/sign_up'
URL_LOGIN = 'http://95.182.122.183/login'

fake = Faker()
email = fake.email()
password = fake.password(length=9, upper_case=True, digits=True, special_chars=True)
name = fake.first_name()

"""Регистрация нового пользователя с использованием фикстуры"""
def test_registration_new_user(driver, wait, registration_data):
    driver.get(URL)

    driver.find_element(By.ID, 'email').send_keys(registration_data['email'])
    driver.find_element(By.ID, 'pass1').send_keys(registration_data['password'])
    driver.find_element(By.ID, 'pass2').send_keys(registration_data['password'])
    driver.find_element(By.ID, 'name').send_keys(registration_data['name'])

    register_btt = driver.find_element(By.XPATH, "//button[@class='ui button blue']")
    wait.until(EC.element_to_be_clickable(register_btt)).click()

    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""Регистрация нового пользователя с использованием fake"""
def test_registration_user(driver, wait):
    driver.get(URL)

    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass1').send_keys(password)
    driver.find_element(By.ID, 'pass2').send_keys(password)
    driver.find_element(By.ID, 'name').send_keys(name)
    print(email, password, name)

    register_btt = driver.find_element(By.XPATH, "//button[@class='ui button blue']")
    wait.until(EC.element_to_be_clickable(register_btt)).click()
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'

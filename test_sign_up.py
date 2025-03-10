from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from components import Register, generate_fixed_length_email

URL = 'http://95.182.122.183/sign_up'
URL_LOGIN = 'http://95.182.122.183/login'

fake = Faker()
password = fake.password(length=9, upper_case=True, digits=True, special_chars=True)
name = fake.first_name()

"""Регистрация нового пользователя с использованием фикстуры (валидные данные)"""
def test_registration_new_user(driver, wait, registration_data):
    driver.get(URL)

    driver.find_element(By.ID, 'email').send_keys(registration_data['email'])
    driver.find_element(By.ID, 'pass1').send_keys(registration_data['password'])
    driver.find_element(By.ID, 'pass2').send_keys(registration_data['password'])
    driver.find_element(By.ID, 'name').send_keys(registration_data['name'])

    register_btt = driver.find_element(By.XPATH, "//button[@class='ui button blue']")
    wait.until(EC.element_to_be_clickable(register_btt)).click()

    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""Регистрация нового пользователя с использованием fake(валидные данные)"""
def test_registration_user(driver, wait):
    email = generate_fixed_length_email(length=8)
    driver.get(URL)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass1').send_keys(password)
    driver.find_element(By.ID, 'pass2').send_keys(password)
    driver.find_element(By.ID, 'name').send_keys(name)
    print(email, password, name)

    register_btt = driver.find_element(By.XPATH, "//button[@class='ui button blue']")
    wait.until(EC.element_to_be_clickable(register_btt)).click()
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-002 Регистрация с заполненными валидными данными обязательными полями и пустым полем Имя"""
def test_registration_user_with_empty_filed(driver, wait):
    email = generate_fixed_length_email(length=40)
    print(f'=========== длина в символах {len(email)} <============')
    driver.get(URL)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass1').send_keys(password)
    driver.find_element(By.ID, 'pass2').send_keys(password)
    driver.find_element(By.ID, 'name').send_keys()
    register_btt = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ui button blue']")))
    register_btt.click()
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-003 Регистрация с заполненными валидными данными  полями и email состоящий из 6 символов"""
def test_registration_user_with_length_6_simbols(driver, wait):
    register = Register(driver)
    register.open_page()
    register.registration_new_user(wait, email_length=6, password_length=9)
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'

import time
import pytest
from faker import Faker
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page.components import Register
from data import generate_fixed_length_email, alert_mms
from page.registration_page import RegistrationPage

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
    # print(f'=========== длина в символах {len(email)} <============')
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
    register.registration_new_user(wait, email_length=6, password_length=9, uppercase_email=False, empty_field=False)
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-004 Регистрация с заглавными латинскими символами в email"""
def test_registration_new_user_with_upper_case_email(driver, wait):
    register = Register(driver)
    register.open_page()
    register.registration_new_user(wait, email_length=6, password_length=9, uppercase_email=True, empty_field=False)
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-005 Регистрация с email, включающий "_" """
@pytest.mark.parametrize('email, user_password, user_name', [
    ('Test_User_07@hotmail.com', '123HyNcVb', 'ViktorCi')
])
def test_registration_new_user_with_underline_in_email_field(driver, wait, email, user_password, user_name):
    page = Register(driver)
    page.open_page()
    register_field = RegistrationPage(driver, wait)
    register_field.fill_email(email)
    register_field.fill_password(user_password)
    register_field.fill_name(user_name)
    register_field.click_register_button()
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'

"""TC-NN-006 Ввод цифр в аккаунтной части поля "Email";
TC-NN-007 Ввод цифр в доменной части поля "Email" """
@pytest.mark.parametrize('user_data', [
    {'email':'Test_User_09@gmail.com', 'password':'1244HyNcVb', 'name':''},
    {'email':'TestUser_YU@80hotmail.com', 'password':'1223UomVb', 'name':'KarlaP'}
])
def test_registration_new_user_with_underline_in_email_field(driver, wait, user_data):
    page = Register(driver)
    page.open_page()
    register_field = RegistrationPage(driver, wait)
    register_field.fill_email(user_data['email'])
    register_field.fill_password(user_data['password'])
    register_field.fill_name(user_data['name'])
    register_field.click_register_button()
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-009 Регистрация с заполненными валидными данными  полями и email состоящий из 51 символа"""
@pytest.mark.negative
def test_registration_new_user_with_51_simbols(driver, wait):
    register = Register(driver)
    register.open_page()
    register.registration_new_user(wait, email_length=51, password_length=9, uppercase_email=False, empty_field=False)
    alert = driver.find_element(By.CSS_SELECTOR, '.field:nth-of-type(1) .mt-2.text-sm.text-rose-600.italic').text
    assert alert == 'Не более 50 символов', f"Ожидали ограничение в 50 символов, но получили: {alert}"
    assert "50" in alert, f"Ожидали ограничение в 50 символов, но получили: {alert}"



"""TC-NN-010 Регистрация с кириллицей в доменной части email 
TC-NN-011   Регистрация с кириллицей в аккаунтной части email
TC-NN-012	Регистрация с пробелом в начале email 
TC-NN-013	Регистрация с email  без "." в доменной части  
TC-NN-014	Регистрация с пробелом перед @ в email 
TC-NN-015	Регистрация с пробелом в доменной части email 
TC-NN-016	Регистрация с пробелом в конце email 
TC-NN-018	Регистрация c некорректным форматом email ( без @ ) """
@pytest.mark.negative
def test_registration_new_user_with_ru_domain(driver, wait, create_user_data):
    page = Register(driver)
    page.open_page()
    register_field = RegistrationPage(driver, wait)
    register_field.fill_email(create_user_data['email'])
    register_field.fill_password(create_user_data['password'])
    register_field.fill_name(create_user_data['name'])
    register_field.click_register_button()

    incorrect_mail = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='field'][1] //div"))).text

    alert_success = 'Вы успешно зарегистрировались'
    assert incorrect_mail == 'Укажите корректный mail', (
        f"Ожидалось сообщение об ошибке, но получили: {alert_success}")


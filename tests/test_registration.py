import time

import pytest
from faker import Faker
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from conftest import driver
from data import generate_fixed_length_email
from locators import *
from page.components import Register
from page.registration_page import get_error_message, fill_name, fill_password, fill_email, click_register_button, \
    empty_password_field, enter_length

fake = Faker()

URL = 'http://95.182.122.183:3000/sign_up'
URL_LOGIN = 'http://95.182.122.183:3000/login'

password_f = fake.password(length=9, upper_case=True, digits=True, special_chars=True)
name_f = fake.name()

"""Регистрация нового пользователя с использованием фикстуры (валидные данные)"""


@pytest.mark.positive
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
def test_registration_new_user(driver, wait, registration_data):
    driver.get(URL)
    driver.find_element(By.ID, 'email').send_keys(registration_data['email'])
    driver.find_element(By.ID, 'pass1').send_keys(registration_data['password'])
    driver.find_element(By.ID, 'pass2').send_keys(registration_data['password'])
    driver.find_element(By.ID, 'username').send_keys(registration_data['name'])
    register_btt = driver.find_element(By.XPATH, "//button[@class='ui button blue']")
    wait.until(EC.element_to_be_clickable(register_btt)).click()

    # Проверка наличия ошибки
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""Регистрация нового пользователя с использованием fake(валидные данные)"""


@pytest.mark.positive
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
def test_registration_user(driver, wait):
    email = generate_fixed_length_email(length=8)
    driver.get(URL)
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass1').send_keys(password_f)
    driver.find_element(By.ID, 'pass2').send_keys(password_f)
    driver.find_element(By.ID, 'username').send_keys(name_f)
    print(email, password_f, name_f)

    register_btt = driver.find_element(By.XPATH, "//button[@class='ui button blue']")
    wait.until(EC.element_to_be_clickable(register_btt)).click()

    # Проверка наличия ошибки
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-002 Регистрация с заполненными валидными данными обязательными полями и пустым полем Имя(email <=50)"""


@pytest.mark.negative
def test_registration_with_empty_name_field(driver, wait):
    email = generate_fixed_length_email(length=40)
    # print(f'=========== длина в символах {len(email)} <============')
    page = Register(driver)
    page.open_page()
    fill_email(wait, email)
    fill_password(wait, password_1=password_f, password_2=password_f)
    fill_name(wait, '')
    click_register_button(wait)

    # Проверка наличия ошибки

    alert_message = driver.find_element(By.XPATH, "//div[contains(text(),'Это поле обязательно')]").text
    assert 'Это поле обязательно' in alert_message, f"Ожидалось сообщение об ошибке, но появилось : {URL_LOGIN}"


"""TC-NN-003 Регистрация с заполненными валидными данными  полями и email состоящий из 6 символов"""


@pytest.mark.positive
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
def test_registration_with_length_6_symbols(driver, wait):
    register = Register(driver)
    register.open_page()
    register.registration_new_user(wait, email_length=6, password_length=9, uppercase_email=False, empty_field=False)

    # Проверка наличия ошибки
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-004 Регистрация с заглавными латинскими символами в email"""


@pytest.mark.positive
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
def test_registration_with_upper_case_email(driver, wait):
    register = Register(driver)
    register.open_page()
    register.registration_new_user(wait, email_length=6, password_length=9, uppercase_email=True, empty_field=False)

    # Проверка наличия ошибки
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-005 Регистрация с email, включающий "_" """


@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
@pytest.mark.parametrize('email, user_password, user_name', [
    ('Test_User_07@hotmail.com', '123HyNcVb', 'ViktorCi')
])
def test_registration_with_underline_in_email_field(driver, wait, email, user_password, user_name):
    page = Register(driver)
    page.open_page()
    fill_email(wait, email)
    fill_password(wait, user_password, user_password)
    fill_name(wait, user_name)
    click_register_button(wait)
    wait.until(EC.url_changes(driver.current_url))

    # Проверка наличия ошибки
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-006 Ввод цифр в аккаунтной части поля "Email";
TC-NN-007 Ввод цифр в доменной части поля "Email" """


@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
@pytest.mark.parametrize('user_data', [
    {'email': 'Test_User_09@gmail.com', 'password': '1244HyNcVb', 'name': 'Anna'},
    {'email': 'TestUser_YU@80hotmail.com', 'password': '1223UomVb', 'name': 'KarlaP'}
])
def test_registration_with_number_in_email_field(driver, wait, user_data):
    page = Register(driver)
    page.open_page()
    fill_email(wait, user_data['email'])
    fill_password(wait, user_data['password'], user_data['password'])
    fill_name(wait, user_data['name'])
    click_register_button(wait)

    # Проверка наличия ошибки
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-009 Регистрация с заполненными валидными данными  полями и email состоящий из 51 символа"""


@pytest.mark.negative
def test_registration_with_51_symbols(driver, wait):
    register = Register(driver)
    register.open_page()
    register.registration_new_user(wait, email_length=51, password_length=9, uppercase_email=False, empty_field=False)

    # Проверка наличия ошибки
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
def test_registration_with_ru_domain(driver, wait, create_user_data):
    page = Register(driver)
    page.open_page()
    fill_email(wait, create_user_data['email'])
    fill_password(wait, create_user_data['password'], create_user_data['password'])
    fill_name(wait, create_user_data['name'])
    click_register_button(wait)

    # Проверка наличия ошибки
    incorrect_mail_massage = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='field'][1] //div"))).text

    assert 'Укажите корректный mail' in incorrect_mail_massage, (
        f"Ожидалось сообщение 'Укажите корректный mail', но получили: {massage_about_registration}")

    with pytest.raises(TimeoutException):
        wait.until(EC.presence_of_element_located(massage_about_registration))


"""TC-NN-017	Регистрация со спецсимволами в email  ( #$%)"""


@pytest.mark.positive
def test_registration_with_special_symbols(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, email='@Test_user%@gmail.com')
    fill_password(wait, password_1=password_f, password_2=password_f)
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    error_message = driver.find_element(By.XPATH, "// div[contains(text(), 'Укажите корректный mail')]").text
    assert 'Укажите корректный mail' in error_message, (f"Ожидалось сообщение об ошибке {error_message}, "
                                                        f"но появилось: {URL_LOGIN}")


"""TC-NN-019 Попытка регистрации с незаполенным полем email"""


@pytest.mark.negative
def test_registration_fails_with_empty_email_field(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, email='')
    fill_password(wait, password_1=password_f, password_2=password_f)
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    alert_element = get_error_message(wait, empty_email_field)
    assert alert_element.is_displayed()


"""TC-NN-020 Пустое поле "Пароль" при заполненном поле "email" """


@pytest.mark.negative
def test_registration_fails_with_missing_password(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, email=fake.email())
    empty_password_field(wait, password=fake.password(), field_empty=True)
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    alert_element = driver.find_element(*empty_pass1_field).text
    assert 'Это поле обязательно' in alert_element


"""TC-NN-021 Попытка регистрации с незаполенным полем Подтвердите пароль """


@pytest.mark.negative
def test_registration_fails_with_empty_password_confirmation(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, email=fake.email())
    empty_password_field(wait, fake.password(), field_empty=False)
    fill_name(wait, name=fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    alert_element = driver.find_element(*empty_pass2_field).text
    assert 'Это поле обязательно' in alert_element


"""TC-NN-022	Попытка регистрации с несовпадающими символами в поле  Подтвердите пароль """


@pytest.mark.negative
def test_registration_fails_with_mismatched_passwords(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, fake.email())
    fill_password(wait, password_1=fake.password(), password_2=fake.password())
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    alert_text = driver.find_element(*error_password_mismatch).text
    assert 'Пароли не совпадают' in alert_text, "Ожидалось сообщение об ошибке при отсутствии password_1"


"""TC-NN-023 Попытка регистрации с 7 символами в поле Пароль """


@pytest.mark.negative
def test_register_with_short_password(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, fake.email())
    fill_password(wait, password_1=enter_length(7), password_2=enter_length(7))
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    error_message = get_error_message(wait, error_password_message).text
    assert "Не менее 8 символов" in error_message, f"Ожидалось сообщение об ошибке, но не получилось: {error_message}"


"""TC-NN-026 Ввод кириллицы в поле Пароль"""
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
def test_signup_with_cyrillic_password(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, fake.email())
    fill_password(wait, password_1="ФЫВП88ГувыфШ", password_2="ФЫВП88ГувыфШ")
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'



"""TC-NN-027 Ввод цифр в поле "Пароль"""
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
def test_registration_with_digits_only_password(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, fake.email())
    fill_password(wait, password_1=12345678890, password_2=12345678890)
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-028 Ввод пароля с пробелом"""
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
def test_registration_with_password_space(driver, wait):
    page = Register(driver)
    page.open_page()
    fill_email(wait, fake.email())
    fill_password(wait, password_1='jikhytv65  bghh', password_2='jikhytv65  bghh')
    fill_name(wait, fake.name())
    click_register_button(wait)

    # Проверка наличия ошибки
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'


"""TC-NN-029 Регистрация с 50 символами в поле Пароль"""
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
def test_registration_with_50_characters_password(driver, wait):
    page = Register(driver)
    page.open_page()
    page.registration_new_user(wait, email_length= 10, password_length=50)
    # Проверка наличия ошибки
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'

"""TC-NN-030	Регистрация с 49 символами в поле Пароль """
@pytest.mark.xfail(reason="Баг, регистрация не происходит после ввода корректных данных")
@pytest.mark.positive
def test_registration_with_49_characters_password(driver, wait):
    page = Register(driver)
    page.open_page()
    page.registration_new_user(wait, email_length= 10, password_length=49)
    # Проверка наличия ошибки
    wait.until(EC.url_changes(driver.current_url))
    assert driver.current_url == URL_LOGIN, 'Некорректно переданные данные'



"""TC-NN-030	Регистрация с 51 символами в поле Пароль """
@pytest.mark.negative
def test_registration_with_51_characters_password(driver, wait):
    page = Register(driver)
    page.open_page()
    page.registration_new_user(wait, email_length= 10, password_length=51)
    # Проверка наличия ошибк
    error_message = get_error_message(wait, error_message_51).text
    assert "Не более 50 символов" in error_message, f"Ожидалось сообщение об ошибке, но не получилось: {error_message}"

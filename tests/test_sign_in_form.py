import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from data import user_name, user_password, alert_mms, expect_alert_text, incorrect_name, incorrect_password
from page.login_page import Login
from faker import Faker

fake = Faker()
URL = 'http://95.182.122.183:3000/login'
alert_sms = (By.XPATH, '//div[@role="alert"]')


# NOTE: Positive: Check login
@pytest.mark.xfail(reason="Баг, вход не происходит после ввода корректных данных")
def test_check_correct_login(driver, wait):
    page = Login(driver, url=URL)
    page.open()
    page.fill_email(email_value=user_name)
    page.fill_password(password=user_password)
    page.click_enter_button()
    alert_txt = wait.until(
        EC.visibility_of_element_located(alert_sms))
    assert alert_txt.text == alert_mms, '_Not correct login or password'


# NOTE: Negative: Check user using incorrect data
@pytest.mark.xfail
def test_check_incorrect_login(driver, wait):
    page = Login(driver, url=URL)
    page.open()
    page.fill_email(email_value=incorrect_name)
    page.fill_password(password=user_password)
    page.click_enter_button()
    actual_alert_text = wait.until(
        EC.visibility_of_element_located(alert_sms))
    assert actual_alert_text.text == expect_alert_text, 'You are login'


# NOTE: Negative: Check password using incorrect data
@pytest.mark.xfail
def test_check_incorrect_password(driver, wait):
    page = Login(driver, url=URL)
    page.open()
    page.fill_email(email_value=user_name)
    page.fill_password(password=incorrect_password)
    page.click_enter_button()
    actual_alert_text = wait.until(
        EC.visibility_of_element_located(alert_sms))
    assert actual_alert_text.text == expect_alert_text, 'You are login'


'''TC-NN-036 Пустые поля e-mail и пароль'''


@pytest.mark.negative
def test_sign_in_with_empty_email(driver):
    page = Login(driver, url=URL)
    page.open()
    page.fill_email()
    page.fill_password(password=user_password)
    assert not page.is_enter_button_enabled(), "Ошибка! Кнопка 'Войти' активировалась при пустом email!"

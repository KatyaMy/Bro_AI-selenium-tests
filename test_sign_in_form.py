import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from data import user_name, user_password, alert_mms, expect_alert_text, incorrect_name, incorrect_password

URL = 'http://95.182.122.183/login'

email = (By.CSS_SELECTOR, '#email')
password = (By.CSS_SELECTOR, '#pass')
submit_bt = (By.XPATH, '//button[@type="submit"]')
alert_sms = (By.XPATH, '//div[@role="alert"]')

#NOTE: Positive: Check login
def test_check_correct_login(driver, wait):
    driver.get(URL)
    # driver.delete_all_cookies()
    # driver.refresh()
    driver.find_element(*email).send_keys(user_name)
    driver.find_element(*password).send_keys(user_password)
    driver.find_element(*submit_bt).click()
    alert_txt = wait.until(
        EC.visibility_of_element_located(alert_sms))
    assert alert_txt.text == alert_mms, '_Not correct login or password'

# NOTE: Negative: Check user using incorrect data
@pytest.mark.xfail
#FIXME
def test_check_incorrect_login(driver, wait):
    driver.get(URL)
    # driver.delete_all_cookies()
    # driver.refresh()
    driver.find_element(*email).send_keys(incorrect_name)
    driver.find_element(*password).send_keys(user_password)
    driver.find_element(*submit_bt).click()
    actual_alert_text = wait.until(
        EC.visibility_of_element_located(alert_sms))
    assert actual_alert_text.text == expect_alert_text, 'You are login'

#NOTE: Negative: Check password using incorrect data
#FIXME
@pytest.mark.xfail
def test_check_incorrect_password(driver, wait):
    driver.get(URL)
    # driver.delete_all_cookies()
    # driver.refresh()
    driver.find_element(*email).send_keys(user_name)
    driver.find_element(*password).send_keys(incorrect_password)
    driver.find_element(*submit_bt).click()
    actual_alert_text = wait.until(
        EC.visibility_of_element_located(alert_sms))
    assert actual_alert_text.text == expect_alert_text, 'You are login'
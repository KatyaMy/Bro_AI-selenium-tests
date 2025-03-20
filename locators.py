from selenium.webdriver.common.by import By

empty_email_field = By.XPATH, "//div[@class='field'][1]/div"
empty_pass1_field = By.XPATH, "//div[@class='field'][2]/div"
empty_pass2_field = By.XPATH, "//div[@class='field'][3]/div"
# mistake_pass_mms = By.XPATH, "//div[@class='field'][3]/div"
error_password_mismatch = By.XPATH, '//div[contains(text(),"Пароли не совпадают")]'

# //div[contains(text(),"Это поле обязательно")]
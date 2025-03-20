from selenium.webdriver.common.by import By

empty_email_field = By.XPATH, "//div[@class='field'][1]/div"
empty_pass1_field = By.XPATH, "//div[@class='field'][2]/div"
empty_pass2_field = By.XPATH, "//div[@class='field'][3]/div"
# mistake_pass_mms = By.XPATH, "//div[@class='field'][3]/div"
error_password_mismatch = By.XPATH, '//div[contains(text(),"Пароли не совпадают")]'
error_password_message = By.XPATH, '(//div[contains(text(),"Не менее 8 символов")])[1]'
massage_about_registration = By.XPATH, "//div[contains(text(), 'Вы успешно зарегистрировались')]"
# //div[contains(text(),"Это поле обязательно")]
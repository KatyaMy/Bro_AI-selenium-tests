from faker import Faker

fake = Faker()

# correct data
user_name = 'tests_2@gmail.com'
user_password = '12345678'
alert_mms = 'Вы успешно залогинились'
alert_success = 'Вы успешно зарегистрировались'

# incorrect data
incorrect_name = 'tests_not_2@gmail.com'
incorrect_password = '863DetyQA'
expect_alert_text = 'Неверный логин или пароль'


def generate_fixed_length_email(length):
    name = fake.user_name()
    while len(name) < length:
        name += fake.user_name()
    email = name[:length] + '@gmail.com'
    return email




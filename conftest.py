import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.wait import WebDriverWait

fake = Faker()



@pytest.fixture(scope="session")
def options():
    options = Options()
    options.add_argument('--window-size=1920,1080')
    options.headless = False
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options


@pytest.fixture(scope="session")
def driver(options):
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture()
def wait(driver):
    wait = WebDriverWait(driver, timeout=25)
    return wait



@pytest.fixture
def registration_data():
    """Для проверки конкретных данных"""
    return {'email': 'TestNeW_0@mail.com',
            'password': 'HuTc5658',
            'name': 'User_00'}


@pytest.fixture()
def fake_new_user():
    fake.email()
    fake.password()
    fake.user_name()

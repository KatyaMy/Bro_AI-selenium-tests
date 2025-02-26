import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    # for selenium
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument('--headless=new')
    options.add_argument("--lang=en")
    if os.environ.get("CI_RUN"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

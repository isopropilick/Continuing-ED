from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
import pytest
import logging
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG  # 10
    INFO = logging.INFO  # 20
    WARNING = logging.WARNING  # 30
    ERROR = logging.ERROR  # 40
    CRITICAL = logging.CRITICAL  # 50

def console_logger(name: str, level: LogLevel) -> logging.Logger:
    logger = logging.getLogger(f"__{name}__")
    logger.setLevel(level.value)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level.value)
    formatter = logging.Formatter(
        "%(levelname)s - %(asctime)s - %(name)s - %(message)s",
        datefmt="%m/%d/%y %I:%M:%S%p",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger



def selectors(selector):
	s = {
	'search_field' : '//*[@title="Search"]',
	'google_search_button' : '//input[@aria-label="Google Search"]',
	'weather_container' : '//*[@id="wob_wc"]',
	'selected_units' : '//*[@id="wob_wc"]//*[@class="vk_bk wob-unit"]/span',
	'temperature' : '//*[@id="wob_wc"]//span[@id="wob_tm"]'
	}
	return s[selector]
c_logger = console_logger(name="result", level=LogLevel.INFO)

@pytest.fixture
def d():
	d = webdriver.Firefox()
	d.get("https://www.google.com/search?hl=en")
	
	yield d
	d.close()

#Test to check if the temperature is presented as int and not float
def testWebOne(d):
	d.find_element(By.XPATH, selectors('search_field')).send_keys('Weather today'+Keys.ESCAPE)
	WDW(d, 10).until(EC.element_to_be_clickable((By.XPATH, selectors('google_search_button'))))
	d.find_element(By.XPATH, selectors('google_search_button')).click()
	temp = d.find_element(By.XPATH, selectors('temperature')).text
	c_logger.info(f"Result: {temp}")
	assert '.' not in temp and int(temp) <= 49

#Test to check if celsius is the default unit
def testWebTwo(d):
	d.find_element(By.XPATH, selectors('search_field')).send_keys('Weather today'+Keys.ESCAPE)
	WDW(d, 10).until(EC.element_to_be_clickable((By.XPATH, selectors('google_search_button'))))
	d.find_element(By.XPATH, selectors('google_search_button')).click()
	units = d.find_element(By.XPATH, selectors('selected_units')).text
	assert "C" in units


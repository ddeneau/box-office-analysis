from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

source_url = r'https://www.fandango.com/sonic-the-hedgehog-218659/movie-overview'

chrome_options = Options()

chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path=r'/Users/Danny/Downloads/chromedriver', options=chrome_options)

xpath = r'//*[@id="page"]/div[1]/div[1]/div[2]/div/div[1]/section[1]/ul/li[5]/div/a[1]/span[2]'

driver.get(source_url)

try:
    element = driver.find_element_by_xpath(xpath)
except NoSuchElementException:
    print("Error finding element for")

print(element.text)




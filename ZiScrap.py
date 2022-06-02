from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urljoin
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

GOOGLE_FORM_LINK = "https://forms.gle/ubmMifuVWampsuMz5"

WEB_URL = 'https://www.zillow.com/id/?searchQueryState=%7B"pagination"%3A%7B"currentPage"%3A8%7D%2C"usersSearchTerm"%3A"ID"%2C"mapBounds"%3A%7B"west"%3A-126.55781178125%2C"east"%3A-101.72871021875%2C"south"%3A38.81999874480323%2C"north"%3A51.656862607183%7D%2C"regionSelection"%3A%5B%7B"regionId"%3A20%2C"regionType"%3A2%7D%5D%2C"isMapVisible"%3Afalse%2C"filterState"%3A%7B"sort"%3A%7B"value"%3A"globalrelevanceex"%7D%2C"ah"%3A%7B"value"%3Atrue%7D%7D%2C"isListVisible"%3Atrue%2C"mapZoom"%3A6%7D'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=1440,1440')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def get_elements_list():
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, "html.parser")
    return soup.select("ul li article")


def get_all_elements():
    driver.get(WEB_URL)
    time.sleep(4)
    element_list = []
    # Pagination and fetch data.(Up to page 4 for now to avoid capticha verification)
    for page in range(1, 3):
        if page == 1:
            for _ in range(20):
                webdriver.ActionChains(driver).key_down(Keys.TAB).perform()
        for _ in range(120):
            webdriver.ActionChains(driver).key_down(Keys.ARROW_DOWN).perform()
        element_list.extend(get_elements_list())
        page_list = driver.find_elements_by_css_selector(".search-pagination a")[1:-1]
        page_list[page].click()
        time.sleep(2)

    elements_dic = {}
    for n in range(len(element_list)):
        address = element_list[n].select_one(".list-card-addr").getText()
        price = \
            element_list[n].select_one(".list-card-price").getText().split("/")[0].split("+")[0].replace("$", "").split(
                " ")[
                0]
        link = element_list[n].select_one(".list-card-link").get("href")
        # Get absolute path
        link = urljoin(WEB_URL, link)
        elements_dic.update({n: {"address": f"{address}", "price": f"{price}", "link": f"{link}"}})
    print(elements_dic)
    return elements_dic


# Fill out the form.
def input_form(elements_dic):
    driver.get(GOOGLE_FORM_LINK)
    for element in elements_dic.values():
        address = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))

        price = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        link = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        submit_button = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div'
        )

        address.send_keys(f"{element['address']}")
        price.send_keys(f"{element['price']}")
        link.send_keys(f"{element['link']}")
        submit_button.click()
        submit_another_response_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
        submit_another_response_btn.click()


zillow_elements = get_all_elements()
input_form(zillow_elements)

driver.quit()
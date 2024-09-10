import json
import time
from typing import Dict

from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_info(url) -> Dict:
	information = {}
	try:
		browser.get(url)
		about = WebDriverWait(browser, 10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='mu5_27']"))
		)

		infos = about.find_elements(By.XPATH, "./div")
		name = browser.find_element(By.XPATH, "//h1[@class='pm1_27 tsHeadline550Medium']")
		name = name.text
		print(name)

		for info in infos:
			header = info.find_element(By.XPATH, "./div[1]//*[text()]")
			value = info.find_element(By.XPATH, "./div[2]//*[text()]")

			header = header.text
			value = value.text

			information[header] = value

		print(information)
	except Exception:
		pass
	return information


options = webdriver.FirefoxOptions()
options.add_argument("--private")
# options.set_preference("network.proxy.type", 1)
# options.set_preference("network.proxy.socks", "127.0.0.1")
# options.set_preference("network.proxy.socks_port", 9080)
# options.set_preference("network.proxy.socks_remote_dns", False)
browser = webdriver.Firefox(options=options)

browser.get("https://www.ozon.ru/category/smartfony-15502/")
browser.implicitly_wait(5)
button = browser.find_element(By.ID, 'reload-button')
button.click()

pages = browser.find_elements(By.XPATH, "//div[@class='']/a[contains(@class, 'e4q') and @href]")
page_urls = []
phone_links_by_page = []

for page in pages[:5]:
	try:
		page_url = page.get_attribute("href")
		page_urls.append(page_url)
	except:
		pass

for page_url in page_urls:
	browser.get(page_url)

	browser.execute_script("window.scrollBy(0, document.body.scrollHeight);")
	browser.implicitly_wait(3)
	time.sleep(3)
	browser.execute_script("window.scrollBy(0, document.body.scrollHeight);")

	phone_links = WebDriverWait(browser, 10).until(
		EC.presence_of_all_elements_located((By.XPATH, "//div[@class='jn5_23']//a[@href]"))
	)
	phone_links = [phone_link.get_attribute("href") for phone_link in phone_links]
	phone_links_by_page.append(phone_links)

print(phone_links_by_page)

for i, phone_links in enumerate(phone_links_by_page):
	phone_infos = []
	for phone_link in phone_links:
		info = extract_info(phone_link)
		phone_infos.append(info)

	with open(f"{i}.json", "w") as f:
		json.dump(phone_infos, f)

input()

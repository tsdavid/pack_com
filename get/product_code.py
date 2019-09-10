# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import lxml.html
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import urllib.robotparser
import urllib.parse
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import urllib.robotparser
import urllib.parse
import cssselect


def download(url, headers=None, user_agent='wswp', proxy=None, num_retries=2):
	print('Downloading: ', url)
	headers = {'User-agent': user_agent}
	request = Request(url, headers=headers)
	opener = urllib.request.build_opener()
	if proxy:
		proxy_params = {urllib.request.urlparse(url).scheme:proxy}
		opener.add_handler(urllib.request.ProxyHandler(proxy_params))
	try:
		html = urlopen(request).read().decode('utf-8')
	except HTTPError as e:
		print("Download error: ", e.reason)
		html = None
		if num_retries >0 :
			if hasattr(e, 'code') and 500 <= e.code < 600:
				# 5XX HTTP 오류 시 재시도
				return download(url, num_retries -1)
	return html




# driver = webdriver.Chrome('./chromedriver.exe')

area_list = ["A", "B", "J", 'D', "E", "G", "C", "F", "K"]

class HANA_WORK:
	def __init__(self):
		self.driver = webdriver.Chrome('../chromedriver.exe', service_args=["--verbose", "--log-path=C:\\Users\\ipack\\pack_com\\qc1.log"])
		# service_args = chrome webdriver logging
		self.css = self.driver.find_elements_by_css_selector
		self.xpath = self.driver.find_elements_by_xpath
		self.class_name = self.driver.find_elements_by_class_name
		
		# URL SECTION
		self.area_url = "http://www.hanatour.com/asp/booking/productPackage/pk-11000.asp?area="
		# PATH SECTION
		# code_path[0] = 각 code , code_path[1] = 하단 지나가는 버튼
		self.code_path = ('div.result_list > ul > li', 'div.paginate > a')

	def check_delay(self, targets):
		"""
		현재 element가 crwal 가능한 상태인지 확인
		:param targest: webelemnet list
		:return: Boolean
		"""
		# check element available
		try:
			check = targets[0].is_enabled()
		except IndexError:
			check = False
		while check is False:
			# move down, make move
			import numpy as np
			Y = [200, 400, 600, 800, 1000, 1200]
			trial = np.random.choice(Y, 1)  # Y에서 무작위 추출
			self.driver.execute_script("window.scrollTo(0," + str(trial) + ")")
			try:
				check = targets[0].is_enabled()
			except IndexError:
				check = False
			if check is True:
				break

		return True

	def enter_url(self, keyword, url = None):
		"""
		url로 이동하는 함수
		페이지마다 기본 url 이 다를 수 있다.
		area 말고 city로 진입해야하는가?
		그렇다면 area에 맞는 city로 진입해야함
		:param area: area 정보
		:return:
		"""
		if url is None:
			self.driver.get(self.area_url + str(keyword))

		if url is not None:
			self.driver.get(url + str(keyword))

	def get_code(self, file):
		"""
		1차 상품 별 code를 가져오는 함수
		:return: code list by area
		"""
		codes = {}
		while True:
			# delay check
			targets = self.css(self.code_path[0])
			self.check_delay(targets)
			# li crwal
			for target in targets:
				words = target.text.split()
				for word in words:
					if word == 'MD추천':
						words.remove(word)
				idx = words[0]      # dic 의 key
				codes[idx] = {
					'url': 'http://www.hanatour.com/asp/booking/productPackage/pk-11001.asp?pkg_mst_code=AVP130' + idx,
					'words': words,
				}

			# move to next page
			self.css(self.code_path[1])[-2].click()
			# check the duplication
			com = self.css(self.code_path[0])[-1].text.split()

			if words[0] == com[0]:
				break

		# save pickle file
		import pickle
		with open(str(file)+'.pickle', 'wb') as pick:
			pickle.dump(codes, pick)

		return None

	def package_code(self, area):
		"""
		product > package product
		get package product code
		:param area:
		:return:
		"""

		# import pickle file with fit the area
		file_name = str(area) + '.pickle'
		with open('../get/' + file_name, 'rb') as file:
			import pickle
			data = pickle.load(file)

		# URL LIST
		codes = list(data.keys())
		url = """http://www.hanatour.com/asp/booking/productPackage/pk-11001.asp?pkg_mst_code="""
		"""for code in codes"""
		for code in codes:
			self.driver.get(url+code)
			# Check Delay
			targets = self.css('#new_pkg_list > tbody > tr')
			self.check_delay(targets)
			while True:
				"""while pages"""
				for target in targets:
					# Do Staff
					# enter url and get url, code
					target.find_elements_by_css_selector('td')[-3].click()
					self.driver.switch_to_window(self.driver.window_handles[1])
					package_code_target = self.css('div.pdt_code > strong.code_num')
					self.check_delay(package_code_target)
					package_code = package_code_target[0].text

					try:
						current_url = self.driver.current_url
					except IndexError as e:
						print(e , 'occur')
						while True:
							current_url = self.driver.current_url
							if package_code == current_url.split('pkg_code=')[1]:
								break

					self.driver.close()
					self.driver.switch_to_window(self.driver.window_handles[0])

					# cwal
					obj = target.find_elements_by_css_selector('td')
					depart_arrive = obj[1].text.split('\n')
					departure, arrival = depart_arrive[0], depart_arrive[1]
					airplane = obj[2].text
					tour_day = obj[3].text
					pride = obj[4].text
					shop_option = obj[5].text.split('회')[0]
					title = obj[6].text
					price = obj[7].text.split('\n')[0]
					status = obj[8].text

					# save data
					data[code]['packages'] = {
						str(package_code): {
							'url': str(current_url),
							'info': {
								'departure': str(departure),
								'arrival':  str(arrival),
								'airplane': str(airplane),
								'tour_day': str(tour_day),
								'pride': str(pride),
								'shop_option': int(shop_option),
								'title': str(title),
								'price': str(price),
								'status': str(status)

							}
						}
					}

				# move to next page
				self.css(self.code_path[1])[-2].click()
				# check duplication
				"""if code = new code -> break"""
				targets = self.css('#new_pkg_list > tbody > tr')
				targets[-1].find_elements_by_css_selector('td')[-3].click()
				self.driver.switch_to_window(self.driver.window_handles[1])
				package_code_target = self.css('div.pdt_code > strong.code_num')
				self.check_delay(package_code_target)
				check_code = package_code_target[0].text

				self.driver.close()
				self.driver.switch_to_window(self.driver.window_handles[0])

				if code == check_code:
					break


"""
pickle load 방법
with open('list.pickle', 'rb') as f:
b = pickle.load(f)
"""

hana = HANA_WORK()
hana.package_code('A')
# for area in area_list:
# 	hana.enter_url(area)
# 	import time
# 	time.sleep(5)
#
# 	try:
# 		hana.get_code(area)
# 	except IndexError:
# 		time.sleep(5)
# 		targets = hana.driver.find_elements_by_css_selector('div.result_list > ul > li')
# 		check = hana.check_delay(targets)
# 		while check is True:
# 			hana.check_delay(targets)
#
# 			if check is True:
# 				hana.get_code(area)


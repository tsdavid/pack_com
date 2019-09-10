# coding:utf-8


boracai_url = \
	"http://www.hanatour.com/asp/booking/productPackage/pk-11000.asp?" \
	"subject=&country=PH" \
	"&city=KLO" \
	"&etc_code=P&area=A&year=2019&month=09&start_city=JCN&goods_grade=31,32,23&start_week=dyd,dyw&hanacode=pack_main_search"

product_code_url = \
"http://www.hanatour.com/asp/booking/productPackage/pk-11001.asp?pkg_mst_code=APP119"

package_product_url = \
"http://www.hanatour.com/asp/booking/productPackage/pk-12000.asp?pkg_code=APP1191908138YK"


package_base_url = "http://www.hanatour.com/asp/booking/productPackage/pk-11000.asp?area="
"""
*대륙 (?area=)
동남아시아 = A
중국 = B
일본 = J
남태평양 = D
유럽 = E
북미 = G
중남미 = C
아프리카 = F
국내(한국) = K
"""


"""
*도시 (&pub_country=)
필리핀 : PH
대만 : TW
브루나이 : BN
인도네시아 : ID
인도 : IN
"""


"""대륙별 진입
'div.result_list > ul > li'
driver.find_elements_by_css_selector('div.result_list > ul > li')
위에 걸 target 이라고 하면
해당 target.text는 str으로 return
split으로 리스트화 해서 코드만 챙기자
"""



"""
page control
div.paginate > a
위 리스트에 앞에 첫번째 a는 맨 앞으로,
두번째 a는 바로 전

마지막에서 두번째는 바로 다음
마지막은 맨뒤로
"""

"""
product code랑 area로 상품 정보 들어가는 url
http://www.hanatour.com/asp/booking/productPackage/pk-11001.asp?pkg_mst_code=CJP888&area=B
=> code 리스트와 area 있으면 상품 정보 들어갈 수 있네

area는 pk-11000
1차 상품 페이지는 pk-11001
"""


"""
상품명 다 가지고 와서 저장하기
import json
j = {}
for idx, i in enumerate(target):
	lst = i.text.split()
	for ele in lst:
		if ele == 'MD추천':
			lst.remove(ele)

	print(lst)
	j[idx] = lst

"""

"""피글 저장 죽이네
way yo  save something
저장 타겟 = j ( json type)

피클 저장
with open('list.pickle', 'wb') as f:
	pickle.dump(j, f)

피클 로드
with open('list.pickle', 'rb') as f:
	b = pickle.load(f)
"""

"""
page scroll down
driver.execute_script("window.scrollTo(0, Y)") 
"""

"""
# scinario
url 진입  -- enter_url method
약잔의 delay -- check_delay method
li crwal
next page
retrun li crawl

if next page is None
stop
and save pickle

"""


"""
pkg_code = AXP199190907KE1
AXP199  - 상품 코드
190907  - 풀발 날짜
KE1     - 항공사
"""

"""
driver 새로운 탭 컨트롤
driver.switch_to_window(driver.window_handles[1])

"""

a = {
	'AVP130': {
		'url': ,
		'text_list': [],
		'package_product': {
			'AVP130190817LJQ': {

			},
			'AVP130190817LJA': {

			}
		}
	}
     }

"""
package product
enter product code
	http://www.hanatour.com/asp/booking/productPackage/pk-11001.asp?pkg_mst_code=AVP130
click package product 
get url
get package product info


c_time = time.time()
for target in targets:
	target.find_elements_by_css_selector('td')[-3].click()
	driver.switch_to_window(driver.window_handles[1])
	check_delay(driver.find_elements_by_css_selector('div.core_point.spn_point > ul > li'))
	c_url = driver.current_url
	driver.close()
	driver.switch_to_window(driver.window_handles[0])
	b_url = driver.current_url
	print('basic_url :', b_url, 'new_url :', c_url)
print('time: ', c_time - time.time())
"""
b = {'AVP130': {
		'url': 'http://www.hanatour.com/asp/booking/productPackage/pk-11001.asp?pkg_mst_code=AVP130AVP130',
		'words': ['AVP130', '패키지', '다낭/호이안+(후에)', '#베스트셀러', '#홈쇼핑따라잡기', '#100%출발', '▶', '홈쇼핑히트상품,', '깜짝특가', '등', '다양한', '프로모션으로', '기획된', '최저가', '다낭', '특별상품입니다.#베스트셀러', '#빈펄랜드', '#리버프론트', '#9/28,29', '박나래와', '함께하는', 'DJ', '파티', '299,900', '원~', '여행기간', '4~5일', '출발요일', '일,월,화,수,목,금,토', '상세보기'],
		'packages' : {
			'AVP130190821KEB': {
				'url': ,
				'info': {
					'time': '08/17 (토) 11:05 08/20 (화) 22:15',
					'airplane': '대한항공',
					'tour_day': '3박4일',
					"pride": '하나팩',
					'shop_option': '3회',
					'title': '[4명이상 출발확정]♥출발가능♥[관광형]다낭/호이안/후에 4일♥전일정 4성호텔+투본강투어+후에전동카♥후에 전동카 등 스페셜 포함',
					'price': '931,100',
					'reservation': '출발가능'
				}

			},
			'AVP130190821OZB': {

			},

	}
},
	'AVP139': {
		'url' : ,
		'words': [],
		'packages' : {

		},
	}
}

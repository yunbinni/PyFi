""" 모듈 구동 """
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

""" 드라이버 불러오기 """
def startDriver() -> None:
    driver.get('https://www.instiz.net/name_enter')

""" 검색어, 시작일, 종료일 -> url 반환 """
def instizCrawler(keyword: str, sdate: str, edate: str, sPage: int, ePage: int) -> None:
    # 검색옵션(날짜선택기능버튼) 클릭
    driver.find_element_by_css_selector('#search > a').click()
    # 시작일 입력
    driver.find_element_by_css_selector('#startime').send_keys(sdate)
    # 종료일 입력 후 엔터
    driver.find_element_by_css_selector('#endtime').send_keys(edate)
    # 검색어 입력
    driver.find_element_by_css_selector('#k').send_keys(keyword + Keys.ENTER)

    time.sleep(1)

    staticURL = str(driver.current_url)

    # url 바뀜
    driver.get(staticURL)

    titles, contents, replies = [], [], []

    for page in range(sPage, ePage + 1):
        # 페이지별로 url 갱신하기
        url = staticURL + '&page=' + str(page)
        driver.get(url)

        # 게시글 불러오기
        articles = driver.find_elements_by_css_selector('#mainboard > tbody > tr > td > span > a')
        alinks = []

        for article in articles:
            alinks.append(article.get_property('href'))

        for i in range(len(alinks)):
            driver.get(alinks[i])
            time.sleep(1)

            # 글 제목 저장
            title = driver.find_element_by_xpath('//*[@id="nowsubject"]/a').text.strip()
            titles.append(title)
            time.sleep(1)

            # 글 본문 저장
            content = driver.find_element_by_xpath('//*[@id="memo_content_1"]').text.strip()
            contents.append(content)
            time.sleep(1)

            # 댓글, 대댓글 저장
            reply = driver.find_elements_by_css_selector('div.comment_line > span')

            for comment in reply:
                replies.append(comment.text)

            time.sleep(1)

        time.sleep(1)

    return titles, contents, replies, sdate, keyword

def writeFile(titles: list, contents: list, replies: list, sdate: str, keyword: str) -> None:
    with open('titles' + sdate + ('/'+keyword) + '.txt', 'a', encoding='utf-8') as f1:
        for title in titles:
            f1.write(title)

    with open('contents.txt' + sdate + ('/'+keyword) + '.txt', 'a', encoding='utf-8') as f2:
        for content in contents:
            f2.write(content)

    with open('replies.txt' + sdate + ('/'+keyword) + '.txt', 'a', encoding='utf-8') as f3:
        for reply in replies:
            f3.write(reply)

""" 드라이버 종료 """
def closeDriver():
    driver.close()

########################################################################################################################
""" 구동 """
if __name__ == "__main__":
    startDriver()
    titles, contents, replies, sdate, keyword = instizCrawler('코로나', '20201216', '20201217', 1, 2)   # 검색어, 시작날짜, 종료날짜, 시작페이지, 종료페이지
    writeFile(titles, contents, replies, sdate, keyword)
    closeDriver()
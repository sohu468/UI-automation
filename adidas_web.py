# coding=utf-8
#!/usr/bin/env python
import json, os, sys, csv, time, unittest, HTMLTestRunner
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options
#from chromedriver_setup import chrome_head
#from webdrivermanager import ChromeDriverManager
#from webdriver_manager.chrome import ChromeDriverManager

reload(sys)
sys.setdefaultencoding('utf-8')

script_path = os.path.dirname(os.path.realpath(__file__))


def chrome_headless_stable():
    options = Options()
    # options.add_argument("--disable-notifications")
    # # options.add_argument('--headless')
    # # options.add_argument('--no-sandbox')
    # options.add_argument('--hide-scrollbars')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--start-maximized')
    # options.add_argument('disable-infobars')
    # options.add_argument("--disable-extensions")
    # options.add_argument('blink-settings=imagesEnabled=false')
    # options.add_argument('--disable-gpu')

    #options.binary_location = r"/opt/google/chrome/google-chrome"
    # options.add_argument("--window-size=1920,1080")
    
    options.add_argument('--kiosk-printing')
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")

    # prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    # options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=options)
    #driver = webdriver.Chrome(executable_path=ChromeDriverManager().download_and_install(), chrome_options=options)
    driver = webdriver.Chrome(executable_path=script_path + '/chromedriver', chrome_options=options)
    #driver = webdriver.Firefox(executable_path=script_path + '/geckodriver', firefox_options=options)
    return driver


class DemoTest(unittest.TestCase):

    global price

    @classmethod
    def setUpClass(cls):
        # cls.driver = chrome_head()
        cls.driver = chrome_headless_stable()
        cls.driver.get('https://adidas:ad20170731@beta.adidas.com.cn')
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()

    def test_disable_cookie(self):
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/section/div[1]/div/a/i')))
        element.click()
        time.sleep(2)

    def test_login(self):
        element = WebDriverWait(self.driver, 15).until(
            # EC.presence_of_element_located((By.XPATH, "//div/ul/li[4]")))
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginBoxDiv"]/a')))
        element.click()
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='login_form']/div/div/div[1]/a[2]/h4")))
        element.click()
        # time.sleep(10)
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginName"]')))
                # (By.XPATH, '//input[substring(@id, string-length(@id) - string-length("Name")+1)= "Name"]')))
        element.clear()
        element.send_keys('18721216939')
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]')))
        element.clear()
        element.send_keys('aa123456')
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginBtn"]')))
        element.click()

    def test_search_item(self):
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="keyword"]')))
        element.clear()
        element.send_keys('EE4047')
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="keysearch"]/a[1]')))
        element.click()
        globals()['price'] = self.driver.find_element(By.XPATH, '//*[@id="pdpbox"]/div[2]/div[3]/div[3]/div[1]/span').text
        # self.assertEqual(globals()['price'], u"¥1666")

    def test_select_and_add_item(self):
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="pdpbox"]/div[2]/div[3]/div[3]/div[4]/div[1]/div[2]/div[1]/div/div[1]/a/span[1]')))
        element.click()
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//div/ul/li[2]/a[contains(text(), "40.5")]')))
        element.click()

    def test_buy_now(self):
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="pdpbox"]/div[2]/div[3]/div[3]/div[4]/div[3]/a[1]')))
        element.click()
        order = self.driver.find_element(By.XPATH, '//*[@id="orderForm"]/div[2]/div/div[2]/div/div[2]/div[2]/div[1]/span[2]')
        # self.assertEqual(order.text, globals()['price'])
        #print order.text
        #print globals()['price']

    def test_place_order(self):
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="orderForm"]/div[1]/div[9]/div/i')))
        element.click()
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="orderForm"]/div[1]/div[10]/a')))
        element.click()


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(DemoTest('test_disable_cookie'))
    suite.addTest(DemoTest('test_login'))
    suite.addTest(DemoTest('test_search_item'))
    suite.addTest(DemoTest('test_select_and_add_item'))
    suite.addTest(DemoTest('test_buy_now'))
    suite.addTest(DemoTest('test_place_order'))

    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    # unittest.main()
    # driver = chrome_head()
    # suite = unittest.makeSuite(PythonTest)
    now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    filename = script_path + "/"+now + "_result.html"
    with open(filename, 'wb') as fb:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fb,
            title=u'WebTest Report',
            description=u'WebTest Execution Details：')
        runner.run(suite)

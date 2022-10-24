from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import requests, time, random
from twocaptcha import TwoCaptcha

class GG_CAPTCHA_SOLVER:
    default_captcha_key = 'ade7542e2ea021dabe29b6d9933e7661'

    def __init__(self, proxy, driver, API_KEY=default_captcha_key):
        for i in range(3):#Giải captcha 3 lần (nếu phải nhiều hơn, proxy đã quá yếu => Bỏ)
            try:
                if i==0:
                    driver.find_element(By.XPATH, "//div[@id='main']")
                else:
                    WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']")))
                    break
            except:
                print('Captcha solver number:', i)
                check = self.run_solver(driver, API_KEY)
                if check ==0:
                    self.solve_status = 0

        try:
            WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='main']")))
            self.solve_status = 1
        except:
            self.solve_status = 0

    def run_solver(self, driver, API_KEY):
        print('start run_solver')
        try: # recaptcha
            captcha = driver.find_element(By.ID, 'recaptcha')
            print('solving recaptcha')
            return self.RecaptchaSolver(driver, API_KEY=API_KEY)
        except: # normal captcha
            captcha = driver.find_element(By.ID, 'captcha-form')
            print('solving normal captcha')
            return self.NormalCaptcha_solver(driver, API_KEY=API_KEY)

    def RecaptchaSolver(self, driver, API_KEY):
        try:
            captcha = driver.find_element(By.ID, 'recaptcha')
            data_sitekey = captcha.get_attribute("data-sitekey")
            data_s = captcha.get_attribute("data-s")
            config = {
                'data-s':data_s
            }
            current_url = driver.current_url
            solver = TwoCaptcha(API_KEY)
            result = solver.recaptcha(
                        sitekey = data_sitekey,
                        url = current_url,
                        **config
                    )
            print('result',result)
            code = result['code']
            write_token_js = f'document.getElementById("g-recaptcha-response").innerHTML="{code}";'
            submit_js = 'document.getElementById("captcha-form").submit();'
            driver.execute_script(write_token_js)

            time.sleep(10/random.randint(100,150)*random.randint(10,20))
            print('sleep',time)

            driver.execute_script(submit_js)
            return 1 # success
        except:
            return 0

    def NormalCaptcha_solver(self, driver, API_KEY):
        captcha = driver.find_element(By.ID, 'captcha-form')
        captcha_img = captcha.find_element(By.TAG_NAME, 'img')

        captcha_img.screenshot('captcha.png')
        solver = TwoCaptcha(API_KEY)

        try:
            result = solver.normal('captcha.png')
            code = result['code']
            captcha.find_element(By.ID,'captcha').send_keys(code)

            time.sleep(10/random.randint(100,150)*random.randint(10,20))
            print('sleep',time)

            captcha.find_element(By.NAME,'btn-submit').click()
            return 1
        except:
            return 0
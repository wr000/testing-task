import unittest
import time
import random
import string
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NUMBER_OF_LETTERS = 3

def randomString(stringLength=10):
	lettersDigits = string.ascii_lowercase + "0123456789"
	return ''.join(random.choice(lettersDigits) for i in range(stringLength))

def sendMail(self, subject_string, content_string):
    if (not EC.presence_of_element_located((By.XPATH, "//button[@class = 'default send']"))):
        return False
    else:
        driver2 = self.driver
        address_field = driver2.find_element_by_xpath("//input[@name='toFieldInput']")
        address_field.send_keys("dedicatedtothetask@ukr.net")

        subject_field = driver2.find_element_by_xpath("//input[@name='subject']")
        subject_field.send_keys(subject_string)
        
        iframe = driver2.find_element_by_xpath("//iframe[contains(@id, 'ifr')]")
        driver2.switch_to_frame(iframe)
        body_element = driver2.find_element_by_xpath("//body[@id='tinymce']")
        body_element.send_keys(content_string)
        driver2.switch_to.default_content()

        send_button = driver2.find_element_by_xpath("//button[@class='default send']")
        send_button.click()
        WebDriverWait(driver2, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='default']")))
        time.sleep(2)

        self.driver = driver2
        return True

class ukrnet_mail_login(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'D:\Python-space\chromedriver_win32\chromedriver.exe')

    def test_email_input(self):
        #login
        driver = self.driver
        driver.get("https://accounts.ukr.net/login")
        
        email = driver.find_element_by_xpath("//input[@id='id-l']")
        email.send_keys("dedicatedtothetask")
        
        password = driver.find_element_by_xpath("//input[@id='id-p']")
        password.send_keys("selfexplanatory")
        
        submit_button = driver.find_element_by_xpath("//button[@type='submit']")
        submit_button.click()
        WebDriverWait(driver, 10).until(
            EC.url_contains("desktop#msglist"))
        
        #composing message         
        compose_button = driver.find_element_by_xpath("//button[@class='default compose']")
        compose_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[@class='default send']")))
        
        for _ in range(0, NUMBER_OF_LETTERS):
            sendMail(self, randomString(), randomString())

            sendmore_button = driver.find_element_by_xpath("//button[@class='default']")
            sendmore_button.click()
        
        #collecting info about received emails
        inbox_link = driver.find_element_by_xpath(
            "//div[@class='sidebar__lists']//a[@id='0']").get_attribute("href")
        driver.get(inbox_link)

        dict = {}
        linksToReceivedMails_objects = driver.find_elements_by_xpath("//a[contains(@href,'#readmsg/')]")
        linksToReceivedMails_strings = []
        for linkToReceivedMail_object in linksToReceivedMails_objects:
            linksToReceivedMails_strings.append(linkToReceivedMail_object.get_attribute("href"))
        
        for linkToReceivedMail_string in linksToReceivedMails_strings:
            driver.get(linkToReceivedMail_string)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='readmsg']")))
            
            subject_element = driver.find_element_by_xpath(
                "//div[@id='readmsg']//h3[@class='readmsg__subject']")
            subject_string = subject_element.text
            
            content_string = driver.find_element_by_xpath(
                "//div[@class='readmsg__body']/span/div/span[@class='xfmc1']").text

            dict[subject_string] = content_string

            if len(dict) > NUMBER_OF_LETTERS:
                break
        
        #composing report
        text = ""
        for key, value in dict.items():
            text += f"Received mail on theme {key} with message: {value}.\n"
            numOfLetters = sum(c.isalpha() for c in value)
            numOfDigits = sum(c.isdigit() for c in value)
            text += f"It contains {numOfLetters} letters and {numOfDigits} numbers\n"
        
        #sending report
        compose_button.click()
        sendMail(self, "Report", text)
        
        #deleting
        inbox_link = driver.find_element_by_xpath(
            "//div[@class='sidebar__lists']//a[@id='0']").get_attribute("href")
        driver.get(inbox_link)
        WebDriverWait(driver, 10).until(
            EC.url_contains("desktop#msglist"))
        driver.find_element_by_xpath("//div[@class='msglist__checkbox']").click()
        driver.find_element_by_xpath("//tbody/tr[1]/td[1]").click()
        driver.find_element_by_link_text("Видалити").click()
        driver.refresh()

if __name__ == "__main__":
    unittest.main()
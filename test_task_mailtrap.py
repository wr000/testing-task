import unittest
import time
import send_emails
from selenium import webdriver

class MailtrapLogin(unittest.TestCase):

    for x in range(0, 5):
        message = send_emails.randomMessage()
        send_emails.sendMessage(message)
        time.sleep(5)

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'D:\Python-space\chromedriver_win32\chromedriver.exe')

    def test_login(self):
        driver = self.driver
        driver.get("https://mailtrap.io/signin")
        
        email = driver.find_element_by_id("user_email")
        email.send_keys("withrapture000@gmail.com")
        time.sleep(5)
        
        password = driver.find_element_by_id("user_password")
        password.send_keys("selfexplanatory")
        time.sleep(5)
        
        driver.find_element_by_name("commit").click()
        time.sleep(5)

        driver.find_element_by_link_text("Demo inbox").click()
        time.sleep(10)
        
        dict = {}
        list_header = driver.find_element_by_xpath("//*[@id='mainView']/div/div[1]/div/ul")
        elements = list_header.find_elements_by_tag_name("li")

        for element in elements:
            element.click()
            time.sleep(10)
            subject_element = driver.find_element_by_xpath("//h2[contains(@class, 'mbs')]")
            subject_content = subject_element.text

            iframe = driver.find_elements_by_tag_name("iframe")[0]
            driver.switch_to_frame(iframe)
            body_element = driver.find_element_by_xpath("//pre")
            body_content = body_element.text

            dict[subject_content] = body_content
            
            driver.switch_to.default_content()
            if len(dict) > 9:
                break
        
        text = ""
        for key, value in dict.items():
            text += f"Received mail on theme {key} with message: {value}.\n"
            numOfLetters = sum(c.isalpha() for c in value)
            numOfDigits = sum(c.isdigit() for c in value)
            text += f"It contains {numOfLetters} letters and {numOfDigits} numbers\n"
            
        message = send_emails.makeMessage("Report", text)
        send_emails.sendMessage(message)

        #because email with report was sent we must redefine li-list
        driver.refresh()
        list_header = driver.find_element_by_xpath("//*[@id='mainView']/div/div[1]/div/ul")
        elements = list_header.find_elements_by_tag_name("li")
        
        while len(elements) > 1:
            elements[1].click()            
            time.sleep(5)
            delete_button = driver.find_element_by_xpath("//a[contains(@title, 'Delete email')]")
            delete_button.click()
            driver.find_element_by_link_text("Confirm").click()
            time.sleep(5)
            driver.refresh()
            time.sleep(5)
            list_header = driver.find_element_by_xpath("//*[@id='mainView']/div/div[1]/div/ul")
            elements = list_header.find_elements_by_tag_name("li")

if __name__ == "__main__":
    unittest.main()
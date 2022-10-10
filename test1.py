import unittest
import os
from appium import webdriver
from time import sleep

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
)


class Test1Appium(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['app'] = PATH('contactmanager.apk')
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'Genymotion Cloud'
        desired_caps['udid'] = 'localhost:30000'  # do uzupelnia gdyby nie byl staly, to co zwraca: $ adb devices
        desired_caps['appPackeges'] = 'com.example.android.contactmanager'
        desired_caps['appActivity'] = 'com.example.android.contactmanager.ContactManager'

        # polaczenie z Appium
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps) # port jest stay
        self.driver.implicitly_wait(2)
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def testfrom(self):
        self.driver.is_app_installed('com.example.android.contactmanager')
        self.driver.find_element_by_id('com.example.android.contactmanager:id/addContactButton').click()
        sleep(2)
        textfields = self.driver.find_elements_by_class_name('android.widget.EditText')
        textfields[0].send_keys('janek z kato')
        textfields[1].send_keys('123456789')
        textfields[2].send_keys('jan@wsb.com')
        sleep(2)
        print(textfields[0])
        print(textfields[0].text)
        # assercje
        self.assertEqual('janek z kato', textfields[0].text)
        self.assertEqual('123456789', textfields[1].text)
        self.assertEqual('jan@wsb.com', textfields[2].text)

    def testFormfaild(self):
        self.driver.is_app_installed('com.example.android.contactmanager')
        self.driver.find_element_by_id('com.example.android.contactmanager:id/addContactButton').click()

        # kod krzysztfg
        self.driver.find_element_by_id('com.example.android.contactmanager:id/contactNameEditText').send_keys('janek')
        sleep(1)
        self.driver.find_element_by_id('com.example.android.contactmanager:id/contactPhoneEditText').send_keys('1234')
        sleep(1)
        self.driver.find_element_by_id('com.example.android.contactmanager:id/contactEmailEditText').send_keys('janek@wsb.com')
        sleep(1)
        self.driver.find_element_by_id('com.example.android.contactmanager:id/contactSaveButton').click()
        error_message = self.driver.find_element_by_id('android:id/alertTitle').get_attribute('text')
        print(error_message)
        self.driver.find_element_by_id('android:id/aerr_restart').click()
        self.assertEqual('Contact Manager has stopped', error_message)




if __name__ == 'main':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test1Appium)
    unittest.TextTestRunner(verbosity=2).run(suite)

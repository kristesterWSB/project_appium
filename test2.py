import unittest
import os
from appium import webdriver
from time import sleep

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__),p)
)


class Test2Appium(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['app'] = PATH('ApiDemos-debug.apk')
        desired_caps['platformName'] = 'Android'
        desired_caps['deviceName'] = 'Genymotion Cloud'
        desired_caps['udid'] = 'localhost:30000'  # do uzupelnia gdyby nie byl staly, to co zwraca: $ adb devices
        desired_caps['appPackeges'] = 'io.appium.android.apis'
        desired_caps['appActivity'] = 'io.appium.android.apis.ApiDemos'
        desired_caps['noReset'] = 'true'

        # polaczenie z Appium
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps) # port jest stay
        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.quit()

    def testWifi(self):
        self.driver.find_element_by_accessibility_id('Preference').click()
        self.driver.find_element_by_accessibility_id('3. Preference dependencies').click()
        checkboxes = self.driver.find_elements_by_android_uiautomator('new UiSelector().checkable(true)')
        passwordInput = "12345"
        for el in checkboxes:
            is_checked = self.driver.find_element_by_class_name('android.widget.CheckBox')
            if is_checked.get_attribute('checked') == 'true': # == 'true' bo to jest napis
                print('chackebox jest zaznaczony')
                self.driver.find_element_by_xpath('//*[@text="WiFi settings"]').click()
                self.driver.find_element_by_class_name('android.widget.EditText').send_keys(passwordInput)

                passwordCurrent = self.driver.find_element_by_class_name('android.widget.EditText').get_attribute(
                    'text')
                # asercja:
                self.assertEqual(passwordInput, passwordCurrent)

                self.driver.find_element_by_id('android:id/button1').click()  # potwierdz OK przyciskiem
                # back na 2 spososby
                self.driver.back()
                # self.driver.keyevent(4)  # uzycie keyevents androidowe-ok

            else:
                el.click()
                sleep(2)

                self.driver.find_element_by_xpath('//*[@text="WiFi settings"]').click()
                self.driver.find_element_by_class_name('android.widget.EditText').send_keys(passwordInput)

                passwordCurrent = self.driver.find_element_by_class_name('android.widget.EditText').get_attribute('text')
                        # asercja:
                self.assertEqual(passwordInput, passwordCurrent)

                self.driver.find_element_by_id('android:id/button1').click()  # potwierdz OK przyciskiem
                        # back na 2 spososby
                self.driver.back()
                # self.driver.keyevent(4)  # uzycie keyevents androidowe-ok

if __name__ == 'main':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test2Appium)
    unittest.TextTestRunner(verbosity=2).run(suite)

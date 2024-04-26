# import time
# import csv

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support.ui import WebDriverWait as Wait


class IQView:
    def __init__(self, URL="http://192.168.10.254") -> None:
        self.URL = URL
        self.browser = webdriver.Firefox()
        self.browser.get(URL)
        self.wait=Wait(self.browser, 30)
        pass
    
    def ClickItem(self, id="", is_double=False):
        try:
            item=self.wait.until(EC.element_to_be_clickable((by.By.ID, id)))
        except Exception as e:
            print("Wait {} timeout", id, e)
            self.browser.quit()
            exit()
        if is_double:
            AC(self.browser).double_click(item).perform()
        else:
            AC(self.browser).click(item).perform()
            
    def TouchItems(self, IDs):
        for id in IDs:
            # self.ClickItem(id["ID"], id['double'])
            print(id)


def __main__():
    iq=IQView()
    iq.ClickItem('techBtn')
    iq.ClickItem('wifisiso')
    iq.ClickItem('ResultsTab')
    iq.ClickItem('Row11')
    iq.ClickItem('wifi_siso_item1', True)

__main__()
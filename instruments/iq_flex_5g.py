# import time
# import csv

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support.ui import WebDriverWait as Wait


class IQView:
    def __init__(self, URL="http://192.168.10.254") -> None:
        print("open brower")
        self.URL = URL
        self.browser = webdriver.Firefox()
        print("load {}".format(URL))
        self.browser.get(URL)
        print("set viewer loading timeout")
        self.wait=Wait(self.browser, 10)
        print("ready")
        pass
    
    def ClickItem(self, id, is_double=False):
        try:
            item=self.wait.until(EC.element_to_be_clickable((by.By.ID, id)))
        except Exception as e:
            print("wait for <{}> timeout".format(id, e))
            self.browser.quit()
            exit()
        if is_double:
            AC(self.browser).double_click(item).perform()
        else:
            AC(self.browser).click(item).perform()
            
    def TouchItem(self, IDs):
        for id in IDs:
            print(id)
            
    def ReadText(self, selector="") -> str:
        try:
            item=self.wait.until(EC.visibility_of_element_located((by.By.XPATH, selector)))
        except Exception as e:
            print("wait for <{}> timeout".format(id, e))
            self.browser.quit()
            exit()
        # print(item.text)
        return item.text

    def InitInst(self):
        print("init instrument ...")
        self.ClickItem('techBtn')
        self.ClickItem('wifisiso')
        self.ClickItem('ResultsTab')
        self.ClickItem('Row11')
        self.ClickItem('wifi_siso_item1', True)

    def GetEVM(self):
        ''' Get text value from webui '''
        print("get evm snapshort")
        evm = self.ReadText('/html/body/div[1]/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/table/tbody/tr[1]/td[2]')
        print(evm)
import time
import logging

logger = logging.getLogger(__name__)

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.ui import Select as Select
from selenium.webdriver.common.keys import Keys


class IQView:
    ''' channel esti LTF/DATA '''
    CH_EST_LTF = 0
    CH_EST_DATA = 1

    def __init__(self, URL="http://192.168.10.254") -> None:
        logger.info("open brower")
        self.URL = URL
        self._running = True
        self.browser = webdriver.Firefox()
        logger.info("load {}".format(URL))
        try:
            self.browser.get(URL)
        except Exception as e:
            logger.info("set viewer loading timeout {}".format(e))
            self.Quit()
        self.wait=Wait(self.browser, 10)
        logger.info("ready")
        pass

    def Quit(self):
        self._running = False
        self.browser.quit()
    
    def _click_item(self, id, is_double=False):
        try:
            item=self.wait.until(EC.element_to_be_clickable((by.By.ID, id)))
        except:
            logger.info("wait for <{}> timeout".format(id))
            self.browser.quit()
            exit()
        if is_double:
            AC(self.browser).double_click(item).perform()
        else:
            AC(self.browser).click(item).perform()
        logger.info("clicked {}".format(id))
        pass
    
    def _is_visable(self, id):
        try:
            item = self.browser.find_element(by.By.ID, id)
            return item.is_displayed()
        except:
            return False
            
    def _select_item(self, id, idx=0):
        try:
            item=self.wait.until(EC.element_to_be_clickable((by.By.ID, id)))
        except:
            logger.info("wait for <{}> timeout".format(id))
            self.browser.quit()
            exit()
        AC(self.browser).click(item).perform()
        AC(self.browser).click(item.find_elements(by.By.XPATH, './child::*')[idx]).perform()
        logger.info("select {} index {}".format(id, idx))
        pass
            
    def _read_text(self, selector) -> str:
        try:
            item=self.wait.until(EC.visibility_of_element_located((by.By.XPATH, selector)))
        except:
            logger.info("wait for <{}> timeout".format(id))
            # self.browser.quit()
            return None
        logger.debug("read {} from [x]".format(item.text))
        return item.text

    def _write_text(self, id, txt):
        try:
            item=self.wait.until(EC.element_to_be_clickable((by.By.ID, id)))
        except:
            logger.info("write to {} not exsit".format(id))
            # self.browser.quit()
            return False
        AC(self.browser).double_click(item).perform()
        item.send_keys(txt)
        item.send_keys(Keys.ENTER)
        logger.info("input {} in {}".format(txt, id))
        return True

    def InitIQ(self):
        logger.info("init instrument ...")
        self._click_item('techBtn')
        self._click_item('wifisiso')
        self._click_item('ResultsTab')
        self._click_item('Row11')
        self._click_item('wifi_siso_item1', True)
        self._click_item('Row12')
        self._click_item('wifi_siso_item3', True)
        
    def _frame2cell(self, frame=1, list=1, row=1, col=2):
        '''
        Frame:
            [F1, F3]
            [F2, F4]
            List:
                [L1, L2]
                Row,Col:
                    [k1, v1]
                    [k2, v2]
                    ...
        '''
        xpath="/html/body/div[1]/div[2]/div[4]/div/div[{}]/div[1]/div/div[2]/div[{}]/div/div[1]/div/div[1]/table/tbody/tr[{}]/td[{}]".format(frame, list, row, col)
        return xpath

    def GetPowerEVM(self, timeout=0.5, retry=60):
        ''' Get text value from webui '''
        while self._running and retry > 0:
            '''
                '/html/body/div[1]/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/table/tbody/tr[1]/td[2]'
                '/html/body/div[1]/div[2]/div[4]/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/table/tbody/tr[1]/td[2]'
                ...
            '''
            power = self._read_text(self._frame2cell(frame=1, list=1, row=1, col=2))
            evm = self._read_text(self._frame2cell(frame=1, list=2, row=1, col=2))
            loleak = self._read_text(self._frame2cell(frame=1, list=1, row=6, col=2))
            try:
                return float(power), float(evm), float(loleak)
            except ValueError:
                retry = retry - 1
                pass
            time.sleep(timeout)
        logger.error("evm vs power timeout")
        return None, None
            
    def GetTxQuality(self):
        pass
    
    def SetHardware(self, freq=5210, level=25):
        self._click_item('HardwareTab')
        if self._is_visable('VSASettings') != True:
            self._click_item('ui-id-7')   # VSA Settings
        self._write_text('Frequency_inp', "{}".format(freq))
        self._write_text('refLevel', "{}".format(level))
        pass

    def SetSettings(self, ch_est=CH_EST_DATA):
        self._click_item('SettingsTab')
        if self._is_visable('wifi_ofdm_analysis_settings_panel') != True:
            self._click_item('mimo_ofdm_analysis_settings_header')
        self._select_item('mimo_chan_est-button', ch_est)
        pass
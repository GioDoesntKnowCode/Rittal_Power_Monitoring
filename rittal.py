from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time,datetime
import argparse



class monitor(object):
    def __init__(self, interval):
        self.interval = interval
        self.browser = webdriver.Chrome("chromedriver")
        self.phase, self.voltage, self.current, self.power, self.energy = -1,-1,-1,-1,-1
        self.logfile = None

    def login(self):
         # Prompt the user to enter their login credentials
        username = input("Enter your username: ")
        password = input("Enter your password: ")
     

        # Launch the browser and navigate to your website
        self.browser.get("http://localhost:8080")

        self.browser.find_element("id","loginUsername").send_keys(username)
        self.browser.find_element("id","loginPassword").send_keys(password)

        self.browser.find_element("id","dijit_form_Button_0").click()   # Login

        WebDriverWait(driver=self.browser, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        error_message = "Incorrect username or password."
        errors = self.browser.find_elements("css selector", ".flash-error")

        if any(error_message in e.text for e in errors):
            print("[!] Login failed")
        else:
            print("[+] Login successful")

        time.sleep(5) # Wait for page to load

        self.browser.find_elements(By.CLASS_NAME,"dojoxGridExpandoNode")[1].click()


    def extractData(self):


        table = self.browser.find_element("id","pdu3TotalTable") # Store whole table 

        shortlist = table.text.split('\n')

        phase, voltage, current, power, energy = shortlist[1].split(" ")[:5]
        self.phase = phase
        self.voltage = float(voltage)
        self.current = float(current)
        self.power = float(power)
        self.energy = float(energy)

    def log(self, logfile = None):
            if logfile:
                self.logfile = logfile
                o = open(self.logfile,'w')

            n = 0
            timeout_start = time.time()
            

            while time.time() < timeout_start + args.timeout:

                self.extractData
                if self.logfile:
                    o.write('%s %d %s %4.1f %2.2f %3.1f %3.1f\n' % (datetime.datetime.now(), n, self.phase, self.voltage, self.current, self.power, self.energy))  # SAVE TO LOG
                n += 1
                time.sleep(self.interval)
            try:
                o.close()
            except:
                pass

    def displayReadings(self):
        print("For Phase: ", self.phase)
        print("Voltage[V]: ", self.voltage)
        print("Current[A]: ", self.current)
        print("Power[W]: ", self.power)
        print("Energy[kWh]: ", self.energy)
            
        

    def logout(self): ### ---W I P---
        self.browser.find_element("xpath","//button[@xpath='1']").click()



def main(args):

    logger = monitor(1)
    logger.login()
    logger.extractData()
    time.sleep(5)
    logger.log(args.outfile)

    time.sleep(5)






if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get data from Watts Up power meter.')
    parser.add_argument('-s', '--sample-interval', dest='interval', default=2.0, type=float, help='Sample interval (default 2 s)')
    parser.add_argument('-t', '--timeout', dest='timeout', default=10.0, type=float, help='Timeout for experiment (default 10 s)')
    parser.add_argument('-o', '--outfile', dest='outfile', default='log.out', help='Output file')
    # parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

    args = parser.parse_args()
    main(args)
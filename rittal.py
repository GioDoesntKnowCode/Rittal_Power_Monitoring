from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import time,datetime
import argparse
import curses
import getpass

class monitor(object):
    def __init__(self):
        self.interval = args.interval
        print("Rittal Credentials")
        self.username = input("Enter your username: ")
        self.password = getpass.getpass("Enter your password: ")

        print("Logging in..")
        
        options = webdriver.ChromeOptions()
        if args.headless.lower() == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')


        if args.system == "MACOS":              
            self.browser = webdriver.Chrome(options=options)
        elif args.system == "LTS":
            chrome_driver_path = "./chromedrivers/chromedriveramd"
            self.browser = webdriver.Chrome(service=Service(executable_path=chrome_driver_path), options=options)
   
        else:
            print("ERROR: Only configuired for MACOS and LTS")
            sys.exit()

        self.phase, self.voltage, self.current, self.power, self.energy = -1,-1,-1,-1,-1
        self.logfile = None

    def login(self):
        # Launch the webpage and navigate to your website
        self.browser.get(self.ip)  # Rittal System: http://192.168.0.200 || Port Forwarding: http://localhost:8080

        self.browser.find_element("id","loginUsername").send_keys(self.username)
        self.browser.find_element("id","loginPassword").send_keys(self.password)

        self.browser.find_element("id","dijit_form_Button_0").click()   # Login

        WebDriverWait(driver=self.browser, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        error_message = "Incorrect username or password."
        errors = self.browser.find_elements("css selector", ".flash-error")

        if any(error_message in e.text for e in errors):
            print("[!] Login failed")
            sys.exit()
        else:
            print("[+] Login successful")

        print("Waiting on page to load..")
        time.sleep(1) # Wait for page to load

        self.browser.find_elements(By.CLASS_NAME,"dojoxGridExpandoNode")[1].click()


    def extractData(self):
        table = self.browser.find_element("id","pdu3TotalTable") # Store whole table 

        shortlist = table.text.split('\n')

        phase, voltage, current, power, energy = shortlist[self.phaseMeasure].split(" ")[:5]
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

                if time.time() - self.last_click_time > 300:
                    requests.get(self.ip)
                    self.last_click_time = time.time()


                try:                # Sometimes the Rittal Interface auto-logs you out
                    self.extractData()  
                except:
                    print("Auto-Logged out: Resolving..")
                    self.login()

                    

                if self.logfile:
                    o.write('%s %d %s %4.1f %2.2f %3.1f %3.1f\n' % (datetime.datetime.now(), n, self.phase, self.voltage, self.current, self.power, self.energy))  # SAVE TO LOG
                n += 1
                time.sleep(self.interval)

            try:
                o.close()
            except:
                pass
            print("Logged Readings Succesfully")

        except Exception as e:
            print("Crashed at: " + str(n) + " " + str(datetime.datetime.now()))
            print(e)
        

    def displayReadings(self):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.nodelay(1)
        try:
            curses.curs_set(0)
        except:
            pass
        n = 0
        while True:
            self.extractData()

            screen.clear()
            screen.addstr(2, 4, 'Logging from Phase %s' % self.phase)
            screen.addstr(4, 4, 'Time:     %d s' % n)
            screen.addstr(5, 4, 'Power:   %3.1f W' % self.power)
            screen.addstr(6, 4, 'Voltage: %5.1f V' % self.voltage)
            if self.current<1000:
                screen.addstr(7, 4, 'Current: %d mA' % int(self.current))
            else:
                screen.addstr(7, 4, 'Current: %3.3f A' % self.current)
            screen.addstr(9, 4, 'Press "q" to quit ')
            n += 1
            time.sleep(self.interval)
            screen.refresh()
            c = screen.getch()
            if c in (ord('q'), ord('Q')):
                break  # Exit the while()
        curses.nocbreak()
        curses.echo()
        curses.endwin()


    def logout(self): ### ---W I P---
        self.browser.find_element("xpath","//button[@xpath='1']").click()



def main(args):

    logger = monitor()
    logger.login()
    logger.extractData()
    # time.sleep(5)
    logger.log(args.outfile)  # Just Logging
    # logger.displayReadings()  # For Live readings






if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get data from Watts Up power meter.')
    parser.add_argument('-i', '--interval', dest='interval', default=2.0, type=float, help='Sample interval (default 2 s)')
    parser.add_argument('-t', '--timeout', dest='timeout', default=10.0, type=float, help='Timeout for experiment (default 10 s)')
    parser.add_argument('-o', '--outfile', dest='outfile', default='log.out', help='Output file')
    parser.add_argument('-n', '--network', dest='network', default='http://localhost:8080', help='IP for Rittal interface (Dependent on System)')
    parser.add_argument('-s', '--system', dest='system', default='MACOS', help='System for chromedriver')
    parser.add_argument('-d', '--headless', dest='headless', default='True', help='Open chrome browser (Only possible on MAC)')
    parser.add_argument('-p', '--phase', dest='phase', default='L1', help='Select Phase')

    # parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

    args = parser.parse_args()
    main(args)
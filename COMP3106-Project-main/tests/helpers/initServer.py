import subprocess
from selenium import webdriver
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InitServer():

    def setupDriversAndServer():
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver2 = webdriver.Chrome(options=options)
        warnings.filterwarnings("ignore", category=ResourceWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        p = subprocess.Popen(["node", "server.js"], shell=True)
        driver.get("http://localhost:3000")
        driver2.get("http://localhost:3000")
        WebDriverWait(driver, 10).until(EC.title_is('Blackjack'))
        WebDriverWait(driver2, 10).until(EC.title_is('Blackjack'))
        return driver, driver2, p
    
    def tearDownDriversAndServer(driver, driver2, p):
        driver.quit()
        driver2.quit()
        # Kill Node Server
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=p.pid))
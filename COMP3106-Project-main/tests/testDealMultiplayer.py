import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class DealMultiplayer(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_correct_buttons_on_browser1(self):
        driver = self.driver
        self.assertIn("Blackjack", driver.title)

        deal = driver.find_element_by_id("deal")
        deal2 = driver.find_element_by_id("deal2")
        hit = driver.find_element_by_id("hit")
        hit2 = driver.find_element_by_id("hit2")
        stand = driver.find_element_by_id("stand")
        stand2 = driver.find_element_by_id("stand2")

        self.assertEqual(deal.get_attribute("disabled") , None)
        self.assertEqual(deal2.get_attribute("disabled") , None)
        self.assertEqual(hit.get_attribute("disabled") , 'true')
        self.assertEqual(hit2.get_attribute("disabled") , 'true')
        self.assertEqual(stand.get_attribute("disabled") , 'true')
        self.assertEqual(stand2.get_attribute("disabled") , 'true')
    
    def test_correct_buttons_on_browser2(self):
        driver = self.driver2
        self.assertIn("Blackjack", driver.title)

        deal = driver.find_element_by_id("deal")
        deal2 = driver.find_element_by_id("deal2")
        hit = driver.find_element_by_id("hit")
        hit2 = driver.find_element_by_id("hit2")
        stand = driver.find_element_by_id("stand")
        stand2 = driver.find_element_by_id("stand2")

        self.assertEqual(deal.get_attribute("disabled") , None)
        self.assertEqual(deal2.get_attribute("disabled") , None)
        self.assertEqual(hit.get_attribute("disabled") , 'true')
        self.assertEqual(hit2.get_attribute("disabled") , 'true')
        self.assertEqual(stand.get_attribute("disabled") , 'true')
        self.assertEqual(stand2.get_attribute("disabled") , 'true')

    def test_press_deal_on_browser1(self):
        driver = self.driver
        driver2 = self.driver2

        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # Browser 1 is updated correctly
        deal = driver.find_element_by_id("deal")
        deal2 = driver.find_element_by_id("deal2")
        hit = driver.find_element_by_id("hit")
        hit2 = driver.find_element_by_id("hit2")
        stand = driver.find_element_by_id("stand")
        stand2 = driver.find_element_by_id("stand2")
        self.assertEqual(deal.get_attribute("disabled") , 'true')
        self.assertEqual(deal2.get_attribute("disabled") , 'true')
        self.assertEqual(hit.get_attribute("disabled") , None)
        self.assertEqual(hit2.get_attribute("disabled") , 'true')
        self.assertEqual(stand.get_attribute("disabled") , None)
        self.assertEqual(stand2.get_attribute("disabled") , 'true')

        # Browser 2 is updated correctly
        dealBrowser2 = driver2.find_element_by_id("deal")
        deal2Browser2 = driver2.find_element_by_id("deal2")
        hitBrowser2 = driver2.find_element_by_id("hit")
        hit2Browser2 = driver2.find_element_by_id("hit2")
        standBrowser2 = driver2.find_element_by_id("stand")
        stand2Browser2 = driver2.find_element_by_id("stand2")
        self.assertEqual(dealBrowser2.get_attribute("disabled") , 'true')
        self.assertEqual(deal2Browser2.get_attribute("disabled") , 'true')
        self.assertEqual(hitBrowser2.get_attribute("disabled") , 'true')
        self.assertEqual(hit2Browser2.get_attribute("disabled") , 'true')
        self.assertEqual(standBrowser2.get_attribute("disabled") , 'true')
        self.assertEqual(stand2Browser2.get_attribute("disabled") , 'true')
    
    def test_press_deal_on_browser2(self):
        driver = self.driver
        driver2 = self.driver2

        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        # Click deal on Browser 2
        driver2.find_element_by_id("deal").click()

        # Browser 1 is updated correctly
        deal = driver.find_element_by_id("deal")
        deal2 = driver.find_element_by_id("deal2")
        hit = driver.find_element_by_id("hit")
        hit2 = driver.find_element_by_id("hit2")
        stand = driver.find_element_by_id("stand")
        stand2 = driver.find_element_by_id("stand2")
        self.assertEqual(deal.get_attribute("disabled") , 'true')
        self.assertEqual(deal2.get_attribute("disabled") , 'true')
        self.assertEqual(hit.get_attribute("disabled") , 'true')
        self.assertEqual(hit2.get_attribute("disabled") , 'true')
        self.assertEqual(stand.get_attribute("disabled") , 'true')
        self.assertEqual(stand2.get_attribute("disabled") , 'true')
        
        # Browser 2 is updated correctly
        dealBrowser2 = driver2.find_element_by_id("deal")
        deal2Browser2 = driver2.find_element_by_id("deal2")
        hitBrowser2 = driver2.find_element_by_id("hit")
        hit2Browser2 = driver2.find_element_by_id("hit2")
        standBrowser2 = driver2.find_element_by_id("stand")
        stand2Browser2 = driver2.find_element_by_id("stand2")
        self.assertEqual(dealBrowser2.get_attribute("disabled") , 'true')
        self.assertEqual(deal2Browser2.get_attribute("disabled") , 'true')
        self.assertEqual(hitBrowser2.get_attribute("disabled") , None)
        self.assertEqual(hit2Browser2.get_attribute("disabled") , 'true')
        self.assertEqual(standBrowser2.get_attribute("disabled") , None)
        self.assertEqual(stand2Browser2.get_attribute("disabled") , 'true')

    def test_dealing_rigged_cards(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([1,2,3,4,5,6,7,8])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        #Browser 1 Should contain the correct cards for each player
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        aiVis = driver.find_element_by_id("aiCardsVisible")
        dealerVis = driver.find_element_by_id("dealerCardsVisible")

        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : 3<img class="card" src="img/club.png"></div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : 5<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 7<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/club.png"></div>')

        #Browser 2 Should contain the correct cards for each player
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")

        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : 3<img class="card" src="img/club.png"></div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : 5<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 7<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/club.png"></div>')

    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
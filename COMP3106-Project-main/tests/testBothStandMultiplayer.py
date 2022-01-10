import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class BothStandMultiplayer(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_correct_buttons_on_browsers_after_stand(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()

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
        self.assertEqual(hitBrowser2.get_attribute("disabled") , 'true')
        self.assertEqual(hit2Browser2.get_attribute("disabled") , None)
        self.assertEqual(standBrowser2.get_attribute("disabled") , 'true')
        self.assertEqual(stand2Browser2.get_attribute("disabled") , None)
    
    def test_both_players_stand_result(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([12,13,22,23,25,26,10,38])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Browser 1 Should contain the correct cards for each player
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : J<img class="card" src="img/diamond.png"></div>')

        #Browser 2 Should contain the correct cards for each player
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : J<img class="card" src="img/diamond.png"></div>')

        #Both Browsers should have the correct hand for AI and Dealer
        aiVis = driver.find_element_by_id("aiCardsVisible")
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : K<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : K<img class="card" src="img/heart.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        
    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
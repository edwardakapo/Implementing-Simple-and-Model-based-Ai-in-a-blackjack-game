import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PlayRoundMultiplayer(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_game_turn_execution_order(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([5,10,49,50,51,48,19,21,29,8,4])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # It should be player 1s Turn
        deal = driver.find_element_by_id("deal")
        stand = driver.find_element_by_id("stand")
        hit = driver.find_element_by_id("hit")

        self.assertEqual(deal.get_attribute("disabled") , 'true')
        self.assertEqual(stand.get_attribute("disabled") , None)
        self.assertEqual(hit.get_attribute("disabled") , None)

        # Click Hit for Player 1
        driver.find_element_by_id("hit").click()

        # It should be player 2s Turn
        deal2 = driver.find_element_by_id("deal2")
        stand2 = driver2.find_element_by_id("stand2")
        hit2 = driver2.find_element_by_id("hit2")

        self.assertEqual(deal2.get_attribute("disabled") , 'true')
        self.assertEqual(stand2.get_attribute("disabled") , None)
        self.assertEqual(hit2.get_attribute("disabled") , None)

        # Click Stand for Player 2
        driver2.find_element_by_id("stand2").click()

        # The AI should be updated
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/spade.png">9<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/spade.png">9<img class="card" src="img/club.png"></div>')
       
        # It should be player 1s Turn again
        deal3 = driver.find_element_by_id("deal")
        stand3 = driver.find_element_by_id("stand")
        hit3 = driver.find_element_by_id("hit")

        self.assertEqual(deal3.get_attribute("disabled") , 'true')
        self.assertEqual(stand3.get_attribute("disabled") , None)
        self.assertEqual(hit3.get_attribute("disabled") , None)

        # Click Stand for Player 1
        driver.find_element_by_id("stand").click()

        # Then Dealer should be updated
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/diamond.png">5<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/diamond.png">5<img class="card" src="img/club.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        
    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
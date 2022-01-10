import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AiBehavior(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_ai_stay_twenty_one(self):
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

        #Both Browsers should have the correct score for AI and Dealer
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
    
    def test_ai_hit_single_visible_card(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([12,13,22,23,5,26,10,38,8,9])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for AI
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png">9<img class="card" src="img/club.png">10<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png">9<img class="card" src="img/club.png">10<img class="card" src="img/club.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        
    def test_ai_hit_values_in_range(self):
        # else if the current value of the hand of the AI player is between 18 and 20
        # then if any other player has visible cards that add up to strictly more than the AI player’s hand’s value minus 10,
        # then hit
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([9,8,22,21,33,35,37,38,50])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for AI
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/heart.png">Q<img class="card" src="img/spade.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/heart.png">Q<img class="card" src="img/spade.png"></div>')

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
    
    def test_ai_stay_values_not_in_range(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([9,8,22,21,34,35,37,38,50])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for AI
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/heart.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
    
    def test_ai_forced_hit(self):
        # Ai has no other option but to hit
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([9,8,22,21,32,35,37,38,50])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for AI
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/heart.png">Q<img class="card" src="img/spade.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/heart.png">Q<img class="card" src="img/spade.png"></div>')

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
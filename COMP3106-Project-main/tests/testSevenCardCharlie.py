import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class SevenCardCharlie(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()

    def test_player1_seven_card_charlie(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([0,1,49,50,39,48,19,22,13,14,3,4,5])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        for _ in range(4):
            # Click hit on Browser 1
            driver.find_element_by_id("hit").click()
            # Click stand on Browser 2
            driver2.find_element_by_id("stand2").click()
        
        # Final Hit Before 7 Card Charlie Should Be Decalred
        driver.find_element_by_id("hit").click()

        #Browser 1 Should contain the correct cards for each player
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : 2<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png">2<img class="card" src="img/diamond.png">4<img class="card" src="img/club.png">5<img class="card" src="img/club.png">6<img class="card" src="img/club.png"></div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : Q<img class="card" src="img/spade.png"></div>')

        #Browser 2 Should contain the correct cards for each player
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : 2<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png">2<img class="card" src="img/diamond.png">4<img class="card" src="img/club.png">5<img class="card" src="img/club.png">6<img class="card" src="img/club.png"></div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : Q<img class="card" src="img/spade.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Win - 7 Card Charlie</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Win - 7 Card Charlie</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
    
    def test_player2_seven_card_charlie(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([49,50,0,1,39,48,19,22,13,14,3,4,5])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        for _ in range(5):
            # Click stand on Browser 1
            driver.find_element_by_id("stand").click()
            # Click hit on Browser 2
            driver2.find_element_by_id("hit2").click()

        #Browser 1 Should contain the correct cards for each player
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : Q<img class="card" src="img/spade.png"></div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : 2<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png">2<img class="card" src="img/diamond.png">4<img class="card" src="img/club.png">5<img class="card" src="img/club.png">6<img class="card" src="img/club.png"></div>')

        #Browser 2 Should contain the correct cards for each player
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : Q<img class="card" src="img/spade.png"></div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : 2<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png">2<img class="card" src="img/diamond.png">4<img class="card" src="img/club.png">5<img class="card" src="img/club.png">6<img class="card" src="img/club.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Win - 7 Card Charlie</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Win - 7 Card Charlie</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
    
    def test_ai_seven_card_charlie(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([49,50,39,48,0,1,19,22,13,14,2,3,4])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Browser 1 Should contain the correct cards for the ai
        aiVis = driver.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 2<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png">2<img class="card" src="img/diamond.png">3<img class="card" src="img/club.png">4<img class="card" src="img/club.png">5<img class="card" src="img/club.png"></div>')

        #Browser 1 Should contain the correct cards for the ai
        aiVis2 = driver2.find_element_by_id("aiCardsVisible")
        self.assertEqual(aiVis2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 2<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png">2<img class="card" src="img/diamond.png">3<img class="card" src="img/club.png">4<img class="card" src="img/club.png">5<img class="card" src="img/club.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Win - 7 Card Charlie</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Win - 7 Card Charlie</div>')

    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
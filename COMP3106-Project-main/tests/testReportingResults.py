import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class ReportingResults(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_player_1_busts_after_hit_and_player_2_stays(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([5,10,49,50,39,48,19,22,37])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click hit on Browser 1
        driver.find_element_by_id("hit").click()

        #Player 1 Bust Should Be Visible On Browser 1
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        res1 = driver.find_element_by_id("result")
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : J<img class="card" src="img/club.png">Q<img class="card" src="img/heart.png"></div>')
        self.assertEqual(res1.get_attribute('outerHTML') , '<div id="result">Bust</div>')
        
        #Player 1 Bust Should Be Visible On Browser 2
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        res1Browser2 = driver2.find_element_by_id("result")
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : J<img class="card" src="img/club.png">Q<img class="card" src="img/heart.png"></div>')
        self.assertEqual(res1Browser2.get_attribute('outerHTML') , '<div id="result">Bust</div>')

        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Bust</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Bust</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')

    def test_player_2_busts_after_hit_and_player_1_stays(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([5,10,49,50,39,48,19,22,37])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click hit on Browser 2
        driver2.find_element_by_id("hit2").click()

        #Browser 1 Should contain the correct cards for each player
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : J<img class="card" src="img/club.png"></div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : Q<img class="card" src="img/spade.png">Q<img class="card" src="img/heart.png"></div>')

        #Browser 2 Should contain the correct cards for each player
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : J<img class="card" src="img/club.png"></div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : Q<img class="card" src="img/spade.png">Q<img class="card" src="img/heart.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Bust</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Bust</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')

    def test_ai_wins_with_higher_value(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)
        driver.execute_script("App.dealRigged([5,10,49,50,38,48,19,22,29,39])")
        # App.dealRigged([5,10,49,50,38,48,19,22,29,39])
        # App.dealRigged([9,0,49,50,38,48,19,22,13,39])

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click hit on Browser 1
        driver.find_element_by_id("hit").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')

    def test_player_wins_with_fewest_cards(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([9,0,49,50,38,48,19,22,13,39])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click hit on Browser 2
        driver2.find_element_by_id("hit2").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Lose</div>')
    
    def test_ai_bust_should_be_visible_to_all(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([9,1,49,50,38,48,19,22,13,43])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click hit on Browser 1
        driver.find_element_by_id("hit").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        # Ai should play and then bust should be visible
        resultsAi = driver.find_element_by_id("aiResult")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
    
    def test_two_players_with_the_same_value_and_size_should_tie(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)
        driver.execute_script("App.dealRigged([11,10,49,50,38,46,19,22,16])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Win</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Win</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')

    def test_player_wins_with_largest_hand(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)
        driver.execute_script("App.dealRigged([38,39,49,50,5,10,19,22,29,48])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

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

    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
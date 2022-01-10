import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PlayMultipleGames(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_play_two_sequential_games_different_player_numbers(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)
        # Game 1
        driver.execute_script("App.dealRigged([5,10,49,50,51,48,19,21,29,8,4])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # Verify P1 is active (green)
        p1html = driver.find_element_by_xpath("/html/body/div[2]/div[1]").get_attribute('outerHTML')
        self.assertIn('typeActive' , str(p1html))

        # Click Hit for Player 1
        driver.find_element_by_id("hit").click()

        # Click Stand for Player 2
        driver2.find_element_by_id("stand2").click()

        # The AI should be updated
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")

        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/spade.png">9<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/spade.png">9<img class="card" src="img/club.png"></div>')

        # Click Stand for Player 1
        driver.find_element_by_id("stand").click()
        
        # The dealer should be updated
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/diamond.png">5<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/diamond.png">5<img class="card" src="img/club.png"></div>')

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

        # Game 2
        driver2.execute_script("App.dealRigged([6,11,50,51,49,47,18,20,28,9,5])")

        # Click deal on Browser 2
        driver2.find_element_by_id("deal").click()

        # Verify P1 is not active
        p1html = driver.find_element_by_xpath("/html/body/div[2]/div[1]").get_attribute('outerHTML')
        self.assertNotIn('typeActive' , str(p1html))
        # Verify P2 is active (green) - i.e. P2 is now player 1
        p2html = driver2.find_element_by_xpath("/html/body/div[2]/div[1]").get_attribute('outerHTML')
        self.assertIn('typeActive' , str(p2html))

        # Click Stand for Player 1
        driver2.find_element_by_id("stand").click()

        # Click Stand for Player 2
        driver.find_element_by_id("stand2").click()

        # The AI then dealer should be updated
        aiVis = driver.find_element_by_id("aiCardsVisible")
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")

        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 9<img class="card" src="img/spade.png">3<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 8<img class="card" src="img/diamond.png">10<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 9<img class="card" src="img/spade.png">3<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 8<img class="card" src="img/diamond.png">10<img class="card" src="img/club.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Win</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Win</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')

    def test_play_two_sequential_games_same_player_numbers(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)
        # Game 1
        driver.execute_script("App.dealRigged([5,10,49,50,51,48,19,21,29,8,4])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # Verify P1 is active (green)
        p1html = driver.find_element_by_xpath("/html/body/div[2]/div[1]").get_attribute('outerHTML')
        self.assertIn('typeActive', str(p1html))

        # Click Hit for Player 1
        driver.find_element_by_id("hit").click()

        # Click Stand for Player 2
        driver2.find_element_by_id("stand2").click()

        # The AI should be updated
        aiVis = driver.find_element_by_id("aiCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")

        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/spade.png">9<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 10<img class="card" src="img/spade.png">9<img class="card" src="img/club.png"></div>')

        # Click Stand for Player 1
        driver.find_element_by_id("stand").click()
        
        # The dealer should be updated
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/diamond.png">5<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 9<img class="card" src="img/diamond.png">5<img class="card" src="img/club.png"></div>')

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

        # Game 2
        driver.execute_script("App.dealRigged([6,11,50,51,49,47,18,20,28,9,5])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # Verify P1 is Still active (green)
        p1html = driver.find_element_by_xpath("/html/body/div[2]/div[1]").get_attribute('outerHTML')
        self.assertIn('typeActive', str(p1html))

        # Click Stand for Player 1
        driver.find_element_by_id("stand").click()

        # Click Stand for Player 2
        driver2.find_element_by_id("stand2").click()

        # The AI then dealer should be updated
        aiVis = driver.find_element_by_id("aiCardsVisible")
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")

        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 9<img class="card" src="img/spade.png">3<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 8<img class="card" src="img/diamond.png">10<img class="card" src="img/club.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : 9<img class="card" src="img/spade.png">3<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 8<img class="card" src="img/diamond.png">10<img class="card" src="img/club.png"></div>')

        #Results should be displayed correctly on both Browsers
        results1 = driver.find_element_by_id("result")
        results2 = driver.find_element_by_id("result2")
        resultsAi = driver.find_element_by_id("aiResult")
        results1Browser2 = driver2.find_element_by_id("result")
        results2Browser2 = driver2.find_element_by_id("result2")
        resultsAiBrowser2 = driver2.find_element_by_id("aiResult")
        self.assertEqual(results1.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2.get_attribute('outerHTML') , '<div id="result2">Win</div>')
        self.assertEqual(resultsAi.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')
        self.assertEqual(results1Browser2.get_attribute('outerHTML') , '<div id="result">Lose</div>')
        self.assertEqual(results2Browser2.get_attribute('outerHTML') , '<div id="result2">Win</div>')
        self.assertEqual(resultsAiBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Bust</div>')

    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
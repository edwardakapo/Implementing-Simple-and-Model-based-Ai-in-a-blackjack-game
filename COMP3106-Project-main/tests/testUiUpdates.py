import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helpers.initServer import InitServer

class UiUpdates(unittest.TestCase):
    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()

    def test_elements_visible_for_both_players_on_game_deal(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)
        driver.execute_script("App.dealRigged([12,13,22,23,25,26,10,38])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        # Browser 1 Should contain the correct cards for each player
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p1Cards = driver.find_element_by_id("player1Cards")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        p2Cards = driver.find_element_by_id("player2Cards")
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : J<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p1Cards.get_attribute('outerHTML') , '<div id="player1Cards">Hand : K<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png"></div>')
        # Player 1 should not be able to see p2's cards
        self.assertEqual(p2Cards.get_attribute('outerHTML') , '<div id="player2Cards"></div>')

        # Browser 1 Should contain the correct cards for each player
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p1CardsBrowser2 = driver2.find_element_by_id("player1Cards")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        p2CardsBrowser2 = driver2.find_element_by_id("player2Cards")
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : J<img class="card" src="img/diamond.png"></div>')
        # Player 2 should not be able to see p1's cards
        self.assertEqual(p1CardsBrowser2.get_attribute('outerHTML') , '<div id="player1Cards"></div>')
        self.assertEqual(p2CardsBrowser2.get_attribute('outerHTML') , '<div id="player2Cards">Hand : 10<img class="card" src="img/diamond.png">J<img class="card" src="img/diamond.png"></div>')

        # Both Browsers should have the correct hand for AI and Dealer
        aiVis = driver.find_element_by_id("aiCardsVisible")
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        aiVisBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(aiVis.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : K<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiVisBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : K<img class="card" src="img/heart.png"></div>')
        
        # Should not be able to see dealers/AI hand
        aiCards = driver.find_element_by_id("aiCards")
        dealerCards = driver.find_element_by_id("dealerCards")
        aiCardsBrowser2 = driver2.find_element_by_id("aiCards")
        dealerCardsBrowser2 = driver2.find_element_by_id("dealerCards")
        self.assertEqual(aiCards.get_attribute('outerHTML') , '<div id="aiCards"></div>')
        self.assertEqual(dealerCards.get_attribute('outerHTML') , '<div id="dealerCards"></div>')
        self.assertEqual(aiCardsBrowser2.get_attribute('outerHTML') , '<div id="aiCards"></div>')
        self.assertEqual(dealerCardsBrowser2.get_attribute('outerHTML') , '<div id="dealerCards"></div>')
    
    def test_elements_visible_for_both_players_on_game_end(self):
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

        # All elements should be visible on browser 1
        aiCards = driver.find_element_by_id("aiCards")
        aiVisible = driver.find_element_by_id("aiCardsVisible")
        aiScore = driver.find_element_by_id("aiScore")
        aiResult = driver.find_element_by_id("aiResult")
        dealerCards = driver.find_element_by_id("dealerCards")
        dealerVisible = driver.find_element_by_id("dealerCardsVisible")
        dealerScore = driver.find_element_by_id("dealerScore")
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p1Cards = driver.find_element_by_id("player1Cards")
        p1Score = driver.find_element_by_id("player1Score")
        p1Result = driver.find_element_by_id("result")
        p2Vis = driver.find_element_by_id("player2CardsVisible")
        p2Cards = driver.find_element_by_id("player2Cards")
        p2Score = driver.find_element_by_id("player2Score")
        p2Result = driver.find_element_by_id("result2")
        self.assertEqual(aiCards.get_attribute('outerHTML') , '<div id="aiCards">Hand : K<img class="card" src="img/diamond.png">A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiVisible.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiScore.get_attribute('outerHTML') , '<div id="aiScore">Score : 21</div>')
        self.assertEqual(aiResult.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        self.assertEqual(dealerCards.get_attribute('outerHTML') , '<div id="dealerCards">Hand : J<img class="card" src="img/club.png">K<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisible.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : K<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerScore.get_attribute('outerHTML') , '<div id="dealerScore">Score : 20</div>')
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p1Cards.get_attribute('outerHTML') , '<div id="player1Cards">Hand : K<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p1Score.get_attribute('outerHTML') , '<div id="player1Score">Score : 21</div>')
        self.assertEqual(p1Result.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(p2Vis.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : J<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2Cards.get_attribute('outerHTML') , '<div id="player2Cards">Hand : 10<img class="card" src="img/diamond.png">J<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2Score.get_attribute('outerHTML') , '<div id="player2Score">Score : 20</div>')
        self.assertEqual(p2Result.get_attribute('outerHTML') , '<div id="result2">Lose</div>')

        # All elements should be visible on browser 2
        aiCardsBrowser2 = driver2.find_element_by_id("aiCards")
        aiVisibleBrowser2 = driver2.find_element_by_id("aiCardsVisible")
        aiScoreBrowser2 = driver2.find_element_by_id("aiScore")
        aiResultBrowser2 = driver2.find_element_by_id("aiResult")
        dealerCardsBrowser2 = driver2.find_element_by_id("dealerCards")
        dealerVisibleBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        dealerScoreBrowser2 = driver2.find_element_by_id("dealerScore")
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        p1CardsBrowser2 = driver2.find_element_by_id("player1Cards")
        p1ScoreBrowser2 = driver2.find_element_by_id("player1Score")
        p1ResultBrowser2 = driver2.find_element_by_id("result")
        p2VisBrowser2 = driver2.find_element_by_id("player2CardsVisible")
        p2CardsBrowser2 = driver2.find_element_by_id("player2Cards")
        p2ScoreBrowser2 = driver2.find_element_by_id("player2Score")
        p2ResultBrowser2 = driver2.find_element_by_id("result2")
        self.assertEqual(aiCardsBrowser2.get_attribute('outerHTML') , '<div id="aiCards">Hand : K<img class="card" src="img/diamond.png">A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiVisibleBrowser2.get_attribute('outerHTML') , '<div id="aiCardsVisible">Visible : A<img class="card" src="img/heart.png"></div>')
        self.assertEqual(aiScoreBrowser2.get_attribute('outerHTML') , '<div id="aiScore">Score : 21</div>')
        self.assertEqual(aiResultBrowser2.get_attribute('outerHTML') , '<div id="aiResult">Win</div>')
        self.assertEqual(dealerCardsBrowser2.get_attribute('outerHTML') , '<div id="dealerCards">Hand : J<img class="card" src="img/club.png">K<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisibleBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : K<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerScoreBrowser2.get_attribute('outerHTML') , '<div id="dealerScore">Score : 20</div>')
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p1CardsBrowser2.get_attribute('outerHTML') , '<div id="player1Cards">Hand : K<img class="card" src="img/club.png">A<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p1ScoreBrowser2.get_attribute('outerHTML') , '<div id="player1Score">Score : 21</div>')
        self.assertEqual(p1ResultBrowser2.get_attribute('outerHTML') , '<div id="result">Win</div>')
        self.assertEqual(p2VisBrowser2.get_attribute('outerHTML') , '<div id="player2CardsVisible">Visible : J<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2CardsBrowser2.get_attribute('outerHTML') , '<div id="player2Cards">Hand : 10<img class="card" src="img/diamond.png">J<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(p2ScoreBrowser2.get_attribute('outerHTML') , '<div id="player2Score">Score : 20</div>')
        self.assertEqual(p2ResultBrowser2.get_attribute('outerHTML') , '<div id="result2">Lose</div>')

    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
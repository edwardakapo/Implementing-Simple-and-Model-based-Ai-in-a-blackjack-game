import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class CorrectScore(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()

    def test_value_of_two_aces(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([39,0,22,21,34,35,37,38,50])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        #Verify UI Updates and correct score
        p1Score = driver.find_element_by_id("player1Score")
        p1ScoreBrowser2 = driver2.find_element_by_id("player1Score")
        self.assertEqual(p1Score.get_attribute('outerHTML') , '<div id="player1Score">Score : 12</div>')
        self.assertEqual(p1ScoreBrowser2.get_attribute('outerHTML') , '<div id="player1Score"></div>')
    
    def test_value_of_ace_changes(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([39,0,22,21,34,35,37,38,50])")

        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()

        #Verify UI Updates and correct score
        p1Score = driver.find_element_by_id("player1Score")
        p1ScoreBrowser2 = driver2.find_element_by_id("player1Score")
        p1Vis = driver.find_element_by_id("player1CardsVisible")
        p1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        self.assertEqual(p1Score.get_attribute('outerHTML') , '<div id="player1Score">Score : 12</div>')
        self.assertEqual(p1ScoreBrowser2.get_attribute('outerHTML') , '<div id="player1Score"></div>')
        self.assertEqual(p1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/club.png"></div>')
        self.assertEqual(p1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/club.png"></div>')

        # Hit on Player 1
        driver.find_element_by_id("hit").click()

        # Verify Score remains 12, and visible cards grows
        ap1Score = driver.find_element_by_id("player1Score")
        ap1ScoreBrowser2 = driver2.find_element_by_id("player1Score")
        ap1Vis = driver.find_element_by_id("player1CardsVisible")
        ap1VisBrowser2 = driver2.find_element_by_id("player1CardsVisible")
        self.assertEqual(ap1Score.get_attribute('outerHTML') , '<div id="player1Score">Score : 12</div>')
        self.assertEqual(ap1ScoreBrowser2.get_attribute('outerHTML') , '<div id="player1Score"></div>')
        self.assertEqual(ap1Vis.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/club.png">Q<img class="card" src="img/spade.png"></div>')
        self.assertEqual(ap1VisBrowser2.get_attribute('outerHTML') , '<div id="player1CardsVisible">Visible : A<img class="card" src="img/club.png">Q<img class="card" src="img/spade.png"></div>')

    def tearDown(self):
        InitServer.tearDownDriversAndServer(self.driver, self.driver2, self.p)

# if __name__ == "__main__":
#     unittest.main()
import unittest
from helpers.initServer import InitServer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class DealerBehavior(unittest.TestCase):

    def setUp(self):
        self.driver, self.driver2, self.p = InitServer.setupDriversAndServer()
    
    def test_dealer_hit_less_than_seventeen(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([12,13,22,23,25,26,1,9,36])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for Dealer
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 10<img class="card" src="img/club.png">J<img class="card" src="img/heart.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 10<img class="card" src="img/club.png">J<img class="card" src="img/heart.png"></div>')

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
    
    def test_dealer_hit_equal_to_seventeen(self):
        #If the dealer’s hand value is 17 and its hand contains an ace, then the dealer must hit.
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([12,13,22,23,25,26,0,5,15])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for Dealer
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 6<img class="card" src="img/club.png">3<img class="card" src="img/diamond.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 6<img class="card" src="img/club.png">3<img class="card" src="img/diamond.png"></div>')

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
    
    def test_dealer_stay_equal_to_seventeen(self):
        #If the dealer’s hand value is exactly 17 and that hand does not have an ace, the dealer must stay.
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([12,13,22,23,25,26,6,9,15])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for Dealer
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 10<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 10<img class="card" src="img/club.png"></div>')

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

    def test_dealer_stay_eighteen_or_greater(self):
        driver = self.driver
        driver2 = self.driver2
        self.assertIn("Blackjack", driver.title)
        self.assertIn("Blackjack", driver2.title)

        driver.execute_script("App.dealRigged([12,13,22,23,25,26,7,9,15])")
        # Click deal on Browser 1
        driver.find_element_by_id("deal").click()
        # Click stand on Browser 1
        driver.find_element_by_id("stand").click()
        # Click stand on Browser 2
        driver2.find_element_by_id("stand2").click()

        #Both Browsers should have the correct cards for Dealer
        dealerVis = driver.find_element_by_id("dealerCardsVisible")
        dealerVisBrowser2 = driver2.find_element_by_id("dealerCardsVisible")
        self.assertEqual(dealerVis.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 10<img class="card" src="img/club.png"></div>')
        self.assertEqual(dealerVisBrowser2.get_attribute('outerHTML') , '<div id="dealerCardsVisible">Visible : 10<img class="card" src="img/club.png"></div>')

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
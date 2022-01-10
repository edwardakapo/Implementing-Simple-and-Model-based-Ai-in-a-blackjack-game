import unittest
from testUiUpdates import UiUpdates
from testAiBehavior import AiBehavior
from testBothStandMultiplayer import BothStandMultiplayer
from testDealerBehavior import DealerBehavior
from testDealMultiplayer import DealMultiplayer
from testPlayRoundMultiplayer import PlayRoundMultiplayer
from testReportingResults import ReportingResults
from testSevenCardCharlie import SevenCardCharlie
from testCorrectScore import CorrectScore
from testPlayMultipleGames import PlayMultipleGames

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(UiUpdates))
    test_suite.addTest(unittest.makeSuite(PlayRoundMultiplayer))
    test_suite.addTest(unittest.makeSuite(BothStandMultiplayer))
    test_suite.addTest(unittest.makeSuite(DealMultiplayer))
    test_suite.addTest(unittest.makeSuite(ReportingResults))
    test_suite.addTest(unittest.makeSuite(AiBehavior))
    test_suite.addTest(unittest.makeSuite(DealerBehavior))
    test_suite.addTest(unittest.makeSuite(SevenCardCharlie))
    test_suite.addTest(unittest.makeSuite(CorrectScore))
    test_suite.addTest(unittest.makeSuite(PlayMultipleGames))
    return test_suite

if __name__ == "__main__":
    mySuite=suite()
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(mySuite)

# 3106 Blackjack

**Requirements**
* Python 3.8.2
    * Run `pip install -r requirements.txt` in the repository to download required python modules.
* npm 6.13.4
    * Run `npm install` in the repository to download required npm modules.
* ChromeDriver 96.0.4664.45
    * See https://chromedriver.chromium.org/downloads for installation details.

**Runtime Instructions**
* To run the server, first run `node server.js` or `npm init` in the repository. Then go to `http://localhost:3000` in two seperate browsers.

**Test Instructions**
* Run `python tests\testSuite.py` in the repository, which will run all the tests.

**Round Structure**
* In each round of the game, the players play their rounds in order (Player 1, then Player 2, then AI).
* The dealer makes a move only after all players/AI are done.

**Other Information**
* Simple Blackjack server using node and socket.io, based off of: 
    * https://github.com/mrward/node-blackjack/

* Public domain SVG images taken from The Noun Project:
    * http://thenounproject.com/noun/spade/#icon-No232
    * http://thenounproject.com/noun/diamond/#icon-No224
    * http://thenounproject.com/noun/heart/#icon-No187
    *  http://thenounproject.com/noun/club/#icon-No217

var cards = require('./cards');

// Blackjack game.
function BlackjackGame () {
    // Intialize Player Hands
    this.dealerHand = new BlackjackHand();
    this.aiPlayerHand = new BlackjackHand();    
    this.modelAiPlayerHand = new BlackjackHand();
    // Turn Index
    this.firstPlayerIndex = 0;
    this.secondPlayerIndex = 0;
    // Results
    this.result = 'None';
    this.result2 = 'None';
    this.aiResult = 'None';
    this.modelAiResult = 'None';
    // Deck
    this.cards = cards.createPlayingCards();
	this.AImoney = 1000;
    this.modelAImoney = 1000;
	this.prizePool = 0;
    // Active Player and List of Players
    this.players = [];
    this.activePlayer = new Player(0, new BlackjackHand());
}

// Rig the Deck to start with the cards in data
BlackjackGame.prototype.rigDeck = function(data){
    var splitData = String(data).split(',');
    splitData.forEach(c => {
        var card = parseInt(c);
        if(this.cards.cards.includes(card)){
            var indexInCards = this.cards.cards.indexOf(card);
            var indexInData = splitData.indexOf(c);
            if(indexInCards!=indexInData){
                this.cards.cards[indexInCards] = this.cards.cards[indexInData];
                this.cards.cards[indexInData] = parseInt(splitData[indexInData]);
            }
        }
    });
    console.log(this.cards.cards);
}

// Add a new player to the game
BlackjackGame.prototype.newPlayer = function (playerID) {
    this.players.push(new Player(playerID, new BlackjackHand()));
    // Set active player
    if(this.activePlayer == new Player(0, new BlackjackHand())) {
        this.activePlayer = this.players[0];
    }
}

// Remove a player from to the game
BlackjackGame.prototype.removePlayer = function(playerID) {
    var index = 0;
    this.players.forEach(player => {
        if(player.id == playerID) { index = this.players.indexOf(player); }
    });
    if (index > -1) { this.players.splice(index, 1); }
}

// Set the index of the first player in players
BlackjackGame.prototype.setFirstPlayerIndex = function(index) {
    this.firstPlayerIndex = index;
}

// Get the index of the first player in players
BlackjackGame.prototype.getFirstPlayerIndex = function() {
    return this.firstPlayerIndex;
}

// Set the index of the second player in players
BlackjackGame.prototype.setSecondPlayerIndex = function(index) {
    this.secondPlayerIndex = index;
}

// Get the index of the second player in players
BlackjackGame.prototype.getSecondPlayerIndex = function() {
    return this.secondPlayerIndex;
}

// Create a new Game of Blackjack
BlackjackGame.prototype.newGame = function () {
    // Intialize Player Hands
    this.aiPlayerHand = new BlackjackHand();
    this.dealerHand = new BlackjackHand();
    this.modelAiPlayerHand = new BlackjackHand();
    // Intialize all connected players
    this.players.forEach(element => {
        element.playerHand = new BlackjackHand();
        element.playerHand.addCard(this.cards.dealNextCard(), false);
        element.playerHand.addCard(this.cards.dealNextCard(), true);
        element.playerHand.score = element.playerHand.getScore();
    });
    // Deal cards to AI
    this.aiPlayerHand.addCard(this.cards.dealNextCard(), false);
    this.aiPlayerHand.addCard(this.cards.dealNextCard(), true);
    // Deal cards to Model AI
    this.modelAiPlayerHand.addCard(this.cards.dealNextCard(), false);
    this.modelAiPlayerHand.addCard(this.cards.dealNextCard(), true);
    // Deal cards to Dealer
    this.dealerHand.addCard(this.cards.dealNextCard(), false);
    this.dealerHand.addCard(this.cards.dealNextCard(), true);
    // Results
    this.result = 'None';
    this.result2 = 'None';
    this.aiResult = 'None';
    this.modelAiResult = 'None';
    // Active Player is the one who presses deal
    this.activePlayer = this.players[0];
}

// Reset the players hands and the deck 
BlackjackGame.prototype.resetHands = function () {
    // Deck
    this.cards = cards.createPlayingCards();
    // Intialize Player Hands
    this.aiPlayerHand = new BlackjackHand();
    this.dealerHand = new BlackjackHand();
    this.modelAiPlayerHand = new BlackjackHand();
    // Results
    this.result = 'None';
    this.result2 = 'None';
    this.aiResult = 'None';
    this.modelAiResult = 'None';
    // Players
    this.players.forEach(p => {
        p.playerHand = new BlackjackHand();
        // Reset round options
        p.roundOption = 'None';
    });
    // Reset Bets
    this.players[0].bet = 0;
    this.players[1].bet = 0;    
}


// Check if the game is in progress
BlackjackGame.prototype.isInProgress = function () {
    var playerResult = (this.result === 'None') && (this.result2 === 'None')
    var aiDealerResult = (this.dealerHand.hasCards()) && (this.aiResult === 'None') && (this.modelAiResult === 'None')
    return playerResult && aiDealerResult;
}

// Convert the game objects to JSON for the server/client
BlackjackGame.prototype.toJson = function () {
    return {
        dealer: {
            cards: this.dealerHand.getCards(),
            score: this.dealerHand.getScore(),
            visible: this.dealerHand.getVisibleCards(),
        },
        players : {
            players: this.players,
        },
        activePlayer: {
            cards: this.activePlayer.playerHand.getCards(),
            score: this.activePlayer.playerHand.getScore(),
            visible: this.activePlayer.playerHand.getVisibleCards(),
			money: this.activePlayer.money,
            id: this.activePlayer.id,
        },
        ai: {
            cards: this.aiPlayerHand.getCards(),
            score: this.aiPlayerHand.getScore(),
			money: this.AImoney,
            visible: this.aiPlayerHand.getVisibleCards(),
        },
        modelAi: {
            cards: this.modelAiPlayerHand.getCards(),
            score: this.modelAiPlayerHand.getScore(),
			money: this.modelAImoney,
            visible: this.modelAiPlayerHand.getVisibleCards(),
        },
        result: this.result,
        result2: this.result2,
        aiResult: this.aiResult,
        modelAiResult: this.modelAiResult,
		prizePool: this.prizePool,
        firstPlayerIndex: this.getFirstPlayerIndex(),
        secondPlayerIndex: this.getSecondPlayerIndex()
    };
}

// Check if the active player has busted
BlackjackGame.prototype.getResultForPlayerBust = function () {
    var score = this.activePlayer.playerHand.getScore();
    if (score > 21) {
        this.activePlayer.roundOption = 'Stand';
        return 'Bust';
    }
    return 'None';
}

// Move active player to the next player
BlackjackGame.prototype.advanceActivePlayer = function() {
    if(this.players.indexOf(this.activePlayer) == 1) {
        this.activePlayer = this.players[0];
    }
    else {
        this.activePlayer = this.players[1];
    }
}
//Betting
BlackjackGame.prototype.AiBet = function (amount){
    var intAmount = parseInt(amount)
	this.AImoney -= intAmount;
	this.prizePool += intAmount;
}

BlackjackGame.prototype.AiWinMoney = function (){
	// this.AiMoney += parseInt(this.prizePool);
    this.AiMoney += 50 // Constant bet of 25
	this.prizePool = 0;
}

BlackjackGame.prototype.bet = function (Player, amount){
    var intAmount = parseInt(amount)
    Player.bet = intAmount;
	Player.money -= intAmount;
	this.prizePool += intAmount;
}

BlackjackGame.prototype.winMoney = function (Player){
	Player.money += parseInt(this.prizePool);
	this.prizePool = 0;
}

BlackjackGame.prototype.betPlayerNumber = function (playerNumber, amount){
    var intAmount = parseInt(amount)
    this.players[playerNumber-1].bet = intAmount;
	this.players[playerNumber-1].money -= intAmount;
	this.prizePool += intAmount;
}

BlackjackGame.prototype.betAiNumber = function (amount, ai){
    var intAmount = parseInt(amount)
    if(ai == 'Basic') {
        this.AImoney -= intAmount;
        this.prizePool += intAmount;
    }
    else if(ai == 'Model') {
        this.modelAImoney -= intAmount;
        this.prizePool += intAmount;
    }
}

BlackjackGame.prototype.getPlayerNumberbet = function (playerNumber){
    return this.players[playerNumber-1].bet;
}

// Check if the AI player has busted
BlackjackGame.prototype.getResultForAiPlayerBust = function (aiNumber) {
    if(aiNumber == 'Basic') {
        var score = this.aiPlayerHand.getScore();
        if (score > 21) {
            return 'Bust';
        }
        return 'None';
    } 
    else if(aiNumber == 'Model') {
        var score = this.modelAiPlayerHand.getScore();
        if (score > 21) {
            return 'Bust';
        }
        return 'None';
    }
}

// Check if there are still players who need to play
BlackjackGame.prototype.isGameInProgress = function () {
    var opt1 = this.result === 'None' && this.result2 === 'None';
    var opt2 = this.result === 'Bust' && this.result2 === 'None';
    var opt3 = this.result === 'None' && this.result2 === 'Bust';
    return opt1 || opt2 || opt3;
}

// Game Hit Function
BlackjackGame.prototype.hit = function () {
    if (this.isGameInProgress()) {
        // Set their turn choice
        this.activePlayer.roundOption = 'Hit';
        // Deal out the next card in the deck
        var card = this.cards.dealNextCard();
        this.activePlayer.playerHand.addCard(card, true);
        // Check for Busts
        if(this.players.indexOf(this.activePlayer) == 1){
            this.result2 = this.getResultForPlayerBust();
        }else {
            this.result = this.getResultForPlayerBust();
        }
        // Declare 7 Card Charlie if exists and end game
        if(this.activePlayer.playerHand.getCards().length == 7 && this.activePlayer.playerHand.getScore() <= 21){
            if(this.players.indexOf(this.activePlayer) == 1){
                this.result2 = "Win - 7 Card Charlie";
                this.result = "Lose";
                this.aiResult = "Lose";
                this.modelAiResult = "Lose";
            }
            else {
                this.result = "Win - 7 Card Charlie";
                this.result2 = "Lose";
                this.aiResult = "Lose";
                this.modelAiResult = "Lose";
            }
			this.winMoney(this.activePlayer);
            return "End";
        }
        // Check if both players have acted
        choiceCount = 0;
        this.players.forEach(p => {
            if(p.roundOption != 'None'){
                choiceCount++;
            }
        })
        // Move to next player or play AI and dealer turns if both players are finished the round
        if(choiceCount == 1) {
            this.advanceActivePlayer();
            return 'None';
        }
        else if(choiceCount == 2) {
            this.playAiTurn();
            // this.playDealerTurn();
            //Reset turn choices if not both stay
            hitCount = 0;
            this.players.forEach(p => {
                if(p.roundOption === 'Hit'){
                    p.roundOption = 'None';
                    hitCount++;
                }
            });
            //If both players have stood/busted end the game
            standCount = 0;
            this.players.forEach(p => {
                if(p.roundOption === 'Stand'){
                    standCount++;
                }
            });
            if(standCount == 2) {
                //AI + Dealer Results
                while(this.aiResult == 'None' || this.modelAiResult == 'None') {
                    //Both players are done, so finish up the AI's moves
                    this.playAiTurn();
                }
                this.playDealerTurn();

                // Player 1 Result
                this.result = this.getResultForPlayer(this.players[this.firstPlayerIndex]);
                // Player 2 Result
                if(this.firstPlayerIndex == 1){
                    this.result2 = this.getResultForPlayer(this.players[0]);
                }else {
                    this.result2 = this.getResultForPlayer(this.players[1]);
                }

                // Determine the actual winner and return an end signal
                this.determineActualWinner();
                return 'End';
            }
            else {
                //Else if both players have not stood
                this.advanceActivePlayer();
            }
        }
    }
    return 'None';
}

// AI Hit function
BlackjackGame.prototype.hitAi = function (aiDesc) {
    // if (this.isGameInProgress()) {
        var card = this.cards.dealNextCard();
        if(aiDesc == 'Basic'){
            this.aiPlayerHand.addCard(card, true);
            this.aiResult = this.getResultForAiPlayerBust(aiDesc);
        }
        else if(aiDesc == 'Model'){
            this.modelAiPlayerHand.addCard(card, true);
            this.modelAiResult = this.getResultForAiPlayerBust(aiDesc);
        }
    // }
}

// Get the AI players final result
BlackjackGame.prototype.getAiResult = function (aiDesc) {
    var dealerScore = this.dealerHand.getScore();

    if(aiDesc == 'Basic'){
        var aiScore = this.aiPlayerHand.getScore();

        if (this.aiPlayerHand.isBust()) {
            return 'Bust';
        }
        else if (this.dealerHand.isBust()) {
            return 'Win';
        }
        if (aiScore > dealerScore) {
            return 'Win';
        } else if (aiScore == dealerScore) {
            return 'Push';
        }
        return 'Lose';
    }
    else if(aiDesc == 'Model'){
        var aiScore = this.modelAiPlayerHand.getScore();
        
        if (this.modelAiPlayerHand.isBust()) {
            return 'Bust';
        }
        else if (this.dealerHand.isBust()) {
            return 'Win';
        }
        if (aiScore > dealerScore) {
            return 'Win';
        } else if (aiScore == dealerScore) {
            return 'Push';
        }
        return 'Lose';
    }

}

// Get a given players final result
BlackjackGame.prototype.getResultForPlayer = function(player) {
    var playerScore = player.playerHand.getScore()
    var dealerScore = this.dealerHand.getScore();
    if (player.playerHand.isBust()) {
        return 'Bust';
    }
    else if (this.dealerHand.isBust()) {
        return 'Win';
    }
    if (playerScore > dealerScore) {
        return 'Win';
    } else if (playerScore === dealerScore) {
        return 'Push';
    }
    return 'Lose';
}

// Get the active players result 
BlackjackGame.prototype.getResult = function () {
    var playerScore = this.activePlayer.playerHand.getScore()
    var dealerScore = this.dealerHand.getScore();
    if (this.activePlayer.playerHand.isBust()) {
        return 'Bust';
    }
    else if (this.dealerHand.isBust()) {
        return 'Win';
    }
    if (playerScore > dealerScore) {
        return 'Win';
    } else if (playerScore === dealerScore) {
        return 'Push';
    }
    return 'Lose';
}

// Determine the real with with respect to hand sizes and values
BlackjackGame.prototype.determineActualWinner = function() {
    // Exit if AI got a 7 Card Charlie
    if(this.aiResult == "Win - 7 Card Charlie"){
        this.result2 = "Lose";
        this.result = "Lose";
        this.modelAiResult = "Lose";
		this.AiWinMoney();
        return
    }

    var winPlayers = [];
    if(this.aiResult == "Win"){
        winPlayers.push(new Player("AI1", this.aiPlayerHand));
    }
    if(this.modelAiResult == "Win"){
        winPlayers.push(new Player("AI2", this.modelAiPlayerHand));
    }
    if(this.result == "Win" || this.result == "Push"){
        winPlayers.push(this.players[0]);
    }
    if(this.result2 == "Win" || this.result2 == "Push"){
        winPlayers.push(this.players[1]);
    }
    // Find the highest score and remove lower players
    var maxScorePlayer = 0;
    winPlayers.forEach(p => {
        if(p.playerHand.getScore() > maxScorePlayer) {
            maxScorePlayer = p.playerHand.getScore();
        }
    });
    removePlayers = [];
    winPlayers.forEach(p => {
        if(p.playerHand.getScore() < maxScorePlayer) {
            removePlayers.push(p);
            if(this.players.indexOf(p) == 1){
                this.result2 = "Lose";
            }
            if(this.players.indexOf(p) == 0){
                this.result = "Lose";
            }
            if(p.id == "AI1"){
                this.aiResult = "Lose";
            }
            if(p.id == "AI2"){
                this.modelAiResult = "Lose";
            }
        }
    });
    removePlayers.forEach(i => {
        winPlayers.splice(winPlayers.indexOf(i), 1);
    });
    // Find the smallest hand length and adjust results
    var minLengthPlayer = 100;
    winPlayers.forEach(p => {
        if(p.playerHand.getCards().length < minLengthPlayer) {
            minLengthPlayer = p.playerHand.getCards().length;
        }
    });
    winPlayers.forEach(p => {
        if(p.playerHand.getCards().length > minLengthPlayer) {
            if(this.players.indexOf(p) == 1){
                this.result2 = "Lose";
            }
            if(this.players.indexOf(p) == 0){
                this.result = "Lose";
            }
            if(p.id == "AI1"){
                this.aiResult = "Lose";
            }
            if(p.id == "AI2"){
                this.modelAiResult = "Lose";
            }
        }
    });

    if(this.result2 == "Win"){
        this.players[1].money += (parseInt(this.players[1].bet) * 2)
    }

    if(this.result == "Win"){
        this.players[0].money += (parseInt(this.players[0].bet) * 2)
    }

    if(this.aiResult == "Win"){
        this.AImoney += 50
    }

    if(this.modelAiResult == "Win"){
        this.modelAImoney += 50
    }


    if(this.result2 == "Push"){
        this.players[1].money += (parseInt(this.players[1].bet))
    }

    if(this.result == "Push"){
        this.players[0].money += (parseInt(this.players[0].bet))
    }

    if(this.aiResult == "Push"){
        this.AImoney += 25
    }

    if(this.modelAiResult == "Push"){
        this.modelAImoney += 25
    }

	this.prizePool = 0;
}

// Play the dealers turn
BlackjackGame.prototype.playDealerTurn = function() {
    // Check if Dealer has Ace
    var dealerScore = this.dealerHand.getScore();
    var hasAce = false;
    this.dealerHand.getCards().forEach(card => {
        if(card.rank == 1){
            hasAce = true;
        }
    });

    // Dealer plays last (After everyone is done) so do all their moves at once.
    while(dealerScore < 17 || dealerScore == 17 && hasAce){
        //Check if Dealer has Ace
        dealerScore = this.dealerHand.getScore();
        hasAce = false;
        this.dealerHand.getCards().forEach(card => {
            if(card.rank == 1){
                hasAce = true;
            }
        });
        // if its hand’s value is less than 17, it must hit. 
        if(dealerScore < 17) {
            var card = this.cards.dealNextCard();
            this.dealerHand.addCard(card, true);
        }
        // Equal to 17 with ace = hit
        else if(dealerScore == 17 && hasAce){
            var card = this.cards.dealNextCard();
            this.dealerHand.addCard(card, true);
        }
        // Stay
        else if(dealerScore == 17 && !hasAce){ }
        else if(dealerScore >= 18) { }
    }
}

BlackjackGame.prototype.playAiTurn = function(){
    if(this.aiResult == 'None'){
        this.playBasicAiTurn();
    }
    if(this.modelAiResult == 'None'){
        this.playModelAiTurn();
    }
}

// Play the Basic AI's turn
BlackjackGame.prototype.playBasicAiTurn = function() {
    if(this.aiResult=="None"){
        // Get players visible hands
        var aiScore = this.aiPlayerHand.getScore();
        var visibleScores = [];
        var visibleLengths = [];
        this.players.forEach(element => {
            visibleScores.push(element.playerHand.getVisibleScore())
            visibleLengths.push(element.playerHand.getVisibleCards().length)
        });

        //Stay
        if(aiScore==21){ this.aiResult = this.getAiResult('Basic'); }
        //if a human player currently has a single visible card and this visible card is an ace or a card of value 10
        else if(visibleLengths.includes('1') && 
                    (visibleScores[visibleLengths.indexOf('1')] == 10 || visibleScores[visibleLengths.indexOf('1')] == 1)){
            //Then hit
            this.hitAi('Basic');
        }
        //else if the current value of the hand of the AI player is between 18 and 20
        else if(aiScore >= 18 && aiScore <= 20){
            //then if any other player has visible cards that add up to strictly more than the AI player’s hand’s value minus 10
            var scoreLarger = false;
            visibleScores.forEach(score => {
                if(score > (aiScore - 10) ){
                    scoreLarger = true;
                }
            });
            //Then Hit
            if(scoreLarger){ this.hitAi('Basic'); }
            //Stay
            else{ this.aiResult = this.getAiResult('Basic'); }
        }
        //Hit
        else { this.hitAi('Basic'); }

        // Check for 7 card charlie
        if(this.aiPlayerHand.getCards().length == 7 && this.aiPlayerHand.getScore() <= 21){
                this.aiResult = "Win - 7 Card Charlie";
                this.result = "Lose";
                this.result2 = "Lose";
                this.modelAiResult = "Lose";
				this.AiWinMoney();
        }
    }
}

// Play the model Ais turn
BlackjackGame.prototype.playModelAiTurn = function(){
	if(this.modelAiResult == "None"){
		var aiScore = this.modelAiPlayerHand.getScore();
		var visibleScores = [];
        this.players.forEach(element => {
            visibleScores.push(element.playerHand.getVisibleScore())
        });
		if(aiScore <= 11){
			//always hit
			this.hitAi('Model');
		}
		else if(aiScore >= 17){
			//always stand
			this.modelAiResult = this.getAiResult('Model');
		}
		else {
			// 
			var descisionArr = [];
			visibleScores.forEach(element => {descisionArr.push(makeDescision(aiScore, element))})
			var choice = descisionArr.reduce(myfunc = (total, num) => {return total + num}, 0);
			if(choice < 2){
				// stand
				this.modelAiResult = this.getAiResult('Model');
			}
			else{
				this.hitAi('Model');
			}

		}		
	}
}

function makeDescision(aiScore, playerScore){

    if(aiScore >= 14 && aiScore <= 16){
        if(playerScore > 6){
            return 1;
        }
        else{
            return 0;
        }
    }
    else{
        if(playerScore > 6 ){
            return 1;
        }
        else if(aiScore == 13 && (playerScore > 2 || playerScore < 7)){
            return 0;
        }
        else if((aiScore == 13 || aiScore == 12) && playerScore == 2){
            return 1;
        }
        else if(aiScore == 12 && (playerScore == 3 || playerScore == 4 || playerScore == 6 )){
            return 0;
        }
        else if(aiScore == 12 && playerScore == 5){
            return 1;
        }
    }


}

// Game Stand function
BlackjackGame.prototype.stand = function () {
    if (this.isGameInProgress()) {
        // Set active players turn choice
        this.activePlayer.roundOption = 'Stand';
        // Check if both players have made an action
        choiceCount = 0;
        this.players.forEach(p => {
            if(p.roundOption != 'None'){
                choiceCount++;
            }
        });
        // Move to next player or play AI and dealer turns if both players are finished the round
        if(choiceCount == 1) {
            this.advanceActivePlayer();
            return 'None';
        }
        else if(choiceCount == 2) {
            this.playAiTurn();
            // this.playDealerTurn();
        }
        //If both players have stood end the game
        standCount = 0;
        this.players.forEach(p => {
            if(p.roundOption == 'Stand'){
                standCount++;
            }
        });
        if(standCount == 2) {
            //AI + Dealer Results
            while(this.aiResult == 'None' || this.modelAiResult == 'None') {
                //Both players are done, so finish up the AI's moves
                this.playAiTurn();
            }
            this.playDealerTurn();

            this.result = this.getResultForPlayer(this.players[this.firstPlayerIndex]);
            if(this.firstPlayerIndex == 1){
                this.result2 = this.getResultForPlayer(this.players[0]);
            }else {
                this.result2 = this.getResultForPlayer(this.players[1]);
            }

            this.determineActualWinner();
            return 'End';
        }
        else { this.advanceActivePlayer(); }
    }
    return 'None';
}

// Player object
function Player(playerID, playerHand) {
    this.id = playerID;
    this.roundOption = 'None';
    this.playerHand = playerHand;
	this.money = 1000;
    this.bet = 0;
}


// Blackjack hand.
function BlackjackHand() {
    this.cards = [];
    this.visibleCards = [];
    this.score = 0;
}

BlackjackHand.prototype.hasCards = function () {
    return this.cards.length > 0;
}

BlackjackHand.prototype.addCard = function (card, isVisible) {
    this.cards.push(card);
    if(isVisible) { this.visibleCards.push(card); }
}

BlackjackHand.prototype.numberToSuit = function (number) {
  var suits = ['C', 'D', 'H', 'S'];
  var index = Math.floor(number / 13);
  return suits[index];
}

BlackjackHand.prototype.numberToCard = function (number) {
  return {
    rank: (number % 13) + 1,
    suit: this.numberToSuit(number)
  };
}

BlackjackHand.prototype.getVisibleCards = function () {
    var convertedCards = [];
    for (var i = 0; i < this.visibleCards.length; i++) {
        var number = this.visibleCards[i];
        convertedCards[i] = this.numberToCard(number);
    }
    return convertedCards;
}

BlackjackHand.prototype.getCards = function () {
    var convertedCards = [];
    for (var i = 0; i < this.cards.length; i++) {
        var number = this.cards[i];
        convertedCards[i] = this.numberToCard(number);
    }
    return convertedCards;
}

BlackjackHand.prototype.getCardScore = function (card) {
    if (card.rank === 1) {
        return 11;
    } else if (card.rank >= 11) {
        return 10;
    }
    return card.rank;
}

BlackjackHand.prototype.getVisibleScore = function() {
    var score = 0;
    var cards = this.getVisibleCards();
    var aces = [];

    // Sum all cards excluding aces.
    for (var i = 0; i < cards.length; ++i) {
        var card = cards[i];
        if (card.rank === 1) {
            aces.push(card);
        } else {
            score = score + this.getCardScore(card);
        }
    }

    // Add aces.
    if (aces.length > 0) {
        var acesScore = aces.length * 11;
        var acesLeft = aces.length;
        while ((acesLeft > 0) && (acesScore + score) > 21) {
            acesLeft = acesLeft - 1;
            acesScore = acesScore - 10;
        }
        score = score + acesScore;
    }

    return score;
}

BlackjackHand.prototype.getScore = function () {
    var score = 0;
    var cards = this.getCards();
    var aces = [];

    // Sum all cards excluding aces.
    for (var i = 0; i < cards.length; ++i) {
        var card = cards[i];
        if (card.rank === 1) {
            aces.push(card);
        } else {
            score = score + this.getCardScore(card);
        }
    }

    // Add aces.
    if (aces.length > 0) {
        var acesScore = aces.length * 11;
        var acesLeft = aces.length;
        while ((acesLeft > 0) && (acesScore + score) > 21) {
            acesLeft = acesLeft - 1;
            acesScore = acesScore - 10;
        }
        score = score + acesScore;
    }

    this.score = score;
    return score;
}

BlackjackHand.prototype.isBust = function () {
    return this.getScore() > 21;
}

// Exports.
function newGame () {
    return new BlackjackGame();
}
function main(){
	game = newGame();
	game.newPlayer(100);
	game.newPlayer(200);
	game.setFirstPlayerIndex(0);
	game.setSecondPlayerIndex(1);
	console.log(game.players);
	console.log(game.prizePool);
	game.bet(game.players[game.firstPlayerIndex], 100);
	game.advanceActivePlayer();
	game.bet(game.players[game.secondPlayerIndex], 100);
	game.AiBet(100);
	game.advanceActivePlayer();
	console.log(game.players);
	console.log(game.prizePool);
	
	//game.rigDeck([5,10,49,50,39,48,19,22,37]);
	game.newGame();
	console.log("cards have been dealt");
	console.log();
	console.log(game.players);
	
	game.hit();
	console.log("player 1 hit");
	console.log("Game players: ");
	game.players.forEach(player => console.log("player : " , player.id, "visible cars" , player.playerHand));
	console.log();
	console.log("Game object:");
	console.log(game.toJson());

	console.log();
	console.log("AI hand: ", game.aiPlayerHand);

	console.log();
	game.stand();
	console.log("player 2 stands");
	console.log("Game players: ");
	console.log(game.players);
	console.log("Game object:");
	console.log(game.toJson());

}
// main();

exports.newGame = newGame

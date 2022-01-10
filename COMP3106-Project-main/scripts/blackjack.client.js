var App = {}

App.deal = function () {
    App.socket.emit('deal');
}

App.hit = function () {
    App.socket.emit('hit');
}

App.stand = function () {
    App.socket.emit('stand');
}

App.dealRigged = function(data) {
    App.socket.emit('deal-rigged', data);
}

App.bet = function(playerNumber, ammount) {
    App.socket.emit('bet', {pIndex: playerNumber, betTotal: ammount})
    App.styleGivenPlayer(playerNumber);
}

App.getSuitHtml = function (suit) {
    var image = 'club.png';
    if (suit === 'H') {
        image = 'heart.png';
    } else if (suit === 'S') {
        image = 'spade.png';
    } else if (suit === 'D') {
        image = 'diamond.png';
    }
    return "<img class='card' src='img/" + image + "'/>";
}

App.getRankHtml = function (rank) {
    if (rank === 1) {
        return 'A';
    } else if (rank === 11) {
        return 'J';
    } else if (rank === 12) {
        return 'Q';
    } else if (rank === 13) {
        return 'K';
    }
    return rank;
}

App.getCardsHtml = function (cards) {
    var html = '';
    for (var i = 0; i < cards.length; i++) {
        var card = cards[i];
        html += App.getRankHtml(card.rank);
        html += App.getSuitHtml(card.suit);
    }
    return html;
}

App.numberToCard = function (number) {
    return {
      rank: (number % 13) + 1,
      suit: ['C', 'D', 'H', 'S'][Math.floor(number / 13)]
    };
}

App.getObjectCardsHtml = function (cards) {
    var html = '';
    for (var i = 0; i < cards.length; i++) {
        var card = App.numberToCard(cards[i]);
        html += App.getRankHtml(card.rank);
        html += App.getSuitHtml(card.suit);
    }
    return html;
}

App.updateAiVisibleCards = function (aiPlayer1, aiPlayer2) {
    var html = App.getCardsHtml(aiPlayer1.visible);
    var html2 = App.getCardsHtml(aiPlayer2.visible);
    $('#aiCardsVisible').html("Visible : " + html);
    $('#modelAiCardsVisible').html("Visible : " + html2);

}

App.updateDealerVisibleCards = function (dealer) {
    var html = App.getCardsHtml(dealer.visible);
    $('#dealerCardsVisible').html("Visible : " + html);
}

App.updatePlayer = function (player) {
    var html = App.getCardsHtml(player.cards);
    var html2 = App.getCardsHtml(player.visible);
    $('#playerCards').html("Hand : " + html);
    $('#playerCardsVisible').html("Visible : " + html2);
    $('#playerScore').text("Score : " + player.score);
}

App.updatePlayers = function (players) {
    for(let i = 0; i < Object.values(players)[0].length; i++) {
        var html = App.getObjectCardsHtml(Object.values(players)[0][i].playerHand.cards);
        var html2 = App.getObjectCardsHtml(Object.values(players)[0][i].playerHand.visibleCards);
        var playerCards = '#player' + (i+1) + 'Cards';
        var playerScore = '#player' + (i+1) + 'Score';
        var playerCardsVisible = '#player' + (i+1) + 'CardsVisible';
        $(playerCards).html("Hand : " + html);
        $(playerCardsVisible).html("Visible : " + html2);
        $(playerScore).text("Score : " + Object.values(players)[0][i].playerHand.score);
    }
}

App.printAiIfBusted = function(aiResult, ai) {
    if(aiResult=="Bust"){
        var html = App.getCardsHtml(ai.visible);
        $('#aiCardsVisible').html("Visible : " + html);
        $('#aiResult').text(aiResult);
    }
}

App.printModelAiIfBusted = function(aiResult, ai) {
    if(aiResult=="Bust"){
        var html = App.getCardsHtml(ai.visible);
        $('#modelAiCardsVisible').html("Visible : " + html);
        $('#modelAiResult').text(aiResult);
    }
}

App.setAllVisible = function(ai, dealer, ai2) {
    var html = App.getCardsHtml(ai.cards);
    var html2 = App.getCardsHtml(dealer.cards);
    var html3 = App.getCardsHtml(ai.visible);
    var html4 = App.getCardsHtml(dealer.visible);
    var html5 = App.getCardsHtml(ai2.cards);
    var html6 = App.getCardsHtml(ai2.visible);

    $('#dealerCards').html("Hand : " + html2);
    $('#dealerCardsVisible').html("Visible : " + html4);
    $('#dealerScore').text("Score : " + dealer.score);

    $('#aiCards').html("Hand : " + html);
    $('#aiCardsVisible').html("Visible : " + html3);
    $('#aiScore').text("Score : " + ai.score);

    $('#modelAiCards').html("Hand : " + html5);
    $('#modelAiCardsVisible').html("Visible : " + html6);
    $('#modelAiScore').text("Score : " + ai2.score);
}

App.updateAIResult = function (result) {
    var displayResult = result;
    if (result === 'None') {
        displayResult = '';
    }
    $('#aiResult').text(displayResult);
}

App.updateModelAIResult = function (result) {
    var displayResult = result;
    if (result === 'None') {
        displayResult = '';
    }
    $('#modelAiResult').text(displayResult);
}

App.updateResult = function (result) {
    var displayResult = result;
    if (result === 'None') {
        displayResult = '';
    }
    $('#result').text(displayResult);
}

App.updateResultPlayer2 = function (result) {
    var displayResult = result;
    if (result === 'None') {
        displayResult = '';
    }
    $('#result2').text(displayResult);
}

App.updatePlayerMoneyBalances = function (players) {
    for(let i = 0; i < Object.values(players)[0].length; i++) {
        var playerMoney = '#player' + (i+1) + 'Money';
        $(playerMoney).text("Money : " + Object.values(players)[0][i].money + "$");
    }
}

App.updateAiMoneyBalances = function (ai, ai2) {
    $('#aiMoney').text("Money : " + ai.money + "$");
    $('#modelAiMoney').text("Money : " + ai2.money + "$");
}

App.updateP1BetResult = function (p1Bet) {
    $('#player1Bet').text("Bet : " + p1Bet + "$");
    $('.betForm1').hide();
}

App.updateP2BetResult = function (p2Bet) {
    $('#player2Bet').text("Bet : " + p2Bet + "$");
    $('.betForm2').hide();
}

App.updateAiBets = function (ai1Bet, ai2Bet) {
    $('#aiBet').text("Bet : " + ai1Bet + "$");
    $('#modelAiBet').text("Bet : " + ai2Bet + "$");

}

App.styleGivenPlayer = function(playerNumber) {
    $('body > div:nth-child(3) > div:nth-child(' + playerNumber + ')').removeClass("type1").addClass("typeActive");
}

App.styleActivePlayer = function(firstPlayer) {
    if(firstPlayer) {
        // Change P1 Colour
        $('body > div:nth-child(3) > div:nth-child(1)').removeClass("type1").addClass("typeActive");
    } else {
        // Change P2 Colour
        $('body > div:nth-child(3) > div:nth-child(2)').removeClass("type1").addClass("typeActive");
    }
}

App.updatePlayerOneVisible = function (players, game) {
    var playerObj = Object.values(players)[0][game.firstPlayerIndex];
    var html = App.getObjectCardsHtml(playerObj.playerHand.cards);
    var html2 = App.getObjectCardsHtml(playerObj.playerHand.visibleCards);
    $('#player'+1+'Cards').html("Hand : " + html);
    $('#player'+1+'CardsVisible').html("Visible : " + html2);
    $('#player'+1+'Score').text("Score : " + playerObj.playerHand.score);
    //Refresh Other players visible cards
    var playerObj2 = Object.values(players)[0][game.secondPlayerIndex];
    var html3 = App.getObjectCardsHtml(playerObj2.playerHand.visibleCards);
    $('#player'+2+'CardsVisible').html("Visible : " + html3);
}

App.updatePlayerTwoVisible = function (players, game) {
    var playerObj = Object.values(players)[0][game.secondPlayerIndex];
    var html = App.getObjectCardsHtml(playerObj.playerHand.cards);
    var html2 = App.getObjectCardsHtml(playerObj.playerHand.visibleCards);
    $('#player'+2+'Cards').html("Hand : " + html);
    $('#player'+2+'CardsVisible').html("Visible : " + html2);
    $('#player'+2+'Score').text("Score : " + playerObj.playerHand.score);
    //Refresh Other players visible cards
    var playerObj2 = Object.values(players)[0][game.firstPlayerIndex];
    var html3 = App.getObjectCardsHtml(playerObj2.playerHand.visibleCards);
    $('#player'+1+'CardsVisible').html("Visible : " + html3);
}

App.disableButton = function (id) {
    $(id).attr('disabled', 'disabled');
}

App.enableButton = function (id) {
    $(id).removeAttr('disabled');
}

App.toggleButton = function (id) {
    $(id).prop('disabled', function(index, isDisabled) { return !isDisabled; });
}

App.disableAllButtons = function () {
    App.disableButton('#deal');
    App.disableButton('#hit');
    App.disableButton('#stand')
    App.disableButton('#deal2');
    App.disableButton('#hit2');
    App.disableButton('#stand2')
}

App.disableDeal = function () {
    App.disableButton('#deal');
    App.enableButton('#hit');
    App.enableButton('#stand');
}

App.enableDeal = function () {
    App.enableButton('#deal');
    App.disableButton('#hit');
    App.disableButton('#stand');
}

App.enableDeal2 = function () {
    App.enableButton('#deal2');
    App.disableButton('#hit2');
    App.disableButton('#stand2');
}

App.enableDealIfGameFinished = function (result) {
    if (result !== 'None') {
        App.enableDeal();
    }
}

App.clearVisibleElements = function() {
    $('#player1Cards').empty();
    $('#player1CardsVisible').empty();
    $('#player1Score').empty();
    $('#result').empty();
    $('#player2Cards').empty();
    $('#player2CardsVisible').empty();
    $('#player2Score').empty();
    $('#result2').empty();
    $('#aiCards').empty();
    $('#aiCardsVisible').empty();
    $('#aiScore').empty();
    $('#aiResult').empty();
    $('#modelAiCards').empty();
    $('#modelAiCardsVisible').empty();
    $('#modelAiScore').empty();
    $('#modelAiResult').empty();
    $('#dealerCards').empty();
    $('#dealerCardsVisible').empty();
    $('#dealerScore').empty();
}

App.newGameUpdate = function(game) {
    App.clearVisibleElements();
    // Remove the active green highlight
    // $("div.circleBase").addClass('type1').removeClass('typeActive');
    // Change P1 Colour
    $('body > div:nth-child(3) > div:nth-child(1)').removeClass("typeActive").addClass("type1");
    // Change P2 Colour
    $('body > div:nth-child(3) > div:nth-child(2)').removeClass("typeActive").addClass("type1");
}

App.endGameUpdate = function(game) {
    // Update Players and set everything to visible
    App.updatePlayers(game.players);
    App.setAllVisible(game.ai, game.dealer, game.modelAi);
    App.updateAIResult(game.aiResult);
    App.updateModelAIResult(game.modelAiResult);
    App.updateResult(game.result);
    App.updateResultPlayer2(game.result2);
    // Reset buttons
    App.enableButton('#deal');
    App.disableButton('#hit');
    App.disableButton('#stand');
    App.enableButton('#deal2');
    App.disableButton('#hit2');
    App.disableButton('#stand2');
    // Update balances
    App.updatePlayerMoneyBalances(game.players);
    App.updateAiMoneyBalances(game.ai, game.modelAi);
    // Update bets
    // App.updateP1BetResult(0);
    // App.updateP1BetResult(0);
    $('#player1Bet').empty();
    $('#player2Bet').empty();
    $('#aiBet').empty();
    $('#modelAiBet').empty();
    // Display betting input
    $('.betForm1').show();
    $('.betForm2').show();
    // Disable buttons
    App.disableAllButtons();
}

App.dealResult = function (game, curIndex) {
    //Whoever pressed deal should have the other player greyed out
    App.disableDeal();

    if(curIndex == game.firstPlayerIndex) {
        App.disableButton('#deal2');
        App.disableButton('#hit2');
        App.disableButton('#stand2');
        App.updatePlayerOneVisible(game.players, game);
        App.styleActivePlayer(true);
    }
    else {
        App.disableButton('#deal');
        App.disableButton('#hit');
        App.disableButton('#stand');
        App.disableButton('#hit2');
        App.disableButton('#stand2');
        App.disableButton('#deal2');
        App.updatePlayerTwoVisible(game.players, game);
        App.styleActivePlayer(false);
    }

    App.updatePlayerMoneyBalances(game.players);
    App.updateAiMoneyBalances(game.ai, game.modelAi);

    App.updateAiVisibleCards(game.ai, game.modelAi);
    App.updateDealerVisibleCards(game.dealer);
    App.updateResult(game.result);
    App.updateResultPlayer2(game.result2);
    App.updateAIResult(game.aiResult);
    App.updateModelAIResult(game.modelAiResult);
}

App.hitResult = function (game, curIndex, p1Index) {
    // Check if player1
    if(curIndex == game.firstPlayerIndex) {
        App.updatePlayerOneVisible(game.players, game);
        App.updateResult(game.result);
    } else {
        App.updatePlayerTwoVisible(game.players, game);
        App.updateResultPlayer2(game.result2);
    }
    App.updateDealerVisibleCards(game.dealer);
    App.updateAiVisibleCards(game.ai, game.modelAi);
}

App.standResult = function (game, curIndex, pIndex) {
    // Check if player1
    if(curIndex == game.firstPlayerIndex){
        App.updatePlayerOneVisible(game.players, game);
        App.updateResult(game.result);
    } else {
        App.updatePlayerTwoVisible(game.players, game);
        App.updateResultPlayer2(game.result2);
    }
    App.updateDealerVisibleCards(game.dealer);
    App.updateAiVisibleCards(game.ai, game.modelAi);
}

App.updateTurnUI = function(game, curIndex, pIndex) {
    //P1 has ended turn
    if(curIndex == pIndex) {
        App.toggleButton('#hit');
        App.toggleButton('#stand');
        App.updatePlayerOneVisible(game.players, game);
    }
    //P2 Has Ended Turn
    else {
        App.toggleButton('#hit2');
        App.toggleButton('#stand2');
        App.updatePlayerTwoVisible(game.players, game);
    }

    if(game.aiResult == "Bust"){
        App.printAiIfBusted(game.aiResult, game.ai);
    } 
    else if(game.modelAiResult == "Bust"){
        App.printModelAiIfBusted(game.modelAiResult, game.modelAi);
    }
    else {
        App.updateAiVisibleCards(game.ai, game.modelAi);
    }

    App.updateDealerVisibleCards(game.dealer);
    App.updateResult(game.result);
    App.updateResultPlayer2(game.result2);
}

App.joinResult = function(game) { }

App.betResult = function(game, betP1, betP2) {

    // Reset visiblity 
    App.clearVisibleElements();

    if(betP1 !== 0){
        App.updateP1BetResult(betP1);
    }

    if(betP2 !== 0){
        App.updateP2BetResult(betP2);
    }

    if(betP1 !== 0 && betP2 !== 0){
        App.enableDeal();
        App.enableDeal2();
        App.updateAiBets(25, 25);
    }

}

App.socket = {}

App.registerClientActions = function () {
    
    $('#deal').click(function () {
        App.deal();
    });

    $('#hit').click(function () {
        App.hit();
    });

    $('#stand').click(function () {
        App.stand();
    });

    $('#deal2').click(function () {
        App.deal();
    });

    $('#hit2').click(function () {
        App.hit();
    });

    $('#stand2').click(function () {
        App.stand();
    });
    
    $('#bet1').click(function () {
        App.bet(1, $("#bet1box").val());
    });

    $('#bet2').click(function () {
        App.bet(2, $("#bet2box").val());
    });
}

App.registerServerActions = function () {    

    App.socket.on("join", function (game) {
        App.joinResult(game);
    });

    App.socket.on("end-game", function (game) {
        App.endGameUpdate(game);
    });

    App.socket.on("new-game", function (game) {
        App.newGameUpdate(game);
    });

    App.socket.on("end-turn", function ({game, curIndex, pIndex}) {
        App.updateTurnUI(game, curIndex, pIndex);
    });

    App.socket.on('stand', function ({game, curIndex, pIndex}) {
        App.standResult(game, curIndex, pIndex);
    });

    App.socket.on('deal', function ({game, curIndex}) {
        App.dealResult(game, curIndex);
    });

    App.socket.on('hit', function ({game, curIndex, p1Index}) {
        App.hitResult(game, curIndex, p1Index);
    });

    App.socket.on('bet', function ({game, betP1, betP2}) {
        App.betResult(game, betP1, betP2);
    });
    
}

App.init = function () {
    var socket = io.connect('http://localhost:3000');
    App.socket = socket;

    App.socket.emit('join');

    App.registerClientActions();
    App.registerServerActions();

    App.disableAllButtons();
    // App.enableDeal();
    // App.enableDeal2();
}

$(document).ready(function () {
    App.init();
});
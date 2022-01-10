
  1
  2
  3
  4
  5
  6
  7
  8
  9
 10
 11
 12
 13
 14
 15
 16
 17
 18
 19
 20
 21
 22
 23
 24
 25
 26
 27
 28
 29
 30
 31
 32
 33
 34
 35
 36
 37
 38
 39
 40
 41
 42
 43
 44
 45
 46
 47
 48
 49
 50
 51
 52
 53
 54
 55
 56
 57
 58
 59
 60
 61
 62
 63
 64
 65
 66
 67
 68
 69
 70
 71
 72
 73
 74
 75
 76
 77
 78
 79
 80
 81
 82
 83
 84
 85
 86
 87
 88
 89
 90
 91
 92
 93
 94
 95
 96
 97
 98
 99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
var cards = require('./cards');

// Blackjack game.
function BlackjackGame () {
    // Intialize Player Hands
    this.dealerHand = new BlackjackHand();
    this.aiPlayerHand = new BlackjackHand();
    // Turn Index
    this.firstPlayerIndex = 0;
    this.secondPlayerIndex = 0;
    // Results
    this.result = 'None';
    this.result2 = 'None';
    this.aiResult = 'None';
    // Deck
    this.cards = cards.createPlayingCards();
	this.AImoney = 1000;
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
    // Deal cards to Dealer
    this.dealerHand.addCard(this.cards.dealNextCard(), false);
    this.dealerHand.addCard(this.cards.dealNextCard(), true);
    // Results
    this.result = 'None';
    this.result2 = 'None';
    this.aiResult = 'None';
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
    // Results
    this.result = 'None';
    this.result2 = 'None';
    this.aiResult = 'None';
    // Players
    this.players.forEach(p => {
        p.playerHand = new BlackjackHand();
    });
}


// Check if the game is in progress
BlackjackGame.prototype.isInProgress = function () {
    return (this.result === 'None') && (this.dealerHand.hasCards()) && (this.aiResult === 'None') && (this.result2 === 'None');
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
        result: this.result,
        result2: this.result2,
        aiResult: this.aiResult,
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
	this.AImoney -= amount;
	this.prizePool += amount;
}
BlackjackGame.prototype.AiWinMoney = function (){
	this.AiMoney += this.prizePool;
	this.prizePool = 0;
}
BlackjackGame.prototype.bet = function (Player, amount){
	Player.money -= amount;
	this.prizePool += amount;
}

BlackjackGame.prototype.winMoney = function (Player){
	Player.money += this.prizePool;
	this.prizePool = 0;
}


// Check if the AI player has busted
BlackjackGame.prototype.getResultForAiPlayerBust = function () {
    var score = this.aiPlayerHand.getScore();
    if (score > 21) {
        return 'Bust';
    }
    return 'None';
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
            }
            else {
                this.result = "Win - 7 Card Charlie";
                this.result2 = "Lose";
                this.aiResult = "Lose";
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
                while(this.aiResult == 'None') {
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
BlackjackGame.prototype.hitAi = function () {
    if (this.isGameInProgress()) {
        var card = this.cards.dealNextCard();
        this.aiPlayerHand.addCard(card, true);
        this.aiResult = this.getResultForAiPlayerBust();
    }
}

// Get the AI players final result
BlackjackGame.prototype.getAiResult = function () {
    var dealerScore = this.dealerHand.getScore();
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
		this.AiWinMoney();
        return
    }

    var winPlayers = [];
    if(this.aiResult == "Win"){
        winPlayers.push(new Player("AI", this.aiPlayerHand));
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
            if(p.id == "AI"){
                this.aiResult = "Lose";
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
            if(p.id == "AI"){
                this.aiResult = "Lose";
            }
        }
    });
	eachAmount = this.prizePool/ winPlayers.length
	winPlayers.forEach(p => {
		if(p.id != "AI"){
			this.players[this.players.indexOf(p)].money += eachAmount;
		}else{
			this.AImoney += eachAmount;
		}
		
	})
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

// Play the AI's turn
// BlackjackGame.prototype.playAiTurn = function() {
//     if(this.aiResult=="None"){
//         // Get players visible hands
//         var aiScore = this.aiPlayerHand.getScore();
//         var visibleScores = [];
//         var visibleLengths = [];
//         this.players.forEach(element => {
//             visibleScores.push(element.playerHand.getVisibleScore())
//             visibleLengths.push(element.playerHand.getVisibleCards().length)
//         });

//         //Stay
//         if(aiScore==21){ this.aiResult = this.getAiResult(); }
//         //if a human player currently has a single visible card and this visible card is an ace or a card of value 10
//         else if(visibleLengths.includes('1') && 
//                     (visibleScores[visibleLengths.indexOf('1')] == 10 || visibleScores[visibleLengths.indexOf('1')] == 1)){
//             //Then hit
//             this.hitAi();
//         }
//         //else if the current value of the hand of the AI player is between 18 and 20
//         else if(aiScore >= 18 && aiScore <= 20){
//             //then if any other player has visible cards that add up to strictly more than the AI player’s hand’s value minus 10
//             var scoreLarger = false;
//             visibleScores.forEach(score => {
//                 if(score > (aiScore - 10) ){
//                     scoreLarger = true;
//                 }
//             });
//             //Then Hit
//             if(scoreLarger){ this.hitAi(); }
//             //Stay
//             else{ this.aiResult = this.getAiResult(); }
//         }
//         //Hit
//         else { this.hitAi(); }

//         // Check for 7 card charlie
//         if(this.aiPlayerHand.getCards().length == 7 && this.aiPlayerHand.getScore() <= 21){
//                 this.aiResult = "Win - 7 Card Charlie";
//                 this.result = "Lose";
//                 this.result2 = "Lose";
// 				this.AiWinMoney();
//         }
//     }
// }

BlackjackGame.prototype.playAiTurn = function(){
	if(this.aiResult == "None"){
		var aiScore = this.aiPlayerHand.getScore();
		var visibleScores = [];
		var visibleCards = [];
		if(aiScore <= 11){
			//always hit
			this.hitAi();
		}
		else if(aiScore >= 17){
			//always stand
			this.aiResult = this.getAiResult();
		}
		else {
			// 
			var descisionArr = [];
			visibleScores.forEach(element => {descisionArr.push(makeDescision(aiScore, element))})
			var choice = descisionArr.reduce(myfunc = (total, num) => {return total + num}, 0);
			if(choice < 2){
				// stand
				this.aiResult = this.getAiResult();
			}
			else{
				this.hitAi();
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
	else if(aiScore == 12 && (playerScore == 3 || playerScore == 4 ||playerScore == 6 )){
		return 0;
	}
	else if(aiScore == 12 && playerScore ==5){
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
            while(this.aiResult == 'None') {
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
main();

exports.newGame = newGame

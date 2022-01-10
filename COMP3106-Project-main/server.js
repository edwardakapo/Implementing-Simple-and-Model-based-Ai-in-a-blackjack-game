var http = require('http'),
    fs = require('fs'),
    url = require('url'),
    blackjack = require('./lib/blackjack');

var Server = {}
var Users = []
var player1, player2;

var Game = blackjack.newGame();

Server.getGame = function (socket, data, callback) {
    socket.get('game', function (err, game) {
        callback(socket, game);
    });
}

Server.deal = function (socket, data) {
    console.log('deal');
    player1 = Users.indexOf(socket.id);

    // Set AI bets
    Game.betAiNumber(25, 'Basic');
    Game.betAiNumber(25, 'Model');

    socket.emit('new-game', Game.toJson());
    socket.broadcast.emit('new-game', Game.toJson());
    
    if (!Game.isGameInProgress() || !Game.isInProgress()) {
        Game.newGame();
    }

    Game.setFirstPlayerIndex(player1);

    if(player1==1){
        player2=0;
    }else{
        player2=1;
    }

    Game.setSecondPlayerIndex(player2);

    socket.emit('deal', {game: Game.toJson(), curIndex: player1});
    socket.broadcast.emit('deal', {game: Game.toJson(), curIndex: player2});
}

Server.dealRigged = function (socket, data) {
    console.log('deal-rigged');
    Game.rigDeck(data);
}

Server.hit = function (socket, data) {
    console.log('hit');
    var hitReturn = Game.hit();
    socket.emit('hit', {game: Game.toJson(), curIndex: Users.indexOf(socket.id), p1Index: player1});
    // End Turn
    socket.emit('end-turn', {game: Game.toJson(), curIndex: Users.indexOf(socket.id), pIndex: player1});
    socket.broadcast.emit('end-turn', {game: Game.toJson(), curIndex: Users.indexOf(socket.id), pIndex: player2});
    //If game over emit calculatescores
    if(hitReturn == 'End') {
        socket.emit('end-game', Game.toJson());
        socket.broadcast.emit('end-game', Game.toJson());
        // Refresh hands
        Game.resetHands();
    }
}

Server.stand = function (socket, data) {
    console.log('stand');
    var standReturn = Game.stand();
    // socket.emit('stand', {game: Game.toJson(), firstPlayer: true});
    socket.emit('stand', {game: Game.toJson(), curIndex: Users.indexOf(socket.id), p1Index: player1});
    // End Turn
    socket.emit('end-turn', {game: Game.toJson(), curIndex: Users.indexOf(socket.id), pIndex: player1});
    socket.broadcast.emit('end-turn', {game: Game.toJson(), curIndex: Users.indexOf(socket.id), pIndex: player2});
    //If game over emit calculatescores
    if(standReturn == 'End') {
        socket.emit('end-game', Game.toJson());
        socket.broadcast.emit('end-game', Game.toJson());
        // Refresh hands
        Game.resetHands();
    }
}

Server.join = function (socket, data) {
    console.log('New player');
    Game.newPlayer(socket.id);
    Users.push(socket.id);
    socket.emit("join", Game.toJson());
}

Server.bet = function (socket, data) {
    console.log('New bet');
    Game.betPlayerNumber(data.pIndex, data.betTotal);
    socket.emit('bet', {game: Game.toJson(), betP1: Game.getPlayerNumberbet(1), betP2: Game.getPlayerNumberbet(2)});
    socket.broadcast.emit('bet', {game: Game.toJson(), betP1: Game.getPlayerNumberbet(1), betP2: Game.getPlayerNumberbet(2)});
}

Server.registerSocketIO = function (io) {
    io.sockets.on('connection', function (socket) {
        console.log('User connected');

        socket.on("join", (data) => {
            Server.join(socket, data);
        });
    
        socket.on("joined", () => {
            socket.emit("joined", Users);
        });

        socket.on('deal-rigged', function(data) {
            Server.dealRigged(socket, data);
        });

        socket.on('deal', function (data) {
            Server.deal(socket, data);
        });

        socket.on('hit', function (data) {
            Server.hit(socket, data);
        });

        socket.on('stand', function (data) {
            Server.stand(socket, data);
        });

        socket.on('disconnect', function () {
            Game.removePlayer(socket.id);
            console.log('User disconnected');
        });

        socket.on("close", function() {
            Game.removePlayer(socket.id);
            console.log('User disconnected');
        });
          
        socket.on("end", function() {
            Game.removePlayer(socket.id);
            console.log('User disconnected');
        });

        socket.on('bet', function (data) {
            Server.bet(socket, data);
        });
    });
}

Server.init = function () {
    var httpServer = http.createServer(function (req, res) {
        var path = url.parse(req.url).pathname;
        console.log(path);
        var contentType = 'text/html';
        if (path === '/') {
            path = '/index.html';
        } else if (path.indexOf('.css')) {
            contentType = 'text/css';
        } else if (path.indexOf('.svg')) {
            contentType = 'image/svg+xml';
        }
        fs.readFile(__dirname + path, function (error, data) {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(data, 'utf-8');
        });
    }).listen(3000);

    var io = require('socket.io').listen(httpServer);
    Server.registerSocketIO(io);
}

Server.init();



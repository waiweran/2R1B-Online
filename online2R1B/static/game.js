"use strict"

const socket = io();

const allCards = [
    {"name1": "Doctor", "name3": "Engineer", "class": "blueredteam", "num": 2, "id": 1},
    {"name1": "Blue Spy", "name3": "Red Spy", "class": "blueredteam", "num": 2, "id": 2},
    {"name1": "Coy Boy", "name3": "Coy Boy", "class": "blueredteam", "num": 2, "id": 3},
    {"name1": "Shy Guy", "name3": "Shy Guy", "class": "blueredteam", "num": 2, "id": 7},
    {"name1": "Thug", "name3": "Thug", "class": "blueredteam", "num": 2, "id": 8},
    {"name1": "Criminal", "name3": "Criminal", "class": "blueredteam", "num": 2, "id": 9},
    {"name1": "Dealer", "name3": "Dealer", "class": "blueredteam", "num": 2, "id": 10},
    {"name1": "Angel", "name3": "Angel", "class": "blueredteam", "num": 2, "id": 5},
    {"name1": "Demon", "name3": "Demon", "class": "blueredteam", "num": 2, "id": 6},
    {"name1": "Negotiator", "name3": "Negotiator", "class": "blueredteam", "num": 2, "id": 25},
    {"name1": "Paranoid", "name3": "Paranoid", "class": "blueredteam", "num": 2, "id": 26},
    {"name1": "Medic", "name3": "Medic", "class": "blueredteam", "num": 2, "id": 27},
    {"name1": "Psychologist", "name3": "Psychologist", "class": "blueredteam", "num": 2, "id": 28},
    {"name1": "Tuesday Knight", "name3": "Dr. Boom", "class": "blueredteam", "num": 2, "id": 39},
    {"name1": "Invincible", "name3": "Immunologist", "class": "blueredteam", "num": 2, "id": 42},
    {"name1": "Usurper", "name3": "Usurper", "class": "blueredteam", "num": 2, "id": 43},
    {"name1": "Agent", "name3": "Agent", "class": "blueredteam", "num": 2, "id": 44},
    {"name1": "Conman", "name3": "Conman", "class": "blueredteam", "num": 2, "id": 45},
    {"name1": "Eris", "name3": "Cupid", "class": "blueredteam", "num": 2, "id": 51},
    {"name1": "Enforcer", "name3": "Enforcer", "class": "blueredteam", "num": 2, "id": 52},
    {"name1": "Mayor", "name3": "Mayor", "class": "blueredteam", "num": 2, "id": 53},
    {"name1": "Security", "name3": "Security", "class": "blueredteam", "num": 2, "id": 54},
    {"name2": 'Gambler', "class": "grayteam", "num": 1, "id": 13},
    {"name2": 'MI6', "class": "grayteam", "num": 1, "id": 4},
    {"name2": 'Nuclear Tyrant', "class": "grayteam", "num": 1, "id": 31},
    {"name2": 'Hot Potato', "class": "grayteam", "num": 1, "id": 15},
    {"name2": 'Leprechaun', "class": "greenteam", "num": 1, "id": 12},
    {"name1": "Sniper", "name2": "Target", "name3": "Decoy", "class": "grayteam", "num": 3, "id": 16},
    {"name1": "Ahab", "name3": "Moby", "class": "grayteam", "num": 2, "id": 17},
    {"name1": "Butler", "name3": "Maid", "class": "grayteam", "num": 2, "id": 20},
    {"name1": "Romeo", "name3": "Juliet", "class": "grayteam", "num": 2, "id": 23},
    {"name1": "Wife", "name3": "Mistress", "class": "grayteam", "num": 2, "id": 24},
    {"name2": 'Bomb-Bot', "class": "grayteam", "num": 1, "id": 18},
    {"name2": 'Queen', "class": "grayteam", "num": 1, "id": 19},
    {"name2": 'Intern', "class": "grayteam", "num": 1, "id": 21},
    {"name2": 'Victim', "class": "grayteam", "num": 1, "id": 22},
    {"name2": 'Rival', "class": "grayteam", "num": 1, "id": 29},
    {"name2": 'Survivor', "class": "grayteam", "num": 1, "id": 30},
    {"name2": 'Agoraphobe', "class": "grayteam", "num": 1, "id": 40},
    {"name2": 'Traveler', "class": "grayteam", "num": 1, "id": 41},
    {"name2": 'Anarchist', "class": "grayteam", "num": 1, "id": 46},
    {"name2": 'Minion', "class": "grayteam", "num": 1, "id": 47},
    {"name2": 'Mastermind', "class": "grayteam", "num": 1, "id": 48},
    {"name2": 'Clone', "class": "grayteam", "num": 1, "id": 49},
    {"name2": 'Robot', "class": "grayteam", "num": 1, "id": 50},
    {"name1": "President's Daughter", "name3": "Martyr", "class": "blueredteam", "num": 2, "bury": true, "id": 32},
    {"name1": "Nurse", "name3": "Tinkerer", "class": "blueredteam", "num": 2, "bury": true, "id": 33},
    {"name2": "Private Eye", "class": "grayteam", "num": 1, "bury": true, "id": 34},
    {"name2": 'Drunk', "class": "unknownteam", "num": 0, "id": 11},
    {"name2": 'Zombie', "class": "greenteam", "num": 1, "id": 14},
    {"name1": "Blind", "name3": "Blind", "class": "blueredteam", "num": 2, "id": 35},
    {"name1": "Clown", "name3": "Clown", "class": "blueredteam", "num": 2, "id": 36},
    {"name1": "Mime", "name3": "Mime", "class": "blueredteam", "num": 2, "id": 37},
    {"name1": "Mummy", "name3": "Mummy", "class": "blueredteam", "num": 2, "id": 38},
    {"name1": "Blue Team", "name3": "Red Team", "class": "blueredteam", "num": 2, "id": 0},
];


function createGame() {

    var gameCardsBox = document.getElementById('gamecards');
    var allCardsBox = document.getElementById('allcards');
    var numRoles = 2;
    var buryRoles = 0;
    var expand = false;
    for(let card of allCards) {
        var cardElement = document.createElement('SPAN');
        cardElement.className = card.class;
        var name1 = document.createElement('LABEL');
        name1.className = "leftjust";
        var name2 = document.createElement('LABEL');
        var name3 = document.createElement('LABEL');
        name3.className = "rightjust";
        if(card.name1 != undefined) {
            name1.innerHTML = card.name1;            
        }
        if(card.name2 != undefined) {
            name2.innerHTML = card.name2;            
        }
        if(card.name3 != undefined) {
            name3.innerHTML = card.name3;            
        }
        cardElement.appendChild(name1);
        cardElement.appendChild(name2);
        cardElement.appendChild(name3);
        allCardsBox.appendChild(cardElement);
        cardElement.card = card;
    }

    var dragger = dragula([gameCardsBox, allCardsBox], {
        revertOnSpill: true, 
        accepts: function (el, target, source, sibling) {
            return sibling == null || !sibling.classList.contains("fixed");
        },
        invalid: function (el, handle) {
            return el.classList.contains("fixed");
        },

    });
    dragger.on("drop", function (el, target, source, sibling) {
        if(el.card != undefined) {
            if(source.id == 'allcards' && target.id == 'gamecards') {
                numRoles += el.card.num;
                if(el.card.bury) {
                    if(buryRoles == 0) {
                        numRoles--;
                    }
                    buryRoles++;
                }
            }
            else if(source.id == 'gamecards' && target.id == 'allcards') {
                numRoles -= el.card.num;
                if(el.card.bury) {
                    buryRoles--;
                    if(buryRoles == 0) {
                        numRoles++;
                    }
                }
            }
        }
        updateTitle()
        if(el.card != undefined && el.card.id == 0) {
            if(source.id == 'allcards' && target.id == 'gamecards') {
                var cardElement = document.createElement('SPAN');
                cardElement.className = 'blueredteam';
                var name1 = document.createElement('LABEL');
                name1.innerHTML = "Blue Team";
                name1.className = "leftjust";
                var name3 = document.createElement('LABEL');
                name3.className = "rightjust";
                name3.innerHTML = "Red Team";            
                cardElement.appendChild(name1);
                cardElement.appendChild(name3);
                allCardsBox.appendChild(cardElement);
                cardElement.card = el.card;
            }
            else if(source.id == 'gamecards' && target.id == 'allcards') {
                el.remove();
            }
        }
    });

    var expandBtn = document.getElementById('expandbtn');
    expandbtn.onclick = function(e) {
        if(expand) {
            expandBtn.style.backgroundColor = null;
            expand = false;
        }
        else {
            expandBtn.style.backgroundColor = "lightgreen";
            expand = true;
        }
        updateTitle();
    }

    document.getElementById('createbtn').onclick = function(e) {
        var selectedCards = [];
        var numPlayers = 2;
        var burying = false;
        for(let element of document.getElementById('gamecards').children) {
            if(element.card != undefined) {
                selectedCards.push(element.card.id);
                numPlayers += element.card.num;
                if(element.card.bury && !burying) {
                    burying = true;
                    numPlayers--;
                }
            }
        }
        if(numPlayers >= 6) {
            document.getElementById('rolesinput').value = JSON.stringify(selectedCards);
            document.getElementById('numplayersinput').value = numPlayers;
            document.getElementById('expandinput').value = expand;
            document.getElementById('gameform').submit()            
        }
    }

    function updateTitle() {
        if(expand) {
            document.getElementById('gametitle').innerHTML = "Game (" + numRoles + "+ Players)"
        }
        else {
            document.getElementById('gametitle').innerHTML = "Game (" + numRoles + " Players)"
        }
        if(numRoles >= 6) {
            document.getElementById('createbtn').disabled = false;
        }
        else {
            document.getElementById('createbtn').disabled = true;
        }
    }
}


function collectPlayers(code, roleIDs, playerTarget, expandable, hidePVal) {
    document.getElementById("gamebox").style.display = "none";
    document.getElementById("rejoinbox").style.display = "none";

    // Join on server
    socket.emit('player appear', {"code": code})
    var gameId = null;
    var playerId = null;
    var playerNum = null;

    // Setup player joining view
    var isReady = false;
    var nameBox = document.getElementById("name");
    var submitBtn = document.getElementById("submit");
    var readyBtn = document.getElementById("ready");
    readyBtn.style.display = "none";
    submitBtn.onclick = function(e) {
        socket.emit('player update', {"code": code, "id": gameId, "action": "join", "name": nameBox.value});
        submitBtn.innerHTML = 'Change';
        submitBtn.onclick = function(e) {
            socket.emit('player update', {"code": code, "id": gameId, "sender": playerId, "action": "rename", "name": nameBox.value});
        }
    }
    readyBtn.onclick = function ready(e) {
        if(isReady) {
            isReady = false;
            readyBtn.innerHTML = "Ready";
            socket.emit('player update', {"code": code, "id": gameId, "sender": playerId, "action": "ready", "status": -1})
        }
        else {
            isReady = true;
            readyBtn.innerHTML = "Not Ready";
            socket.emit('player update', {"code": code, "id": gameId, "sender": playerId, "action": "ready", "status": 1});
        }
    }

    // Setup game roles view
    var allCardsBox = document.getElementById('rolesbox');
    for(let roleNum of roleIDs) {
        for(let card of allCards) {
            if(card.id == roleNum) {
                var cardElement = document.createElement('SPAN');
                cardElement.className = card.class;
                var name1 = document.createElement('LABEL');
                name1.className = "leftjust";
                var name2 = document.createElement('LABEL');
                var name3 = document.createElement('LABEL');
                name3.className = "rightjust";
                if(card.name1 != undefined) {
                    name1.innerHTML = card.name1;            
                }
                if(card.name2 != undefined) {
                    name2.innerHTML = card.name2;            
                }
                if(card.name3 != undefined) {
                    name3.innerHTML = card.name3;            
                }
                cardElement.appendChild(name1);
                cardElement.appendChild(name2);
                cardElement.appendChild(name3);
                allCardsBox.appendChild(cardElement);
            }
        }
    }


    function updatePlayers(players) {
        var readyBox = document.getElementById('readybox');
        readyBox.innerHTML = "";
        var readyTitle = document.createElement('H2');
        readyBox.appendChild(readyTitle);
        if(expandable) {
            readyTitle.innerHTML = "Players (" + players.length + " of " + playerTarget + "+)";
        }
        else {
            readyTitle.innerHTML = "Players (" + players.length + " of " + playerTarget + ")";
        }
        for(let player of players) {
            var rdyLbl = document.createElement('LABEL');
            if(player.ready) {
                rdyLbl.innerHTML = player.name + " (ready)";
                rdyLbl.style.color = "green";
            }
            else {
                rdyLbl.innerHTML = player.name + " (waiting)";
                rdyLbl.style.color = "red";
            }
            rdyLbl.style.margin = "auto";
            readyBox.appendChild(rdyLbl);
            var rdybreak = document.createElement('BR');
            readyBox.appendChild(rdybreak);
        }
    }

    // Communication for joining the game
    socket.on('game info', function(msg) {
        gameId = msg.game_id;
        updatePlayers(msg.players);
    });

    socket.on('player update', function(msg) {
        if(msg.action == 'join') {
            playerId = msg.player_id;    
            readyBtn.style.display = "";        
        }
        else if(msg.action == 'updatelist') {
            updatePlayers(msg.players);
            for(let i = 0; i < msg.players.length; i++) {
                var player = msg.players[i];
                if(player.id == playerId) {
                    playerNum = i;
                    if(player.ready) {
                        isReady = true;
                        readyBtn.innerHTML = "Not Ready";
                    }
                    else {
                        isReady = false;
                        readyBtn.innerHTML = "Ready";
                    }
                    break;
                }
            }
            if(msg.start) {
                if(playerNum != null) {
                    document.getElementById('joinbox').style.display = "none";
                    socket.emit('game enter', {'id': gameId, 'sender': playerNum, 'code': code});
                }
                else {
                    window.location.replace("/");
                }            
            }
        }
    });

    socket.on('game enter', function(gameMsg) {
        document.getElementById('gamebox').style.display = "";
        initialize(gameMsg, playerNum, false, hidePVal);
    });

    socket.on('open another', function(msg) {
        document.getElementById("name").value = msg.name;
        submitBtn.onclick();
        setTimeout(function(e) {
             readyBtn.onclick();
             if(msg.done) {
                window.open(window.location.href);
             }
        }, 50)
    });
}


function rejoinGame(gameId) {
    document.getElementById('joinbox').style.display = "none";
    document.getElementById('gamebox').style.display = "none";
    document.getElementById('rejoinbox').style.display = "none";
    var playerCode = null;
    var hidePVal = true;
    const pCookie = getCookie("p");
    if(pCookie != null) {
        playerCode = parseInt(pCookie);
    }
    else {
        const urlParams = (new URL(window.location.href)).searchParams;
        if(urlParams.has("p")) {
            playerCode = parseInt(urlParams.get("p"));
            hidePVal = false;
        }
    }
    if(playerCode != null) {
        const playerNum = playerCode/(parseInt(gameId)*4643%3011) - 1;
        socket.on('game rejoin', function(gameMsg) {
            if(gameMsg.fail) {
                window.location.replace("/");
            }
            document.getElementById('gamebox').style.display = "";
            initialize(gameMsg, playerNum, true, hidePVal);
        });
        socket.emit('game reenter', {"id": gameId, "sender": playerNum})
    }
    else {
        socket.on('game names list', function(gameMsg) {
            document.getElementById('rejoinbox').style.display = "";
            const playerButtonArea = document.getElementById('rejoinnames');
            for(const [key, value] of Object.entries(gameMsg.names)) {
                var rejoinBtn = document.createElement('BUTTON');
                rejoinBtn.innerHTML = key;
                rejoinBtn.onclick = function(e) {
                    socket.on('game rejoin', function(gameMsg) {
                        if(gameMsg.fail) {
                            window.location.replace("/");
                        }
                        document.getElementById('rejoinbox').style.display = "none";
                        document.getElementById('gamebox').style.display = "";
                        initialize(gameMsg, value, true, hidePVal);
                    });
                    socket.emit('game reenter', {"id": gameId, "sender": value})
                };
                playerButtonArea.appendChild(rejoinBtn);
            }
        });
        socket.emit('game reenter', {"id": gameId, "sender": "unknown"})
    }
}


function initialize(game, myPlayerNum, rejoin, hidePVal) {
    
    // Set parameter for rejoining
    const url = new URL(window.location.href);
    const playerCode = (myPlayerNum+1)*(parseInt(game.id)*4643%3011);
    if(hidePVal) {
        setCookie("p", playerCode, 1);
    }
    else {
        url.searchParams.set('p', playerCode);
        window.history.replaceState(null, null, url);
    }

    // Set time offset
    var timeOffset = 0;
    socket.emit('time check', {"localTime": Date.now()})
    socket.on('time check', function(msg) {
        var localTime = (Date.now() + msg.localTime)/2;
        timeOffset = msg.serverTime - localTime;
    });

    // Hide overlays
    document.getElementById('bothrooms').style.display = "none";
    document.getElementById('hostages').style.display = "none";
    document.getElementById('decision').style.display = "none";
    document.getElementById('sharing').style.display = "none";
    document.getElementById('revealing').style.display = "none";
    document.getElementById('victory').style.display = "none";
    document.getElementById("sharepower").style.display = "none";

    // Setup my card
    var myCard = document.getElementById('mycard');
    myCard.src = game.myRole.source;
    var myPlayer = null;
    var conditions = game.myConditions;
    var partnerName = "";
    var powerAvailable = true;
    var numShares = 0;
    var publicRevealBtn = document.getElementById('publicreveal');
    var permanentPublicRevealBtn = document.getElementById('permanentpublicreveal');
    var usePowerBtn = document.getElementById('usepower');
    var hasPower = false;
    publicRevealBtn.onclick = function() {
        var revealPane = document.getElementById("revealing");
        var fadeBox = document.getElementById('fade');
        revealPane.style.display = "";
        fadeBox.style.display = "";
        document.getElementById("revealcolor").onclick = function(e) {
            gameUpdate({"action": "publicreveal", "type": "color"});
            revealPane.style.display = "none";
            fadeBox.style.display = "none";
        }
        document.getElementById("revealcard").onclick = function(e) {
            gameUpdate({"action": "publicreveal", "type": "card"});
            revealPane.style.display = "none";
            fadeBox.style.display = "none";
        }
        document.getElementById("revealcancel").onclick = function(e) {
            revealPane.style.display = "none";
            fadeBox.style.display = "none";
        }
    }
    permanentPublicRevealBtn.onclick = function() {
        gameUpdate({"action": "permanentpublicreveal"});
    }
    usePowerBtn.onclick = function() {
        gameUpdate({"action": "power"})
    }
    var cardButtons = document.getElementById('cardbuttons');
    cardButtons.onmouseover = function(e) {
        publicRevealBtn.style.display = "";
        permanentPublicRevealBtn.style.display = "";
        if(hasPower) {
            usePowerBtn.style.display = "";
        }
    }
    cardButtons.onmouseout = function(e) {
        publicRevealBtn.style.display = "none";
        permanentPublicRevealBtn.style.display = "none";
        usePowerBtn.style.display = "none";
    }
    publicRevealBtn.style.display = "none";
    permanentPublicRevealBtn.style.display = "none";
    usePowerBtn.style.display = "none";

    // General Setup
    var round = {"num": game.round, "time": game.time, "hostages": game.numHostages}
    var leader = null;
    var sentHostages = [];
    var currentlyShowing = false;
    var showQueue = [];
    var expandTarget = null;
    var expandElement = document.getElementById('expandelement');
    expandelement.style.display = "none";
    document.body.onkeydown = function(e) {
        if(e.charCode == " ") {
            e.preventDefault();
            if(expandTarget != null) {
                expandElement.src = expandTarget
                expandElement.style.display = "";
            }
        }
    }
    document.body.onkeyup = function(e) {
        if(e.charCode == " ") {
            e.preventDefault()
            expandElement.style.display = "none";            
        }
    }

    // Setup other players
    var players = [];
    for(let i = 0; i < game.numPlayers; i++) {
        let player = makePlayer(i);
        players.push(player);
        if(i == myPlayerNum) {
            myPlayer = player;
        }
    }

    // Setup current game variables for player info update if rejoining
    if(rejoin) {
        powerAvailable = game.power;
        partnerName = game.partner;
        myPlayer.role = game.players[myPlayerNum].role;
    }

    updatePlayerInfo();
    setupRound();

    // Setup current game state if rejoining
    if(rejoin) {
        for(let i = 0; i < game.numPlayers; i++) {
            let player = players[i];
            player.role = game.players[i].role;
            player.votes = game.players[i].votes;
            player.myVote = game.players[myPlayerNum].myVote == i;
            player.tackled = game.players[i].tackled;
            player.voters = [];
            for(let j = 0; j < game.players.length; j++) {
                if(game.players[j].myVote == i) {
                    player.voters.push(j);
                }
            }
            if(player.tackled) {
                player.tackleMarker.style.display = "";
            }
            if(game.players[i].share == 'card') {
                player.cardShareBtn.style.backgroundColor = "lightgreen";
            }
            else if(game.players[i].share == 'color') {
                player.colorShareBtn.style.backgroundColor = "lightgreen";
            }
        }
        numShares = game.myShareCount;
        if(game.myShare.card != null) {
            players[game.myShare.card].cardShareBtn.style.backgroundColor = "skyblue";
        }
        else if(game.myShare.color != null) {
            players[game.myShare.color].colorShareBtn.style.backgroundColor = "skyblue";
        }
        leader = game.leader
        sentHostages = game.sentHostages
        if(leader != null) {
            updateVoting();            
        }
        updateRoles();
        if(game.startTime != null) {
            startRound(game.startTime);            
        }
        if(game.currentAction != null) {
            updateFromEvent(game.currentAction);
        }
    }

    function makePlayer(i) {
        var player = {
            "name": game.players[i].name, 
            "num": i, 
            "room": game.players[i].room, 
            "tackled": false,
        };
        if(myPlayerNum == i) {
            player.name = player.name + " (me)";
        }
        player.element = document.createElement('DIV');

        // Tackle marker for security
        player.tackleMarker = document.createElement('I');
        player.tackleMarker.classList.add("fa");
        player.tackleMarker.classList.add("fa-lock");
        player.tackleMarker.title = "Tackled";
        player.tackleMarker.style.display = "none";
        player.element.appendChild(player.tackleMarker);

        // Player name
        var playerLabel = document.createElement('LABEL');
        playerLabel.innerHTML = player.name;
        player.element.appendChild(playerLabel);

        // Player card icon
        player.permanentRole = document.createElement('IMG');
        player.permanentRole.src = "/static/Cards/Back.png";
        player.permanentRole.onmouseover = function(e) {
            expandTarget = player.permanentRole.src;
        }
        player.permanentRole.onmouseout = function(e) {
            expandTarget = null;
        }
        player.element.appendChild(player.permanentRole)


        // Character-specific powers
        player.powerBtn = document.createElement('BUTTON');
        player.powerBtn.innerHTML = "Use Power";
        player.powerBtn.onclick = function(e) {
            gameUpdate({"action": "power", "target": i});
        };
        player.element.appendChild(player.powerBtn);
        player.powerBtn.disabled = true;
        player.powerBtn.style.display = "none"

        // Election button
        player.nominateBtn = document.createElement('BUTTON');
        player.votes = 0;
        player.nominateBtn.innerHTML = "Nominate Leader";
        player.nominateBtn.onclick = function(e) {
            gameUpdate({"action": "nominate", "target": i});
        };
        player.element.appendChild(player.nominateBtn);

        // Sharing and revealing buttons
        player.privateRevealBtn = document.createElement('BUTTON');
        player.privateRevealBtn.innerHTML = "Private Reveal";
        player.privateRevealBtn.onclick = function(e) {
            var revealPane = document.getElementById("revealing");
            var fadeBox = document.getElementById('fade');
            revealPane.style.display = "";
            fadeBox.style.display = "";
            document.getElementById("revealcolor").onclick = function(e) {
                gameUpdate({"action": "privatereveal", "target": i, "type": "color"});
                revealPane.style.display = "none";
                fadeBox.style.display = "none";
            }
            document.getElementById("revealcard").onclick = function(e) {
                gameUpdate({"action": "privatereveal", "target": i, "type": "card"});
                revealPane.style.display = "none";
                fadeBox.style.display = "none";
            }
            document.getElementById("revealcancel").onclick = function(e) {
                revealPane.style.display = "none";
                fadeBox.style.display = "none";
            }
        };
        player.element.appendChild(player.privateRevealBtn);
        player.colorShareBtn = document.createElement('BUTTON');
        player.colorShareBtn.innerHTML = "Color Share";
        player.colorShareBtn.onclick = function(e) {
            gameUpdate({"action": "share", "type": "color", "target": i});
        };
        player.element.appendChild(player.colorShareBtn);
        player.cardShareBtn = document.createElement('BUTTON');
        player.cardShareBtn.innerHTML = "Card Share";
        player.cardShareBtn.onclick = function(e) {
             gameUpdate({"action": "share", "type": "card", "target": i});
        };
        player.element.appendChild(player.cardShareBtn);
        player.element.appendChild(document.createElement('BR'));
        if(myPlayerNum == i) {
            player.nominateBtn.disabled = true;
        }
        return player;
    }

    function updateRoles() {
        for(let player of players) {
            if(player.role != undefined && !conditions.includes('blind')) {
                player.permanentRole.src = player.role;                
            }
        }
    }

    function updatePlayerInfo() {
        // Update button accessibility
        publicRevealBtn.disabled = myPlayer.role != undefined;
        permanentPublicRevealBtn.disabled = myPlayer.role != undefined;
        usePowerBtn.disabled = !powerAvailable;
        permanentPublicRevealBtn.innerHTML = "Permanent Reveal";
        hasPower = false;
        if(round.num > 1 && (game.myRole.id == 'blueusurper' || game.myRole.id == 'redusurper')) {
            permanentPublicRevealBtn.innerHTML = "Permanent Reveal & Usurp"
        }
        else if(game.myRole.id == 'bluesecurity' || game.myRole.id == 'redsecurity') {
            permanentPublicRevealBtn.innerHTML = "Permanent Reveal & Tackle"
        }
        else if(game.myRole.id == 'blueenforcer' || game.myRole.id == 'redenforcer') {
            hasPower = true;
            usePowerBtn.innerHTML = "Use Enforcer Power";
        }
        else if(game.myRole.id == 'cupid') {
            hasPower = true;
            usePowerBtn.innerHTML = "Use Cupid Power";
        }
        else if(game.myRole.id == 'eris') {
            hasPower = true;
            usePowerBtn.innerHTML = "Use Eris Power";
        }
        else if(game.myRole.id == 'bluemayor' || game.myRole.id == 'redmayor') {
            hasPower = true;
            usePowerBtn.innerHTML = "Reveal & Current Votes +1";
        }
        if(conditions.includes("coy" || conditions.includes("shy") ||
                conditions.includes("savvy") || conditions.includes("paranoid"))) {
            publicRevealBtn.disabled = true;
            permanentPublicRevealBtn.disabled = true;
            usePowerBtn.disabled = true;
        }

        for(let player of players) {
            player.powerBtn.style.display = "none";
            player.colorShareBtn.disabled = false;
            player.cardShareBtn.disabled = false;
            player.privateRevealBtn.disabled = false;
            if(conditions.includes("coy")) {
                player.cardShareBtn.disabled = true;
                player.privateRevealBtn.disabled = true;
            }
            if(conditions.includes("shy")) {
                player.cardShareBtn.disabled = true;
                player.colorShareBtn.disabled = true;
                player.privateRevealBtn.disabled = true;
            }
            if(conditions.includes("savvy") || conditions.includes("paranoid")) {
                player.colorShareBtn.disabled = true;
                player.privateRevealBtn.disabled = true;
            }
            if(conditions.includes("paranoid") && numShares >= 1) {
                player.cardShareBtn.disabled = true;
            }
            if(game.myRole.id == 'blueagent' || game.myRole.id == 'redagent') {
                player.powerBtn.innerHTML = "Agent Power";
                player.powerBtn.style.display = "";
                player.powerBtn.disabled = !powerAvailable;
            }
            else if(game.myRole.id == 'bluebouncer' || game.myRole.id == 'redbouncer') {
                player.powerBtn.innerHTML = "Bouncer Power";
                player.powerBtn.style.display = "";
                player.powerBtn.disabled = !powerAvailable;
            }
            if(myPlayerNum == player.num) {
                player.powerBtn.disabled = true;
                player.cardShareBtn.disabled = true;
                player.colorShareBtn.disabled = true;
                player.privateRevealBtn.disabled = true;
            }
        }

        // Update Conditions
        if(conditions.includes("zombie")) {
            document.getElementById('myzombie').style.display = "";
        }
        else {
            document.getElementById('myzombie').style.display = "none";
        }
        var condstr = ""
        if(conditions.length == 0) {
            condstr = "No Conditions"
        }
        else {
            condstr = "Conditions: ";
        }
        for(let i = 0; i < conditions.length; i++) {
            if(conditions[i] == 'coy') {
                condstr = condstr + 'Coy';
            }
            else if(conditions[i] == 'shy') {
                condstr = condstr + 'Shy';
            }
            else if(conditions[i] == 'foolish') {
                condstr = condstr + 'Foolish';
            }
            else if(conditions[i] == 'ill') {
                condstr = condstr + 'Ill';
            }
            else if(conditions[i] == 'broken') {
                condstr = condstr + 'Broken';
            }
            else if(conditions[i] == 'nursed') {
                condstr = condstr + 'Nursed';
            }
            else if(conditions[i] == 'tinkered') {
                condstr = condstr + 'Tinkered';
            }
            else if(conditions[i] == 'dead') {
                condstr = condstr + 'Dead';
            }
            else if(conditions[i] == 'fizzled') {
                condstr = condstr + 'Fizzled';
            }
            else if(conditions[i] == 'zombie') {
                condstr = condstr + 'Zombie';
            }
            else if(conditions[i] == 'honest') {
                condstr = condstr + 'Honest';
            }
            else if(conditions[i] == 'liar') {
                condstr = condstr + 'Liar';
            }
            else if(conditions[i] == 'savvy') {
                condstr = condstr + 'Savvy';
            }
            else if(conditions[i] == 'blind') {
                condstr = condstr + 'Blind';
            }
            else if(conditions[i] == 'cursed') {
                condstr = condstr + 'Cursed (Make No Noise)';
            }

            else if(conditions[i] == 'immune') {
                condstr = condstr + 'Immune';
            }

            else if(conditions[i] == 'paranoid') {
                condstr = condstr + 'Paranoid';
            }

            else if(conditions[i] == 'in love') {
                condstr = condstr + 'In love with ' + partnerName;
            }

            else if(conditions[i] == 'in hate') {
                condstr = condstr + 'In hate with ' + partnerName;
            }

            if(i < conditions.length - 1) {
                condstr = condstr + ", ";
            }
        }
        document.getElementById('myconditions').innerHTML = condstr;
    }

    function setupRound() {

        // Clean the display
        document.getElementById('hostages').style.display = "none";

        // Clear the rooms
        var room1 = document.getElementById('room1');
        var room2 = document.getElementById('room2');
        var myRoom = document.getElementById('myroom');
        var myHostages = document.getElementById('hostageroom');
        room1.innerHTML = '<h2>Room 1</h2>';
        room2.innerHTML = '<h2>Room 2</h2>';
        myRoom.innerHTML = '';
        myHostages.innerHTML = '';
        sentHostages = [];

        // Put players in the rooms
        for(let player of players) {
            var nameLbl = document.createElement('LABEL');
            nameLbl.innerHTML = player.name;
            if(player.room == 0) {
                room1.appendChild(nameLbl);
                room1.appendChild(document.createElement("BR"));
            }
            else {
                room2.appendChild(nameLbl);
                room2.appendChild(document.createElement("BR"));
            }
            if(player.room == myPlayer.room) {
                myRoom.appendChild(player.element);
            }
        }

        // Setup starting
        var startRoundBtn = document.getElementById('startround');
        startRoundBtn.disabled = true;
        setTimeout(function() {
            startRoundBtn.disabled = false;
        }, 15000)
        startRoundBtn.onclick = function() {
            gameUpdate({"action": "startround", "startTime": Date.now() + timeOffset});
        };

        // Set the timer
        var timer = document.getElementById("timer");
        timer.innerHTML = "Round " + round.num + "<br>" + round.time + ":00"

        // Show the room listing overlay
        document.getElementById('bothrooms').style.display = "";
        document.getElementById('fade').style.display = "";
    }

    function startRound(startTime) {

        // Hide the room listing overlay
        document.getElementById('bothrooms').style.display = "none";
        document.getElementById('fade').style.display = "none";

        // Start the round timer
        var roundEndTime = startTime + 60000*round.time;
        var roundTimer = setInterval(function runTimer() {
            var timeLeft = roundEndTime - (Date.now() + timeOffset);
            timer.innerHTML = "Round " + round.num + "<br>" + Math.floor(timeLeft/60000)
                     + ":" + Math.floor(timeLeft/10000)%6 + "" + Math.floor(timeLeft/1000)%10;
            if(Date.now() + timeOffset > roundEndTime) {
                clearInterval(roundTimer);
                timer.innerHTML = "Round " + round.num + "<br>0:00";
                document.getElementById('sharing').style.display = "none";
                document.getElementById('revealing').style.display = "none";
                document.getElementById('fade').style.display = "";
                setupHostages(round.hostages);
                document.getElementById('hostages').style.display = "";
            }
        }, 100);
    }

    function setupHostages(numHostages) {

        // Setup hostage page
        var myHostages = document.getElementById('hostageroom');
        myHostages.innerHTML = '';
        var sendHostageBtn = document.getElementById('sendhostages');
        sendHostageBtn.disabled = true;
        var hostages = [];
        var hostageNum = 0;
        sendHostageBtn.onclick = function(e) {
            quickUpdate({"action": "hostageupdate", "completed": true})
            gameUpdate({"action": "sendhostages", "hostages": hostages});
            document.getElementById('hostagesubtitle').innerHTML = "Wait for Other Room";
            sendHostageBtn.style.display = "none";
            for(let player of players) {
                if(player.hostageBtn != undefined) {
                    player.hostageBtn.disabled = true;
                    player.hostageBtn.innerHTML = "X";
                }
            }

        }
        if(leader == null) {
            for(let player of players) {
                if(player.room == myPlayer.room) {
                    leader = player.num;
                    break;
                }
            }
        }
        if(myPlayerNum == leader) {
            document.getElementById('hostagetitle').innerHTML = "Hostages";
            if(numHostages == 1) {
                document.getElementById('hostagesubtitle').innerHTML = "Select 1 Hostage to Send";                
            }
            else {
                document.getElementById('hostagesubtitle').innerHTML = "Select " + numHostages + " Hostages to Send";
            }
            sendHostageBtn.style.display = "";
        }
        else {
            document.getElementById('hostagetitle').innerHTML = "Hostages";
            document.getElementById('hostagesubtitle').innerHTML = "Wait for Leader " + players[leader].name;
            sendHostageBtn.style.display = "none";
        }

        // Put players in the rooms
        for(let player of players) {
            hostages.push(false);
            if(player.room == myPlayer.room && player.num != leader) {
                myHostages.append(makeHostage(player));
            }
        }
        if(sentHostages.includes(myPlayer.room)) {
            document.getElementById('hostagesubtitle').innerHTML = "Wait for Other Room";
            sendHostageBtn.style.display = "none";
            for(let player of players) {
                if(player.hostageBtn != undefined) {
                    player.hostageBtn.disabled = true;
                    player.hostageBtn.innerHTML = "X";
                }
            }
        }

        function makeHostage(player) {
            var hostageItem = document.createElement('DIV');
            player.hostageBtn = document.createElement('BUTTON');
            if(player.tackled) {
                player.hostageBtn.disabled = true;
                player.hostageBtn.innerHTML = "Tackled";
            }
            else if(leader == myPlayerNum) {
                player.hostageBtn.innerHTML = "Select";
                player.hostageBtn.onclick = function(e) {
                    hostages[player.num] = !hostages[player.num];
                    if(hostages[player.num]) {
                        quickUpdate({"action": "hostageupdate", "target": player.num, "completed": false, "selected": true});
                        player.hostageBtn.style.backgroundColor = "lightgreen";
                        hostageNum++;
                    }
                    else {
                        quickUpdate({"action": "hostageupdate", "target": player.num, "completed": false, "selected": false});
                        player.hostageBtn.style.backgroundColor = null;
                        hostageNum--;
                    }
                    if(hostageNum == numHostages) {
                        sendHostageBtn.disabled = false;
                    }
                    else {
                        sendHostageBtn.disabled = true;
                    }
                };
            }
            else {
                player.hostageBtn.disabled = true;
                player.hostageBtn.innerHTML = "X";
            }
            hostageItem.appendChild(player.hostageBtn);
            var hostageName = document.createElement('LABEL');
            hostageName.innerHTML = player.name;
            hostageItem.appendChild(hostageName);
            return hostageItem;
        }
    }

    function teamShow(player, team, title, zombie) {
        if(currentlyShowing) {
            showQueue.push({"player": player, "team": team, "title": title, "zombie": zombie})
        }
        else {
            currentlyShowing = true
            var sharePowerBtn = document.getElementById("sharepower");
            sharePowerBtn.style.display = "none";
            sharePowerBtn.onclick = function(e){};
            document.getElementById("sharetitle").innerHTML = title;
            document.getElementById("sharename").innerHTML = player.name;
            var shareCard = document.getElementById("sharecard");
            var zombieOverlay = document.getElementById("zombieoverlay");
            if(zombie) {
                zombieOverlay.src = "/static/Teams/ZombieOverlay.png";
            }
            else {
                zombieOverlay.src = "";
            }
            if(conditions.includes('blind')) {
                shareCard.src = "";
            }
            else {
                shareCard.src = team;
            }
            shareCard.style.height = "14%";
            zombieOverlay.style.height = "14%";
            document.getElementById("cardpictures").style.height = "14%";
            var shareBox = document.getElementById("sharing");
            var fadeBox = document.getElementById('fade');
            if(game.myRole.id == 'blueconman' || game.myRole.id == 'redconman') {
                sharePowerBtn.style.display = "";
                sharePowerBtn.onclick = function(e) {
                    gameUpdate({"action": "power", "target": player.num});
                }
                shareBox.style.display = "none";
                fadeBox.style.display = "none";
                currentlyShowing = false;
                if(showQueue.length > 0) {
                    var info = showQueue.shift()
                    if(info.team != undefined) {
                        teamShow(info.player, info.team, info.title ,info.zombie);
                    }
                    else {
                        cardShow(info.player, info.source, info.title, info.zombie);
                    }
                }
            }
            document.getElementById("shareclose").onclick = function(e) {
                shareBox.style.display = "none";
                fadeBox.style.display = "none";
                currentlyShowing = false;
                if(showQueue.length > 0) {
                    var info = showQueue.shift()
                    if(info.team != undefined) {
                        teamShow(info.player, info.team, info.title ,info.zombie);
                    }
                    else {
                        cardShow(info.player, info.source, info.title, info.zombie);
                    }
                }
            }
            shareBox.style.display = "";
            fadeBox.style.display = "";
        }
    }

    function cardShow(player, source, title, zombie) {
        if(currentlyShowing) {
            showQueue.push({"player": player, "source": source, "title": title, "zombie": zombie})
        }
        else {
            currentlyShowing = true
            var sharePowerBtn = document.getElementById("sharepower");
            sharePowerBtn.style.display = "none";
            sharePowerBtn.onclick = function(e){};
            document.getElementById("sharetitle").innerHTML = title;
            document.getElementById("sharename").innerHTML = player.name;
            var shareCard = document.getElementById("sharecard");
            var zombieOverlay = document.getElementById("zombieoverlay");
            if(zombie) {
                zombieOverlay.src = "/static/Cards/ZombieOverlay.png";
            }
            else {
                zombieOverlay.src = "";
            }
            if(conditions.includes('blind')) {
                shareCard.src = "";
            }
            else {
                shareCard.src = source;
            }
            shareCard.style.height = "60%";
            zombieOverlay.style.height = "60%";
            document.getElementById("cardpictures").style.height = "60%";
            var shareBox = document.getElementById("sharing");
            var fadeBox = document.getElementById('fade');
            document.getElementById("shareclose").onclick = function(e) {
                shareBox.style.display = "none";
                fadeBox.style.display = "none";
                currentlyShowing = false;
                if(showQueue.length > 0) {
                    var info = showQueue.shift()
                    if(info.team != undefined) {
                        teamShow(info.player, info.team, info.title, info.zombie);
                    }
                    else {
                        cardShow(info.player, info.source, info.title, info.zombie);
                    }
                }
            }
            shareBox.style.display = "";
            fadeBox.style.display = "";
        }
    }

    function updateVoting() {
        if(myPlayerNum == leader) {
            for(let player of players) {
                var tooltip = "Voters:";
                for(let i = 0; i < player.voters.length; i++) {
                    tooltip = tooltip + "\n" + players[i].name;
                }
                if(player.num == leader) {
                    player.nominateBtn.innerHTML = "Current Leader";
                    player.nominateBtn.title = "";
                    player.nominateBtn.disabled = true;
                }
                else if(player.votes > 0) {
                    player.nominateBtn.innerHTML = "Pass Leader (" + player.votes + ")";
                    player.nominateBtn.title = tooltip;
                    player.nominateBtn.disabled = false;
                }
                else {
                    player.nominateBtn.innerHTML = "Pass Leadership";
                    player.nominateBtn.title = "";
                    player.nominateBtn.disabled = false;                    
                }
            }
        }
        else {
            for(let player of players) {
                var tooltip = "Voters:";
                for(let i = 0; i < player.voters.length; i++) {
                tooltip = tooltip + "\n" + players[i].name;
                }
                if(player.num == leader) {
                    player.nominateBtn.innerHTML = "Current Leader";
                    player.nominateBtn.title = "";
                    player.nominateBtn.disabled = true;
                }
                else if(player.votes > 0) {
                    if(player.myVote) {
                        player.nominateBtn.innerHTML = "Undo vote (" + player.votes + ")";
                    }
                    else {
                        player.nominateBtn.innerHTML = "Vote for (" + player.votes + ")";                            
                    }
                    player.nominateBtn.title = tooltip;
                    player.nominateBtn.disabled = false;
                }
                else {
                    player.nominateBtn.innerHTML = "Nominate Leader";
                    player.nominateBtn.title = "";
                    player.nominateBtn.disabled = false;
                }
            }
        }
    }

    function displayDecision(name, descrip, tag, options, chooser, multiple, optional) {
        document.getElementById('decision').style.display = "";
        document.getElementById('hostages').style.display = "none";
        document.getElementById('bothrooms').style.display = "none";
        var decisionPane = document.getElementById('decisionoptions');
        decisionPane.innerHTML = "";
        var choices = [];
        var choiceNum = 0;
        for(let option of options) {
            choices.push(false);
        }
        var doneBtn = document.createElement('BUTTON');
        if(chooser == myPlayerNum) {
            document.getElementById('decisiontitle').innerHTML = name;
            document.getElementById('decisionsubtitle').innerHTML = descrip;
            for(let i = 0; i < options.length; i++) {
                decisionPane.appendChild(makeOption(options[i], i));
                decisionPane.appendChild(document.createElement('BR'));
            }
            if(multiple) {
                decisionPane.appendChild(document.createElement('BR'));
                doneBtn.innerHTML = "Done";
                doneBtn.disabled = true;
                doneBtn.onclick = function(e) {
                    var chosen = [];
                    for(let i = 0; i < choices.length; i++) {
                        if(choices[i]) {
                            chosen.push(i);
                        }
                    }
                    gameUpdate({'action': 'decision', 'type': tag, 'choice': chosen}, true);
                };
                decisionPane.appendChild(doneBtn);
            }
            if(optional) {
                var cancelBtn = document.createElement('BUTTON');
                cancelBtn.innerHTML = "Cancel";
                cancelBtn.onclick = function(e) {
                    document.getElementById('decision').style.display = "none";
                };
                decisionPane.appendChild(document.createElement('BR'));
                decisionPane.appendChild(cancelBtn);
            }
        }
        else {
            document.getElementById('decisiontitle').innerHTML = name;
            document.getElementById('decisionsubtitle').innerHTML = "Wait for " + players[chooser].name;
        }

        function makeOption(option, num) {
            var optionBtn = document.createElement('BUTTON');
            optionBtn.innerHTML = option;
            if(multiple) {
                optionBtn.onclick = function(e) {
                    choices[num] = !choices[num];
                    if(choices[num]) {
                        optionBtn.style.backgroundColor = "lightgreen";
                        choiceNum++;
                    }
                    else {
                        optionBtn.style.backgroundColor = null;
                        choiceNum--;
                    }
                    if(choiceNum == 2) {
                        doneBtn.disabled = false;
                    }
                    else {
                        doneBtn.disabled = true;
                    }

                };
            }
            else {
                optionBtn.onclick = function(e) {
                    gameUpdate({'action': 'decision', 'type': tag, 'choice': num}, true);
                };
            }
            return optionBtn;
        }
    }

    function endGame(info) {
        document.getElementById("fade").style.display = "";
        document.getElementById("victory").style.display = "";
        var title = document.getElementById('victorytitle');
        var room1 = document.getElementById('victoryroom1');
        var room2 = document.getElementById('victoryroom2');
        room1.innerHTML = '<h2>Room 1</h2>';
        room2.innerHTML = '<h2>Room 2</h2>';

        // Show all players by room
        for(let player of players) {
            var playerBox = document.createElement('DIV');
            var playerName = document.createElement('LABEL');
            var playerCard = document.createElement('IMG');
            if(info[player.num].won) {
                playerName.innerHTML = player.name + ': W';
            }
            else {
                playerName.innerHTML = player.name + ': L';
            }
            playerCard.src = info[player.num].role;
            playerCard.style.height = "20%";

            playerBox.appendChild(playerName);
            playerBox.appendChild(document.createElement('BR'));
            playerBox.appendChild(playerCard);
            if(player.room == 0) {
                room1.appendChild(playerBox);
            }
            else {
                room2.appendChild(playerBox);
            }
        }

        // Show my win condition
        if(info[myPlayerNum].won) {
            title.innerHTML = "You Win!";
        }
        else {
            title.innerHTML = "You Lose";
        }
    }

    function quickUpdate(item) {
        item.id = game.id;
        item.room = myPlayer.room
        item.sender = myPlayerNum;
        socket.emit('quick event', item);
    }

    function gameUpdate(item) {
        item.id = game.id;
        item.sender = myPlayerNum;
        socket.emit('game event', item);
    }

    socket.on('quick event', function(msg) {
        if(msg.action == 'hostageupdate') {
            if(leader != myPlayerNum) {
                if(msg.completed) {
                    document.getElementById('hostagesubtitle').innerHTML = "Wait for Other Room";
                }
                else {
                    if(msg.selected) {
                        players[msg.target].hostageBtn.style.backgroundColor = "lightgreen";                
                    }
                    else {
                        players[msg.target].hostageBtn.style.backgroundColor = null;                
                    }
                }
            }
        }
        else if(msg.action == 'decision') {
            document.getElementById('decision').style.display = "none";
        }
    });
    socket.on('event list', function(msg) {
        for(let event of msg) {
            updateFromEvent(event);
        }
    });
    socket.on('event response', function(msg) {
        updateFromEvent(msg);
    });

    function updateFromEvent(msg) {
        if(msg.action == 'startround') {
            startRound(msg.startTime);
        }
        else if(msg.action == 'shareupdate') {
            for(let player of players) {
                if(msg.colorout == player.num) {
                    player.colorShareBtn.style.backgroundColor = "skyblue";
                }
                else {
                    player.colorShareBtn.style.backgroundColor = null;                    
                }
                if(msg.cardout == player.num) {
                    player.cardShareBtn.style.backgroundColor = "skyblue";
                }
                else {
                    player.cardShareBtn.style.backgroundColor = null;                    
                }
            }
            for(let share of msg.incoming) {
                if(share.type == 'color')
                    players[share.sender].colorShareBtn.style.backgroundColor = "lightgreen";
                else {
                    players[share.sender].cardShareBtn.style.backgroundColor = "lightgreen";                    
                }
            }
        }
        else if(msg.action == 'privatereveal') {
            if(msg.type == 'card') {
                if(msg.alert != null) {
                    cardShow(players[msg.target], msg.role, msg.alert, false);
                }
                else {
                    cardShow(players[msg.target], msg.role, 'Private Reveal', false);
                }
            }
            else {
                teamShow(players[msg.target], msg.team, 'Private Reveal', false);
            }
        }
        else if(msg.action == 'publicreveal') {
            if(msg.type == 'card') {
                if(msg.alert != null) {
                    cardShow(players[msg.target], msg.role, msg.alert, false);
                }
                else {
                    cardShow(players[msg.target], msg.role, 'Public Reveal', false);
                }
            }
            else {
                teamShow(players[msg.target], msg.team, 'Public Reveal', false);
            }
        }
        else if(msg.action == 'permanentpublicreveal') {
            players[msg.target].role = msg.role;
            if(msg.alert != null) {
                cardShow(players[msg.target], msg.role, msg.alert, false);
            }
            else {
                cardShow(players[msg.target], msg.role, 'Permanent Reveal', false);
            }
            updateRoles();
            if(msg.target == myPlayerNum) {
                updatePlayerInfo();
            }
        }
        else if(msg.action == 'hiderole') {
            players[msg.target].role = "/static/Cards/Back.png";
            updateRoles();
            players[msg.target].role = null;
        }
        else if(msg.action == 'colorshare') {
            teamShow(players[msg.target], msg.team, 'Color Share', msg.zombie);
        }
        else if(msg.action == 'cardshare') {
            if(msg.alert != null) {
                cardShow(players[msg.target], msg.role, msg.alert, msg.zombie);
            }
            else {
                cardShow(players[msg.target], msg.role, 'Card Share', msg.zombie);
            }
        }
        else if(msg.action == 'leaderupdate') {
            leader = msg.leader;
            for(let i = 0; i < players.length; i++) {
                var player = players[i];
                player.votes = msg.votes[i];
                player.myVote = msg.myVotes[myPlayerNum] == i;
                player.voters = [];
                for(let j = 0; j < players.length; j++) {
                    if(msg.myVotes[j] == i) {
                        player.voters.push(j);
                    }
                }
            }
            updateVoting();
        }
        else if(msg.action == 'updateplayer') {
            myCard.src = msg.role.source;
            game.myRole = msg.role;
            conditions = msg.conditions;
            powerAvailable = msg.power;
            numShares = msg.shares;
            if(msg.partner != null)
                partnerName = players[msg.partner].name;
            updatePlayerInfo();
        }
        else if(msg.action == 'updateotherplayer') {
            players[msg.target].tackled = msg.tackled;
            players[msg.target].tackleMarker.style.display = "";
        }
        else if(msg.action == 'setupround') {
            for(let i = 0; i < game.numPlayers; i++) {
                players[i].room = msg.rooms[i];
                if(msg.roles[i] != null) {
                    players[i].role = msg.roles[i];
                }
                players[i].votes = 0;
                players[i].myVote = false;
                players[i].voters = [];
                players[i].tackled = false;
                players[i].tackleMarker.style.display = "none";
            }
            round.num = msg.round;
            round.time = msg.time;
            round.hostages = msg.numHostages;
            leader = msg.leaders[myPlayer.room];
            updateVoting();
            updateRoles();
            setupRound();
        }
        else if(msg.action == 'power') {
            if(msg.type == 'security') {
                displayDecision(msg.name, msg.description, msg.type, msg.options, msg.target, false, true);
            }
            else {
                displayDecision(msg.name, msg.description, msg.type, msg.options, msg.target, true, true);
            }
        }
        else if(msg.action == 'pause') {
            if(msg.type == 'private eye') {
                displayDecision('Private Eye', 'Choose the buried card', msg.type, msg.options, msg.target, false, false);
            }
            else if(msg.type == 'gambler') {
                displayDecision('Gambler', 'Choose the winning team', msg.type, msg.options, msg.target, false, false);
            }
            else if(msg.type == 'sniper') {
                displayDecision('Sniper', 'Choose the Target', msg.type, msg.options, msg.target, false, false);
            }
            else {
                gameUpdate({'action': 'continue'});
            }
        }
        else if(msg.action == 'endgame') {
            for(let i = 0; i < game.numPlayers; i++) {
                players[i].room = msg.info[i].room;
            }
            endGame(msg.info);
        }
    }
}


function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return null;
}

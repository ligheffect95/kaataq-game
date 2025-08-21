# Create the basic file structure for the GitHub repository
import os

# Create directory structure
structure = {
    'index.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kaataq - Traditional Alutiiq Game</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app">
        <!-- Welcome Screen -->
        <div id="welcome" class="screen active">
            <header class="game-header">
                <h1>Kaataq</h1>
                <p class="subtitle">Traditional Alutiiq Stick Game</p>
            </header>
            
            <div class="cultural-info">
                <button id="info-btn" class="info-toggle">About Kaataq</button>
                <div id="info-panel" class="info-panel hidden">
                    <h3>Cultural Context</h3>
                    <p>Kaataq is a traditional Alutiiq guessing game played with two sticks - one marked (wee) and one unmarked (dip). Traditionally played by men before Lent, it involves bluffing, psychology, and social interaction.</p>
                </div>
            </div>

            <div class="actions">
                <button id="create-btn" class="btn btn-primary">Create Room</button>
                <button id="join-btn" class="btn btn-secondary">Join Room</button>
            </div>
        </div>

        <!-- Join Room Screen -->
        <div id="join-screen" class="screen">
            <h2>Join Game</h2>
            <div class="form-group">
                <label>Room Code:</label>
                <input type="text" id="room-code-input" placeholder="Enter 4-digit code" maxlength="4">
            </div>
            <div class="form-group">
                <label>Your Name:</label>
                <input type="text" id="player-name-input" placeholder="Enter your name" maxlength="20">
            </div>
            <div class="actions">
                <button id="join-game-btn" class="btn btn-primary">Join Game</button>
                <button id="back-btn" class="btn btn-secondary">Back</button>
            </div>
        </div>

        <!-- Lobby Screen -->
        <div id="lobby" class="screen">
            <div class="room-info">
                <h2>Room: <span id="room-code-display"></span></h2>
                <p>Share this code with others to join</p>
            </div>
            
            <div class="players-section">
                <h3>Players (<span id="player-count">0</span>)</h3>
                <div id="players-list" class="players-list"></div>
            </div>
            
            <div class="actions" id="lobby-actions">
                <button id="start-game-btn" class="btn btn-primary" disabled>Start Game</button>
                <button id="leave-btn" class="btn btn-secondary">Leave Room</button>
            </div>
        </div>

        <!-- Game Screen -->
        <div id="game-screen" class="screen">
            <div class="game-status">
                <div class="round-info">
                    <span>Round <span id="current-round">1</span></span>
                    <span id="phase-indicator">Waiting...</span>
                </div>
                <div id="timer-display" class="timer"></div>
            </div>

            <div class="current-holder">
                <h3 id="holder-name">Player Name</h3>
                <p id="holder-instruction">is choosing which hand holds the wee...</p>
            </div>

            <!-- Stick Holder View -->
            <div id="holder-view" class="holder-controls hidden">
                <h3>Choose your hand:</h3>
                <div class="stick-choice">
                    <button id="left-hand" class="hand-btn" data-choice="left">
                        <span class="hand-label">Camiq (Left)</span>
                    </button>
                    <button id="right-hand" class="hand-btn" data-choice="right">
                        <span class="hand-label">Taliq (Right)</span>
                    </button>
                </div>
            </div>

            <!-- Voting View -->
            <div id="voting-view" class="voting-controls hidden">
                <h3>Which hand has the wee?</h3>
                <div class="vote-choice">
                    <button id="vote-left" class="hand-btn" data-vote="left">
                        <span class="hand-label">Camiq (Left)</span>
                    </button>
                    <button id="vote-right" class="hand-btn" data-vote="right">
                        <span class="hand-label">Taliq (Right)</span>
                    </button>
                </div>
            </div>

            <!-- Results View -->
            <div id="results-view" class="results hidden">
                <div class="reveal">
                    <h3>The wee was in the <span id="correct-hand"></span> hand!</h3>
                    <div id="vote-summary" class="vote-summary"></div>
                </div>
                <button id="next-round-btn" class="btn btn-primary">Next Round</button>
            </div>

            <!-- Scoreboard -->
            <div class="scoreboard">
                <h4>Scores</h4>
                <div id="scores-list" class="scores-list"></div>
            </div>
        </div>

        <!-- Game End Screen -->
        <div id="end-screen" class="screen">
            <div class="winner-announcement">
                <h2>Game Complete!</h2>
                <div id="winner-display" class="winner"></div>
                <div id="final-scores" class="final-scores"></div>
            </div>
            <div class="actions">
                <button id="play-again-btn" class="btn btn-primary">Play Again</button>
                <button id="new-game-btn" class="btn btn-secondary">New Game</button>
            </div>
        </div>
    </div>

    <!-- Toast notifications -->
    <div id="toast-container" class="toast-container"></div>

    <script src="game.js"></script>
</body>
</html>''',

    'styles.css': '''/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #2c5f5d, #3a7270);
    min-height: 100vh;
    color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
}

#app {
    width: 100%;
    max-width: 400px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    min-height: 600px;
}

/* Screen management */
.screen {
    display: none;
    padding: 20px;
    min-height: 560px;
}

.screen.active {
    display: block;
}

/* Typography */
h1 {
    font-size: 2.5em;
    text-align: center;
    margin-bottom: 10px;
    color: #f0d58c;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

h2 {
    font-size: 1.8em;
    text-align: center;
    margin-bottom: 20px;
    color: #f0d58c;
}

h3 {
    font-size: 1.3em;
    margin-bottom: 15px;
    color: #e8e8e8;
}

.subtitle {
    text-align: center;
    font-size: 1.1em;
    color: #c8c8c8;
    margin-bottom: 30px;
}

/* Buttons */
.btn {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.btn-primary {
    background: linear-gradient(135deg, #d4af37, #b8941f);
    color: white;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #b8941f, #9e7a1a);
    transform: translateY(-2px);
}

.btn-primary:disabled {
    background: #666;
    cursor: not-allowed;
    transform: none;
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Form elements */
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    color: #e8e8e8;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
}

input:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.5);
}

/* Cultural info panel */
.cultural-info {
    margin: 20px 0;
}

.info-toggle {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
}

.info-panel {
    margin-top: 15px;
    padding: 15px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
    border-left: 4px solid #d4af37;
}

.info-panel.hidden {
    display: none;
}

/* Players list */
.players-list {
    display: grid;
    gap: 10px;
    margin-bottom: 20px;
}

.player-card {
    display: flex;
    align-items: center;
    padding: 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    border-left: 4px solid;
}

.player-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
}

.player-name {
    flex: 1;
    font-weight: bold;
}

.player-score {
    font-size: 18px;
    font-weight: bold;
    color: #d4af37;
}

/* Game screens */
.game-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 10px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
}

.round-info {
    display: flex;
    flex-direction: column;
    font-size: 14px;
}

.timer {
    font-size: 24px;
    font-weight: bold;
    color: #d4af37;
}

.current-holder {
    text-align: center;
    margin-bottom: 30px;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

.hand-btn {
    width: 48%;
    margin: 1%;
    padding: 20px;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

.hand-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.05);
}

.hand-btn.selected {
    background: rgba(212, 175, 55, 0.3);
    border-color: #d4af37;
}

.stick-choice, .vote-choice {
    display: flex;
    justify-content: space-between;
}

.hand-label {
    font-size: 16px;
    font-weight: bold;
}

/* Results */
.results {
    text-align: center;
    margin: 20px 0;
}

.vote-summary {
    margin: 20px 0;
    padding: 15px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
}

.vote-item {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
}

/* Scoreboard */
.scoreboard {
    margin-top: 30px;
    padding: 15px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 8px;
}

.scores-list {
    display: grid;
    gap: 5px;
}

.score-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
}

/* Winner screen */
.winner-announcement {
    text-align: center;
    margin-bottom: 30px;
}

.winner {
    font-size: 2em;
    color: #d4af37;
    margin: 20px 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* Utility classes */
.hidden {
    display: none !important;
}

/* Toast notifications */
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.toast {
    background: rgba(0, 0, 0, 0.9);
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    margin-bottom: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    animation: slideIn 0.3s ease;
}

.toast.success {
    border-left: 4px solid #4CAF50;
}

.toast.error {
    border-left: 4px solid #f44336;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

/* Responsive */
@media (max-width: 480px) {
    body {
        padding: 5px;
    }
    
    #app {
        max-width: 100%;
        border-radius: 10px;
    }
    
    .screen {
        padding: 15px;
        min-height: 500px;
    }
    
    h1 {
        font-size: 2em;
    }
    
    .btn {
        padding: 10px 16px;
        font-size: 14px;
    }
}''',

    'game.js': '''// Simple Kaataq Game Implementation
class KaataqGame {
    constructor() {
        this.gameState = 'welcome';
        this.roomCode = '';
        this.players = [];
        this.currentPlayer = null;
        this.isHost = false;
        
        // Game state
        this.currentRound = 1;
        this.currentHolderIndex = 0;
        this.stickChoice = null;
        this.playerVotes = {};
        this.roundPhase = 'waiting';
        this.timer = null;
        this.timeRemaining = 0;
        
        this.config = {
            minPlayers: 3,
            maxPlayers: 8,
            discussionTime: 45,
            votingTime: 30
        };
        
        this.colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'
        ];
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.showScreen('welcome');
    }
    
    bindEvents() {
        // Welcome screen
        document.getElementById('info-btn').addEventListener('click', () => {
            this.toggleInfoPanel();
        });
        
        document.getElementById('create-btn').addEventListener('click', () => {
            this.createRoom();
        });
        
        document.getElementById('join-btn').addEventListener('click', () => {
            this.showScreen('join-screen');
        });
        
        // Join screen
        document.getElementById('join-game-btn').addEventListener('click', () => {
            this.joinRoom();
        });
        
        document.getElementById('back-btn').addEventListener('click', () => {
            this.showScreen('welcome');
        });
        
        // Lobby screen
        document.getElementById('start-game-btn').addEventListener('click', () => {
            this.startGame();
        });
        
        document.getElementById('leave-btn').addEventListener('click', () => {
            this.leaveRoom();
        });
        
        // Game controls
        document.querySelectorAll('.hand-btn[data-choice]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.makeStickChoice(e.target.dataset.choice);
            });
        });
        
        document.querySelectorAll('.hand-btn[data-vote]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.castVote(e.target.dataset.vote);
            });
        });
        
        document.getElementById('next-round-btn').addEventListener('click', () => {
            this.nextRound();
        });
        
        // End game
        document.getElementById('play-again-btn').addEventListener('click', () => {
            this.resetGame();
        });
        
        document.getElementById('new-game-btn').addEventListener('click', () => {
            this.showScreen('welcome');
            this.resetGame();
        });
    }
    
    // Utility methods
    generateRoomCode() {
        return Math.floor(1000 + Math.random() * 9000).toString();
    }
    
    generatePlayerId() {
        return 'player_' + Math.random().toString(36).substr(2, 9);
    }
    
    showScreen(screenId) {
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.remove('active');
        });
        document.getElementById(screenId).classList.add('active');
        this.gameState = screenId;
    }
    
    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
    
    toggleInfoPanel() {
        const panel = document.getElementById('info-panel');
        panel.classList.toggle('hidden');
    }
    
    // Room management
    createRoom() {
        this.roomCode = this.generateRoomCode();
        this.isHost = true;
        
        const playerName = prompt('Enter your name:');
        if (!playerName) return;
        
        this.currentPlayer = {
            id: this.generatePlayerId(),
            name: playerName,
            score: 0,
            color: this.colors[0]
        };
        
        this.players = [this.currentPlayer];
        this.updateLobby();
        this.showScreen('lobby');
        this.showToast('Room created! Share the code with others.', 'success');
    }
    
    joinRoom() {
        const roomCode = document.getElementById('room-code-input').value;
        const playerName = document.getElementById('player-name-input').value;
        
        if (!roomCode || !playerName) {
            this.showToast('Please enter room code and your name.', 'error');
            return;
        }
        
        // Simulate joining (in real implementation, this would be a server call)
        this.roomCode = roomCode;
        this.currentPlayer = {
            id: this.generatePlayerId(),
            name: playerName,
            score: 0,
            color: this.colors[this.players.length]
        };
        
        this.players.push(this.currentPlayer);
        this.updateLobby();
        this.showScreen('lobby');
        this.showToast('Joined room successfully!', 'success');
    }
    
    leaveRoom() {
        this.resetGame();
        this.showScreen('welcome');
    }
    
    updateLobby() {
        document.getElementById('room-code-display').textContent = this.roomCode;
        document.getElementById('player-count').textContent = this.players.length;
        
        const playersList = document.getElementById('players-list');
        playersList.innerHTML = '';
        
        this.players.forEach(player => {
            const card = document.createElement('div');
            card.className = 'player-card';
            card.style.borderLeftColor = player.color;
            
            card.innerHTML = `
                <div class="player-avatar" style="background-color: ${player.color}">
                    ${player.name.charAt(0).toUpperCase()}
                </div>
                <div class="player-name">${player.name}</div>
            `;
            
            playersList.appendChild(card);
        });
        
        const startBtn = document.getElementById('start-game-btn');
        startBtn.disabled = this.players.length < this.config.minPlayers || !this.isHost;
    }
    
    // Game logic
    startGame() {
        this.currentRound = 1;
        this.currentHolderIndex = 0;
        this.showScreen('game-screen');
        this.startRound();
    }
    
    startRound() {
        this.roundPhase = 'choosing';
        this.stickChoice = null;
        this.playerVotes = {};
        
        this.updateGameDisplay();
        
        if (this.isCurrentPlayerHolder()) {
            this.showHolderView();
        } else {
            this.showWaitingView();
        }
    }
    
    isCurrentPlayerHolder() {
        return this.players[this.currentHolderIndex].id === this.currentPlayer.id;
    }
    
    getCurrentHolder() {
        return this.players[this.currentHolderIndex];
    }
    
    showHolderView() {
        document.getElementById('holder-view').classList.remove('hidden');
        document.getElementById('voting-view').classList.add('hidden');
        document.getElementById('results-view').classList.add('hidden');
    }
    
    showWaitingView() {
        document.getElementById('holder-view').classList.add('hidden');
        document.getElementById('voting-view').classList.add('hidden');
        document.getElementById('results-view').classList.add('hidden');
    }
    
    showVotingView() {
        document.getElementById('holder-view').classList.add('hidden');
        document.getElementById('voting-view').classList.remove('hidden');
        document.getElementById('results-view').classList.add('hidden');
        
        this.startTimer(this.config.votingTime);
    }
    
    makeStickChoice(choice) {
        this.stickChoice = choice;
        document.querySelectorAll('.hand-btn[data-choice]').forEach(btn => {
            btn.classList.remove('selected');
        });
        document.querySelector(`[data-choice="${choice}"]`).classList.add('selected');
        
        // Auto-proceed after choice
        setTimeout(() => {
            this.roundPhase = 'voting';
            this.updateGameDisplay();
            this.showVotingView();
        }, 1000);
    }
    
    castVote(vote) {
        this.playerVotes[this.currentPlayer.id] = vote;
        document.querySelectorAll('.hand-btn[data-vote]').forEach(btn => {
            btn.classList.remove('selected');
        });
        document.querySelector(`[data-vote="${vote}"]`).classList.add('selected');
        
        // Check if everyone has voted
        const votingPlayers = this.players.filter(p => p.id !== this.getCurrentHolder().id);
        if (Object.keys(this.playerVotes).length === votingPlayers.length) {
            this.showResults();
        }
    }
    
    showResults() {
        this.roundPhase = 'results';
        this.clearTimer();
        
        document.getElementById('holder-view').classList.add('hidden');
        document.getElementById('voting-view').classList.add('hidden');
        document.getElementById('results-view').classList.remove('hidden');
        
        this.calculateScores();
        this.updateGameDisplay();
    }
    
    calculateScores() {
        const correctHand = this.stickChoice;
        const holder = this.getCurrentHolder();
        let correctGuesses = 0;
        
        // Count correct guesses
        Object.values(this.playerVotes).forEach(vote => {
            if (vote === correctHand) {
                correctGuesses++;
            }
        });
        
        // Award points
        this.players.forEach(player => {
            if (player.id === holder.id) {
                // Holder gets points if less than half guess correctly
                if (correctGuesses < Object.keys(this.playerVotes).length / 2) {
                    player.score += 1;
                }
            } else if (this.playerVotes[player.id] === correctHand) {
                // Correct guessers get points
                player.score += 1;
            }
        });
    }
    
    updateGameDisplay() {
        document.getElementById('current-round').textContent = this.currentRound;
        
        const holder = this.getCurrentHolder();
        document.getElementById('holder-name').textContent = holder.name;
        
        const phaseTexts = {
            'choosing': 'is choosing which hand holds the wee...',
            'voting': 'Vote for which hand has the wee!',
            'results': 'Round complete!'
        };
        
        document.getElementById('holder-instruction').textContent = phaseTexts[this.roundPhase] || '';
        
        if (this.roundPhase === 'results') {
            const handName = this.stickChoice === 'left' ? 'Camiq (Left)' : 'Taliq (Right)';
            document.getElementById('correct-hand').textContent = handName;
            
            // Update vote summary
            this.updateVoteSummary();
        }
        
        this.updateScoreboard();
    }
    
    updateVoteSummary() {
        const summary = document.getElementById('vote-summary');
        summary.innerHTML = '';
        
        const leftVotes = Object.values(this.playerVotes).filter(v => v === 'left').length;
        const rightVotes = Object.values(this.playerVotes).filter(v => v === 'right').length;
        
        summary.innerHTML = `
            <div class="vote-item">
                <span>Camiq (Left):</span>
                <span>${leftVotes} votes</span>
            </div>
            <div class="vote-item">
                <span>Taliq (Right):</span>
                <span>${rightVotes} votes</span>
            </div>
        `;
    }
    
    updateScoreboard() {
        const scoresList = document.getElementById('scores-list');
        scoresList.innerHTML = '';
        
        // Sort players by score
        const sortedPlayers = [...this.players].sort((a, b) => b.score - a.score);
        
        sortedPlayers.forEach(player => {
            const item = document.createElement('div');
            item.className = 'score-item';
            item.innerHTML = `
                <span>${player.name}</span>
                <span class="player-score">${player.score}</span>
            `;
            scoresList.appendChild(item);
        });
    }
    
    nextRound() {
        this.currentRound++;
        this.currentHolderIndex = (this.currentHolderIndex + 1) % this.players.length;
        
        // Check if game should end
        if (this.currentRound > this.players.length) {
            this.endGame();
        } else {
            this.startRound();
        }
    }
    
    endGame() {
        // Find winner
        const winner = this.players.reduce((prev, current) => 
            prev.score > current.score ? prev : current
        );
        
        document.getElementById('winner-display').textContent = 
            `${winner.name} wins with ${winner.score} points!`;
        
        // Show final scores
        const finalScores = document.getElementById('final-scores');
        finalScores.innerHTML = '';
        
        const sortedPlayers = [...this.players].sort((a, b) => b.score - a.score);
        sortedPlayers.forEach((player, index) => {
            const item = document.createElement('div');
            item.className = 'score-item';
            item.innerHTML = `
                <span>${index + 1}. ${player.name}</span>
                <span>${player.score} points</span>
            `;
            finalScores.appendChild(item);
        });
        
        this.showScreen('end-screen');
    }
    
    startTimer(seconds) {
        this.clearTimer();
        this.timeRemaining = seconds;
        this.updateTimerDisplay();
        
        this.timer = setInterval(() => {
            this.timeRemaining--;
            this.updateTimerDisplay();
            
            if (this.timeRemaining <= 0) {
                this.clearTimer();
                if (this.roundPhase === 'voting') {
                    this.showResults();
                }
            }
        }, 1000);
    }
    
    clearTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }
    
    updateTimerDisplay() {
        const display = document.getElementById('timer-display');
        if (this.timeRemaining > 0) {
            display.textContent = `${this.timeRemaining}s`;
        } else {
            display.textContent = '';
        }
    }
    
    resetGame() {
        this.clearTimer();
        this.players.forEach(player => {
            player.score = 0;
        });
        this.currentRound = 1;
        this.currentHolderIndex = 0;
        this.roundPhase = 'waiting';
        this.playerVotes = {};
        this.stickChoice = null;
    }
}

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const game = new KaataqGame();
});''',
    
    'README.md': '''# Kaataq - Traditional Alutiiq Game

A digital adaptation of the traditional Alutiiq stick guessing game, designed as a mobile-friendly multiplayer experience.

## About the Game

Kaataq is a traditional Alutiiq guessing game involving psychological gameplay and social interaction. Players take turns hiding a marked stick (wee) in one of their hands, while others try to guess which hand contains it.

## Features

- Mobile-responsive design
- Room-based multiplayer (3-8 players)
- Cultural education panel
- Turn-based gameplay with scoring
- Clean, accessible interface

## Setup

1. Clone this repository
2. Enable GitHub Pages in repository settings
3. Your game will be available at: `https://[username].github.io/[repository-name]`

## Cultural Note

This game is inspired by traditional Alutiiq gaming practices. The cultural information is sourced from the Alutiiq Museum and Archaeological Repository.

## Technology

- Pure HTML, CSS, and JavaScript
- No external dependencies
- Mobile-first responsive design
- Local multiplayer simulation'''
}

print("Created basic game structure:")
for filename, content in structure.items():
    print(f"- {filename}")
    
# Save each file
for filename, content in structure.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"\nFiles created successfully!")
print("Total files:", len(structure))
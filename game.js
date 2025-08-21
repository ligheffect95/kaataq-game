// Simple Kaataq Game Implementation
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
});
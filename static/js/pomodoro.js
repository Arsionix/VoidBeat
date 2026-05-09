let pomodoroTime = 25 * 60;
let pomodoroInterval = null;
let isWorkMode = true;
let pendingMode = null;

function pomodoroSave() {
    localStorage.setItem('pomodoro_time', pomodoroTime);
    localStorage.setItem('pomodoro_running', pomodoroInterval !== null);
    localStorage.setItem('pomodoro_mode', isWorkMode);
}

function pomodoroLoad() {
    let savedTime = localStorage.getItem('pomodoro_time');
    let wasRunning = localStorage.getItem('pomodoro_running') === 'true';
    let savedMode = localStorage.getItem('pomodoro_mode');
    
    if (savedTime) {
        pomodoroTime = parseInt(savedTime);
    } else {
        pomodoroTime = 25 * 60;
    }
    
    if (savedMode === 'false') {
        isWorkMode = false;
    } else {
        isWorkMode = true;
    }
    
    pomodoroUpdateDisplay();
    
    if (wasRunning && pomodoroTime > 0) {
        pomodoroStart();
    }
}

function pomodoroUpdateDisplay() {
    let minutes = Math.floor(pomodoroTime / 60);
    let seconds = pomodoroTime % 60;
    let display = document.getElementById('timer');
    let modeDisplay = document.getElementById('timerMode');
    
    if (display) {
        display.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    if (modeDisplay) {
        modeDisplay.textContent = isWorkMode ? 'Работа' : 'Перерыв';
    }
    
    pomodoroSave();
}

function pomodoroStopMusic() {
    let player = document.getElementById('player');
    if (player && !player.paused) {
        player.pause();
    }
}

function pomodoroShowNotification(message, nextMode) {
    let notificationDiv = document.getElementById('pomodoro-notification');
    let messageSpan = document.getElementById('notification-message');
    
    messageSpan.textContent = message;
    pendingMode = nextMode;
    notificationDiv.style.display = 'block';
}

function pomodoroConfirm() {
    let notificationDiv = document.getElementById('pomodoro-notification');
    notificationDiv.style.display = 'none';
    
    if (pendingMode === 'break') {
        isWorkMode = false;
        pomodoroTime = 5 * 60;
    } else if (pendingMode === 'work') {
        isWorkMode = true;
        pomodoroTime = 25 * 60;
    }
    
    pomodoroUpdateDisplay();
    pomodoroStart();
}

function pomodoroCancel() {
    let notificationDiv = document.getElementById('pomodoro-notification');
    notificationDiv.style.display = 'none';
    pomodoroReset();
}

function pomodoroStart() {
    if (pomodoroInterval) return;
    
    pomodoroInterval = setInterval(() => {
        if (pomodoroTime <= 0) {
            clearInterval(pomodoroInterval);
            pomodoroInterval = null;
            
            pomodoroStopMusic();
            
            if (isWorkMode) {
                pomodoroShowNotification('Время работы вышло! Начать перерыв на 5 минут?', 'break');
            } else {
                pomodoroShowNotification('Перерыв закончился! Начать работу на 25 минут?', 'work');
            }
        } else {
            pomodoroTime--;
            pomodoroUpdateDisplay();
        }
    }, 1000);
    pomodoroSave();
}

function pomodoroPause() {
    clearInterval(pomodoroInterval);
    pomodoroInterval = null;
    pomodoroSave();
}

function pomodoroReset() {
    clearInterval(pomodoroInterval);
    pomodoroInterval = null;
    isWorkMode = true;
    pomodoroTime = 25 * 60;
    pomodoroUpdateDisplay();
    pomodoroSave();
    
    let notificationDiv = document.getElementById('pomodoro-notification');
    if (notificationDiv) {
        notificationDiv.style.display = 'none';
    }
}

pomodoroLoad();
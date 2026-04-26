function createLikeButton(track) {
    const btn = document.createElement('button');
    updateLikeButton(btn, track);
    
    btn.onclick = function() {
        const logoutBtn = document.querySelector('a[href="/logout"]');
        if (!logoutBtn) {
            alert('Нужно войти, чтобы ставить лайки');
            return;
        }
        
        const newValue = track.user_liked ? 0 : 1;
        
        fetch('/api/rate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({track_id: track.id, value: newValue})
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    };
    
    return btn;
}

function updateLikeButton(btn, track) {
    btn.textContent = (track.user_liked ? '❤️' : '🤍') + ' ' + track.likes;
    btn.style.color = track.user_liked ? 'red' : 'black';
}

function createDislikeButton(track) {
    const btn = document.createElement('button');
    updateDislikeButton(btn, track);
    
    btn.onclick = function() {
        const logoutBtn = document.querySelector('a[href="/logout"]');
        if (!logoutBtn) {
            alert('Нужно войти, чтобы ставить дизлайки');
            return;
        }
        
        const newValue = track.user_disliked ? 0 : -1;
        
        fetch('/api/rate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({track_id: track.id, value: newValue})
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    };
    
    return btn;
}

function updateDislikeButton(btn, track) {
    btn.textContent = (track.user_disliked ? '💔' : '🖤') + ' ' + track.dislikes;
    btn.style.color = track.user_disliked ? 'blue' : 'black';
}
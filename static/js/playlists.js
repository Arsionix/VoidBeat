function createAddToPlaylistButton(track) {
    const btn = document.createElement('button');
    btn.textContent = ' 📁 Добавить в плейлист';
    
    btn.onclick = function() {
        const logoutBtn = document.querySelector('a[href="/logout"]');
        if (!logoutBtn) {
            alert('Нужно войти, чтобы добавлять в плейлисты');
            return;
        }
        
        fetch('/api/playlists')
            .then(response => response.json())
            .then(playlists => {
                if (playlists.length === 0) {
                    alert('У вас нет плейлистов. Создайте сначала на странице /playlists');
                    return;
                }
                
                let message = 'Выберите плейлист:\n';
                for (let i = 0; i < playlists.length; i++) {
                    message += (i + 1) + '. ' + playlists[i].name + '\n';
                }
                const choice = prompt(message);
                const index = parseInt(choice) - 1;
                
                if (index >= 0 && index < playlists.length) {
                    const playlist = playlists[index];
                    fetch(`/api/playlists/${playlist.id}/tracks`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({track_id: track.id})
                    }).then(() => {
                        alert('Трек добавлен в плейлист!');
                    });
                }
            });
    };
    
    return btn;
}

function createRemoveFromPlaylistButton(track) {
    const btn = document.createElement('button');
    btn.textContent = ' ❌ Удалить из плейлиста';
    
    btn.onclick = function() {
        const logoutBtn = document.querySelector('a[href="/logout"]');
        if (!logoutBtn) {
            alert('Нужно войти, чтобы удалять из плейлистов');
            return;
        }
        
        fetch('/api/playlists')
            .then(response => response.json())
            .then(playlists => {
                if (playlists.length === 0) {
                    alert('У вас нет плейлистов');
                    return;
                }
                
                let message = 'Из какого плейлиста удалить?\n';
                for (let i = 0; i < playlists.length; i++) {
                    message += (i + 1) + '. ' + playlists[i].name + '\n';
                }
                const choice = prompt(message);
                const index = parseInt(choice) - 1;
                
                if (index >= 0 && index < playlists.length) {
                    const playlist = playlists[index];
                    fetch(`/api/playlists/${playlist.id}/tracks/${track.id}`, {
                        method: 'DELETE',
                        headers: {'Content-Type': 'application/json'}
                    }).then(() => {
                        alert('Трек удалён из плейлиста!');
                    });
                }
            });
    };
    
    return btn;
}
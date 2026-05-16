let currentPlaylistId = null;

function loadPlaylists() {
    fetch('/api/playlists')
        .then(response => response.json())
        .then(playlists => {
            const container = document.getElementById('playlists-list');
            container.innerHTML = '';
            
            if (playlists.length === 0) {
                container.innerHTML = '<p>У вас пока нет плейлистов</p>';
                return;
            }
            
            for (let i = 0; i < playlists.length; i++) {
                const p = playlists[i];
                const div = document.createElement('div');
                div.className = 'playlist-item';
                div.style.margin = '5px';
                div.style.padding = '10px';
                div.style.border = '1px solid #ddd';
                div.style.borderRadius = '5px';
                div.style.cursor = 'pointer';
                div.style.backgroundColor = currentPlaylistId === p.id ? '#e3f2fd' : 'white';
                
                const title = document.createElement('strong');
                title.textContent = p.name;
                title.style.paddingRight = '10px';
                title.style.color = 'black';
                div.appendChild(title);
                
                const viewBtn = document.createElement('button');
                viewBtn.textContent = 'Показать треки';
                viewBtn.className = 'btn btn-sm btn-info';
                viewBtn.style.marginRight = '5px';
                viewBtn.onclick = function(e) {
                    e.stopPropagation();
                    currentPlaylistId = p.id;
                    document.getElementById('current-playlist-name').textContent = p.name;
                    loadPlaylistTracks(p.id);
                    loadPlaylists();
                };
                div.appendChild(viewBtn);
                
                const delBtn = document.createElement('button');
                delBtn.textContent = 'Удалить';
                delBtn.className = 'btn btn-sm btn-danger';
                delBtn.onclick = function(e) {
                    e.stopPropagation();
                    if (confirm(`Удалить плейлист "${p.name}"?`)) {
                        fetch(`/api/playlists/${p.id}`, {
                            method: 'DELETE',
                            headers: {'Content-Type': 'application/json'}
                        }).then(() => {
                            if (currentPlaylistId === p.id) {
                                currentPlaylistId = null;
                                document.getElementById('current-playlist-name').textContent = '';
                                document.getElementById('playlist-tracks').innerHTML = '';
                            }
                            loadPlaylists();
                        });
                    }
                };
                div.appendChild(delBtn);
                
                container.appendChild(div);
            }
        });
}

function loadPlaylistTracks(playlistId) {
    fetch(`/api/playlists/${playlistId}/tracks`)
        .then(response => response.json())
        .then(tracks => {
            const tracksContainer = document.getElementById('playlist-tracks');
            tracksContainer.innerHTML = '';
            
            if (!tracks || tracks.length === 0) {
                tracksContainer.innerHTML = '<p>В этом плейлисте нет треков</p>';
                return;
            }
            
            for (let i = 0; i < tracks.length; i++) {
                const track = tracks[i];
                const trackDiv = document.createElement('div');
                trackDiv.className = 'track-item';
                trackDiv.style.margin = '10px 0';
                trackDiv.style.padding = '10px';
                trackDiv.style.border = '1px solid #ddd';
                trackDiv.style.borderRadius = '5px';
                
                const trackInfo = document.createElement('div');
                trackInfo.innerHTML = `
                    <strong>${escapeHtml(track.title)}</strong> - ${escapeHtml(track.artist)}
                    <br>
                    <small>Прослушиваний: ${track.plays_count || 0}</small>
                    <br>
                    <audio src="${track.file_url}" controls style="margin-top: 5px;"></audio>
                `;
                trackDiv.appendChild(trackInfo);
                
                const removeBtn = document.createElement('button');
                removeBtn.textContent = '❌ Удалить из плейлиста';
                removeBtn.className = 'btn btn-sm btn-warning mt-2';
                removeBtn.onclick = function() {
                    if (confirm(`Удалить трек "${track.title}" из плейлиста?`)) {
                        fetch(`/api/playlists/${playlistId}/tracks/${track.id}`, {
                            method: 'DELETE',
                            headers: {'Content-Type': 'application/json'}
                        }).then(() => {
                            loadPlaylistTracks(playlistId);
                        });
                    }
                };
                trackDiv.appendChild(removeBtn);
                
                tracksContainer.appendChild(trackDiv);
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки треков:', error);
            document.getElementById('playlist-tracks').innerHTML = '<p>Ошибка загрузки треков</p>';
        });
}

function setupCreatePlaylist() {
    const createBtn = document.getElementById('create-btn');
    if (!createBtn) return;
    
    createBtn.onclick = function() {
        const nameInput = document.getElementById('playlist-name');
        const name = nameInput.value.trim();
        
        if (name === '') {
            alert('Введите название плейлиста');
            return;
        }
        
        fetch('/api/playlists', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name: name})
        }).then(() => {
            nameInput.value = '';
            loadPlaylists();
        });
    };
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

loadPlaylists();
setupCreatePlaylist();
function loadPlaylists() {
    fetch('/api/playlists')
        .then(response => response.json())
        .then(playlists => {
            const container = document.getElementById('playlists-list');
            container.innerHTML = '';
            
            for (let i = 0; i < playlists.length; i++) {
                const p = playlists[i];
                const div = document.createElement('div');
                const title = document.createElement('strong');
                
                div.style.margin = '5px';
                div.style.padding = '5px';
                div.style.border = '1px solid gray';

                title.textContent = p.name;
                title.style.paddingRight = '5px';
                div.appendChild(title);

                const delBtn = document.createElement('button');
                delBtn.textContent = 'Удалить';
                delBtn.style.color = 'red';

                delBtn.onclick = function() {
                    fetch(`/api/playlists/${p.id}`, {
                        method: 'DELETE',
                        headers: {'Content-Type': 'application/json'}
                    }).then(() => {
                        loadPlaylists();
                    });
                };
                div.appendChild(delBtn);
                container.appendChild(div);
            }
        });
}

function setupCreatePlaylist() {
    const createBtn = document.getElementById('create-btn');
    if (!createBtn) return;
    
    createBtn.onclick = function() {
        const nameInput = document.getElementById('playlist-name');
        const name = nameInput.value;
        
        if (name.trim() === '') {
            alert('Введите название');
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

loadPlaylists();
setupCreatePlaylist();
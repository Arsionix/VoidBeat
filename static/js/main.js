function loadTracks() {
    fetch('/api/tracks')
        .then(response => response.json())
        .then(tracks => {
            const container = document.getElementById('track-list');
            container.innerHTML = '';
            
            for (let i = 0; i < tracks.length; i++) {
                const track = tracks[i];
                const card = createTrackCard(track);
                container.appendChild(card);
            }
        });
}

function createTrackCard(track) {
    const card = document.createElement('div');
    card.style.border = '1px solid gray';
    card.style.margin = '10px';
    card.style.padding = '10px';
    card.style.borderRadius = '5px';
    
    const title = document.createElement('strong');
    title.textContent = track.title + ' - ' + track.artist;
    card.appendChild(title);
    card.appendChild(document.createElement('br'));
    
    const ratingContainer = document.createElement('div');
    ratingContainer.style.display = 'flex';
    ratingContainer.style.gap = '5px';
    ratingContainer.style.marginTop = '5px';
    
    const likeBtn = createLikeButton(track);
    ratingContainer.appendChild(likeBtn);
    
    const dislikeBtn = createDislikeButton(track);
    ratingContainer.appendChild(dislikeBtn);
    
    card.appendChild(ratingContainer);
    
    const playlistBtn = createAddToPlaylistButton(track);
    card.appendChild(playlistBtn);
    
    const removeFromPlaylistBtn = createRemoveFromPlaylistButton(track);
    card.appendChild(removeFromPlaylistBtn);
    
    const playBtn = document.createElement('button');
    playBtn.textContent = ' ▶ Воспроизвести';
    playBtn.onclick = () => playTrack(track);
    card.appendChild(playBtn);
    
    return card;
}

function playTrack(track) {
    const player = document.getElementById('player');
    player.src = track.file_url;
    player.play();
    document.getElementById('current-track').textContent = track.title;
}

loadTracks();
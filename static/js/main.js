let currentSearchQuery = '';

let currentPage = 1;
let totalPages = 1;

function loadTracks() {
    let url = `/api/tracks?page=${currentPage}&per_page=20`;
    if (currentSearchQuery) {
        url += `&q=${encodeURIComponent(currentSearchQuery)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tracks = data.tracks;
            totalPages = data.total_pages;
            currentPage = data.page;
            
            const container = document.getElementById('track-list');
            container.innerHTML = '';
            
            if (tracks.length === 0) {
                container.innerHTML = '<p>Ничего не найдено</p>';
                return;
            }
            
            for (let i = 0; i < tracks.length; i++) {
                const track = tracks[i];
                const card = createTrackCard(track);
                container.appendChild(card);
            }
            
            addPaginationButtons();
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

    fetch(`/api/tracks/${track.id}/play`, {method: 'POST', headers: {'Content-Type': 'application/json'}})
        .then(response => response.json())
        .then(data => {
            console.log(`Прослушиваний: ${data.plays_count}`);
        });
}

function setupSearch() {
    const searchBtn = document.getElementById('search-btn');
    const clearBtn = document.getElementById('clear-search');
    const searchInput = document.getElementById('search-input');
    
    if (searchBtn) {
        searchBtn.onclick = function() {
            currentSearchQuery = searchInput.value;
            loadTracks();
        };
    }
    
    if (clearBtn) {
        clearBtn.onclick = function() {
            searchInput.value = '';
            currentSearchQuery = '';
            loadTracks();
        };
    }
    
    if (searchInput) {
        searchInput.onkeypress = function(e) {
            if (e.key === 'Enter') {
                currentSearchQuery = searchInput.value;
                loadTracks();
            }
        };
    }
}

function addPaginationButtons() {
    const container = document.getElementById('track-list');
    const paginationDiv = document.createElement('div');
    paginationDiv.style.marginTop = '20px';
    paginationDiv.style.display = 'flex';
    paginationDiv.style.gap = '10px';
    paginationDiv.style.justifyContent = 'center';
    
    const prevBtn = document.createElement('button');
    prevBtn.textContent = 'Предыдущая';
    prevBtn.disabled = (currentPage <= 1);
    prevBtn.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            loadTracks();
        }
    };
    paginationDiv.appendChild(prevBtn);
    
    const pageInfo = document.createElement('span');
    pageInfo.textContent = `Страница ${currentPage} из ${totalPages}`;
    pageInfo.style.padding = '0 10px';
    paginationDiv.appendChild(pageInfo);
    
    const nextBtn = document.createElement('button');
    nextBtn.textContent = 'Следующая';
    nextBtn.disabled = (currentPage >= totalPages);
    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadTracks();
        }
    };
    paginationDiv.appendChild(nextBtn);
    
    container.appendChild(paginationDiv);
}

loadTracks();
setupSearch();
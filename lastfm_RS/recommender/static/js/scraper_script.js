$(document).ready(function () {
    if (scrape) {
        openLoader(`Scraping ${scrape[0][0]}...`);
        requestItems(0);
    }
})

function requestItems(index) {
    const item  = scrape[index][0],
          limit = scrape[index][1];

    $.ajax({
        url: `user_scraper/${item}`,
        type: "GET",
        data: {
            'user':   user,
            'limit':  limit,
            'use_db': useDb
        },
        cache: true,
        timeout: 0,
        success: function (partialData) {
            hideLoader();

            if ('ERROR' in partialData) {
                error(partialData['ERROR']);
                return;
            }

            loadItems(item, partialData);

            if (index + 1 < scrape.length) {
                openLoader(`Scraping ${scrape[index + 1][0]}...`);
                requestItems(index + 1);
            } else {
                openLoader('Done!');
                setTimeout(() => hideLoader(), 1500);
                scrollToBottom();
            }
        },
        error: function () {
            hideLoader();
            error('Error during data retrieval');
        }
    });
}

function error(msg) {
    const div = document.querySelector("#scrape-tracks");

    div.innerHTML   = `<h4>${msg}</h4>`;
    div.style.color = 'darkred';
    showElement("#scrape-tracks");
}

function loadItems(item, partialData) {
    switch (item) {
        case 'tracks':
            loadTracks(partialData);
            break;
        case 'artists':
            loadArtists(partialData);
            break;
        case 'albums':
            loadAlbums(partialData);
            break;
        case 'tags':
            loadTags(partialData);
            break;
        default:
            console.warn(`Unknown item: ${item}`);
            break;
    }
}

function showElement(className) {
    const elementStyle = document.querySelector(className).style;

    elementStyle.height   = 'auto';
    elementStyle.opacity  = 1;
    elementStyle.overflow = 'auto';
    elementStyle.margin   = '30px 20px 10px 20px';
}

function insertTagCell(cell, item, itemType) {
    cell.innerHTML = '';
    cell.className = createId(item, itemType);
}

function createId(item, type) {
    let id;

    if (Array.isArray(item)) {
        item.unshift(type);
        id = item.join('_');
    }
    else
        id = `${type}_${item}`;

    return id.replace(/\W/g, '_');
}

function noElementsMessage(table, item) {
    document.querySelector(table).replaceWith(`No ${item} retrieved`);
}

function loadTracks(data) {
    const topTracksTbody = document.querySelector("#top-tracks"),
        lovedTracksTbody = document.querySelector("#loved-tracks"),
        recentTracksTbody = document.querySelector("#recent-tracks");

    if (data['top_tracks'].length === 0)
        noElementsMessage(".top-tracks-table", "top tracks");
    if (data['loved_tracks'].length === 0)
        noElementsMessage(".loved-tracks-table", "loved tracks");
    if (data['recent_tracks'].length === 0)
        noElementsMessage(".recent-tracks-table", "recent tracks");

    data['top_tracks'].forEach(track => {
        const row = topTracksTbody.insertRow();

        track.forEach((column, index) => {
            row.insertCell(index).innerHTML = column;
        });
        if (doTags)
            insertTagCell(row.insertCell(3), track, 'tracks');
    });

    ['loved_tracks', 'recent_tracks'].forEach((trackKey, recent) => {

        data[trackKey].forEach((track) => {
            const row = (recent ? recentTracksTbody : lovedTracksTbody).insertRow();

            track[3] = (new Date(track[3] * 1000)).toUTCString();

            track.forEach((column, colIndex) => {
                row.insertCell(colIndex).innerHTML = column;
            });
            if (doTags) {
                track.pop();
                insertTagCell(row.insertCell(4), track, 'tracks');
            }
        });
    });
    showElement("#scrape-tracks");
}

function loadArtists(data) {
    const top_artists_tbody = document.querySelector("#top-artists");

    if (data['top_artists'].length === 0)
        noElementsMessage(".top-artists-table", "artists");

    data['top_artists'].forEach(artist => {
        const row = top_artists_tbody.insertRow();

        row.insertCell(0).innerHTML = artist;
        if (doTags)
            insertTagCell(row.insertCell(1), artist, 'artists');
    });
    showElement("#scrape-artists");
}

function loadAlbums(data) {
    const top_albums_tbody = document.querySelector("#top-albums");

    if (data['top_albums'].length === 0)
        noElementsMessage(".top-albums-table", "albums");

    data['top_albums'].forEach(album => {
        const row = top_albums_tbody.insertRow();

        album.forEach((column, colIndex) => {
            row.insertCell(colIndex).innerHTML = column;
        });
        if (doTags)
            insertTagCell(row.insertCell(2), album, 'albums');
    });
    showElement("#scrape-albums");
}

function loadTags(data) {
    Object.keys(data['item_tags']).forEach((itemType) => {
        data['item_tags'][itemType].forEach((item) => {
            const id = createId(item[0], itemType.toLowerCase()),
                tagCells = document.querySelectorAll(`.${id}`);

            Array.from(tagCells).forEach((cell) => {
                cell.innerHTML = Array.from(item[1]).join(", ");
            });
        })
    });

    if (data['tags_count'].length === 0)
        noElementsMessage("#tags-piechart", "tags");
    else
        tagPieChart('#tags-piechart', data['tags_count'].map(x => x[0]), data['tags_count'].map(x => x[1]));
    showElement("#scrape-tags");
}

function tagPieChart(canvas, labels, frequencies) {
    const pieCanvas = document.querySelector(canvas);
    pieCanvas.style.height = 'auto';
    return new Chart(
        pieCanvas,
        {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Frequency',
                        data: frequencies,
                    }
                ]
            },
            options: {
                radius: '90%',
            }
        }
    );
}
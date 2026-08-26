"""Genre whitelist and the offline fallback playlists shown when the model
provider is unavailable. Both are defined once, here, so the request schema
and the fallback lookup can never drift apart."""

PLAYLIST_SIZE = 5

GENRES = [
    "Afrobeats",
    "Amapiano",
    "Highlife",
    "Jazz",
    "Hip hop",
    "Rock",
    "Classical",
    "Electronic",
]

FALLBACK_PLAYLISTS = {
    "Afrobeats": [
        {"title": "Essence", "artist": "Wizkid ft. Tems"},
        {"title": "Ye", "artist": "Burna Boy"},
        {"title": "Fall", "artist": "Davido"},
        {"title": "Joro", "artist": "Wizkid"},
        {"title": "Last Last", "artist": "Burna Boy"},
    ],
    "Amapiano": [
        {"title": "Amapiano", "artist": "Kabza De Small & DJ Maphorisa"},
        {"title": "Adiwele", "artist": "Kabza De Small & DJ Maphorisa ft. Young Stunna"},
        {"title": "John Wick", "artist": "Pcee"},
        {"title": "Sponono", "artist": "Kabza De Small & DJ Maphorisa ft. Wizkid & Burna Boy"},
        {"title": "Asibe Happy", "artist": "Kabza De Small & DJ Maphorisa ft. Ami Faku"},
    ],
    "Highlife": [
        {"title": "Sweet Mother", "artist": "Prince Nico Mbarga"},
        {"title": "205", "artist": "E.T. Mensah"},
        {"title": "Sunshine Day", "artist": "Osibisa"},
        {"title": "Woman", "artist": "Osibisa"},
        {"title": "Ebi Te Yie", "artist": "Nana Ampadu & the African Brothers Band"},
    ],
    "Jazz": [
        {"title": "Take Five", "artist": "Dave Brubeck"},
        {"title": "So What", "artist": "Miles Davis"},
        {"title": "My Favorite Things", "artist": "John Coltrane"},
        {"title": "'Round Midnight", "artist": "Thelonious Monk"},
        {"title": "Feeling Good", "artist": "Nina Simone"},
    ],
    "Hip hop": [
        {"title": "Juicy", "artist": "The Notorious B.I.G."},
        {"title": "Sicko Mode", "artist": "Travis Scott"},
        {"title": "HUMBLE.", "artist": "Kendrick Lamar"},
        {"title": "Lose Yourself", "artist": "Eminem"},
        {"title": "God's Plan", "artist": "Drake"},
    ],
    "Rock": [
        {"title": "Bohemian Rhapsody", "artist": "Queen"},
        {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses"},
        {"title": "Smells Like Teen Spirit", "artist": "Nirvana"},
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin"},
        {"title": "Hotel California", "artist": "Eagles"},
    ],
    "Classical": [
        {"title": "Symphony No. 5 in C minor", "artist": "Ludwig van Beethoven"},
        {"title": "The Four Seasons: Spring", "artist": "Antonio Vivaldi"},
        {"title": "Clair de Lune", "artist": "Claude Debussy"},
        {"title": "Eine kleine Nachtmusik", "artist": "Wolfgang Amadeus Mozart"},
        {"title": "Canon in D", "artist": "Johann Pachelbel"},
    ],
    "Electronic": [
        {"title": "One More Time", "artist": "Daft Punk"},
        {"title": "Strobe", "artist": "deadmau5"},
        {"title": "Levels", "artist": "Avicii"},
        {"title": "Titanium", "artist": "David Guetta ft. Sia"},
        {"title": "Get Lucky", "artist": "Daft Punk ft. Pharrell Williams"},
    ],
}

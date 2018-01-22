# playlist-tuneup

Playlist tuneup is designed to take your playlists, and make them better.
Instead of having jarring transitions between songs in your playlists (You played Busta Rhymes after Metallica? Really?) this app takes in a playlist that you provide and re-orders it, optimizing the transitions between songs.
It does this by constructing a database of music artists using LastFM's related artist API (Artist 1 is related to Artist 2, who is in turn related to Artist 3). The app then calculates the "distance" between two artists on a playlist, and solves an optimization problem to determine the lowest "distance" path between all artists on the playlist, and thus the new "correct" playlist order.
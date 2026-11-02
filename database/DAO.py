from database.DB_connect import DBConnect
from model.Artist import Artist


class DAO():

    @staticmethod
    def getAllArtists():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT art.ArtistId, art.Name
                FROM Artist art
                
                JOIN Album
                ON Album.ArtistId = art.ArtistId
                
                JOIN Track 
                ON Track.AlbumId = Album.AlbumId
                """

        cursor.execute(query)

        for row in cursor:
            results.append(
                Artist(
                row["ArtistId"],
                row["Name"]
                )
            )

        cursor.close()
        conn.close()

        for artist in results:
            artist.Tracks = DAO.getTracksForArtist(artist.ArtistId)
            artist.Playlists = DAO.getPlaylistsForArtist(artist.ArtistId)

        return results

    @staticmethod
    def getTracksForArtist(ArtistId):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT Track.TrackId
        FROM Artist
        JOIN Album
        ON Album.ArtistId = Artist.ArtistId
        JOIN Track
        ON Track.AlbumId = Album.AlbumId
        
        WHERE Artist.ArtistId = %s
        """
        cursor.execute(query, (ArtistId,))
        for row in cursor:
            results.append(row["TrackId"])

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getPlaylistsForArtist(ArtistId):
        conn = DBConnect.get_connection()

        results = set()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DISTINCT PlaylistTrack.PlaylistId
        FROM Artist
        
        JOIN Album
        ON Album.ArtistId = Artist.ArtistId
        
        JOIN Track
        ON Track.AlbumId = Album.AlbumId
        
        JOIN PlaylistTrack
        ON PlaylistTrack.TrackId = Track.TrackId
        
        WHERE Artist.ArtistId = %s
        """
        cursor.execute(query, (ArtistId,))
        for row in cursor:
            results.add(row["PlaylistId"])

        cursor.close()
        conn.close()
        return results




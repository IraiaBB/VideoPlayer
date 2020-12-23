import mysql.connector


class DBconnection:

    def __init__(self):  # at the time of creating an object of this class, the connection with mysql db starts
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="iraia16",
            password="Amapola96!",
            database="music"
        )

    def set_url(self, song_id):  # query to know the song's url

        my_cursor = self.mydb.cursor()
        my_cursor.execute("SELECT url " +
                          "FROM song " +
                          "WHERE id_song = '" + str(song_id) + "' ; ")

        my_result = my_cursor.fetchall()
        url = my_result[0][0]

        return url

    def list_extraction(self):  # all songs list
        my_cursor = self.mydb.cursor()
        my_cursor.execute("SELECT song.title, artist.public_name, song.id_song, artist.id_artist " +
                          "FROM album " +
                          "INNER JOIN song ON album.id_album = song.id_album " +
                          "INNER JOIN artist ON album.id_main_artist = artist.id_artist " +
                          "ORDER BY artist.public_name;")
        my_list = my_cursor.fetchall()

        return my_list

    def song_info(self, song_id):  # extraction of all song's details

        my_text = " "
        my_cursor = self.mydb.cursor()

        # basic info with just one result per column
        my_cursor.execute("SELECT song.title, song.length, album.title, album.releases, record_company.company_name " +
                          "FROM song " +
                          "INNER JOIN album ON song.id_album = album.id_album " +
                          "INNER JOIN record_company ON album.id_record_co = record_company.id_record " +
                          "WHERE song.id_song = " + str(song_id) + ";")

        my_result = my_cursor.fetchall()

        # music style in a new query because it could be 2 or even 3 rows (easily to manage)
        my_cursor.execute("SELECT m.style_name FROM belongs b " +
                          "RIGHT JOIN music_style m ON m.id_style = b.id_style " +
                          "WHERE b.id_song = " + str(song_id) + ";")
        my_result2 = my_cursor.fetchall()

        for item in my_result:  # creating string
            my_text = "Name: " + item[0].replace("*", "'") + "\nLength: " + item[1] + "\nAlbum: " + item[
                2] + "\nRelease year: " + str(item[3]) + "\nRecord company: " + item[4] + "\nMusic style: "

        for num, item in enumerate(my_result2, start=1):  # appending music style
            my_text = my_text + item[0]

            if num != len(my_result2):
                my_text = my_text + ", "  # plus a comma after each one except the end

        return my_text

    def artist_info(self, artist_id):
        my_cursor = self.mydb.cursor()
        # first we have to check whether it's a band or a soloist
        my_cursor.execute("SELECT COUNT(1) " +
                          "FROM individual " +
                          "WHERE id_artist = " + str(artist_id) + ";")

        artist_or_band = my_cursor.fetchall()

        if artist_or_band[0][0] == 1:  # soloist

            my_text = self.soloist(artist_id)

            return my_text

        else:  # band

            my_text = self.band(artist_id)

            return my_text

    def soloist(self, artist_id):  # info extraction if it's a soloist
        my_text = ""
        my_cursor = self.mydb.cursor()

        my_cursor.execute("SELECT artist.public_name, individual.real_name, " +
                          "individual.last_name, individual.birth, coalesce(individual.death, 'Alive'), " +
                          "country.country_name FROM individual " +
                          "INNER JOIN country ON individual.id_country = country.id_country " +
                          "INNER JOIN artist ON individual.id_artist = artist.id_artist " +
                          "WHERE artist.id_artist = " + str(artist_id) + ";")
        solo_info = my_cursor.fetchall()

        for item in solo_info:
            my_text = ("Artist: " + item[0] + "\nReal name: " + item[1] + " " + item[2] +
                       "\nBirth: " + str(item[3]) + "\nDeath: " + str(item[4]) + "\nOrigin: " + item[5])

        return my_text

    def band(self, artist_id):
        my_text = ""
        my_cursor = self.mydb.cursor()

        my_cursor.execute("SELECT artist.public_name, band.creation, coalesce(band.separation, '-') " +
                          "FROM band " +
                          "INNER JOIN artist ON band.id_artist = artist.id_artist " +
                          "WHERE artist.id_artist = " + str(artist_id) + ";")

        band_info = my_cursor.fetchall()

        for item in band_info:
            my_text = ("Band: " + item[0] + "\nCreation: " + str(item[1]) +
                       "\nSeparation: " + str(item[2]) + "\nMembers:\n")

        my_cursor.execute("SELECT a1.public_name, j.incorporation, j.leaves " +
                          "FROM artist a1, artist a2, joined j, individual i, band b " +
                          "WHERE (a1.id_artist = i.id_artist AND i.id_artist = j.id_singer) AND " +
                          "(a2.id_artist = b.id_artist AND b.id_artist = j.id_band) AND " +
                          "a2.id_artist = " + str(artist_id) + ";")

        members = my_cursor.fetchall()

        for num, item in enumerate(members, start=1):
            my_text = my_text + (item[0] + "(" + str(item[1]) + "-" + str(item[2]) + ")  ")

            if num % 2 and num is not len(members):
                my_text = my_text + "\n"

        return my_text

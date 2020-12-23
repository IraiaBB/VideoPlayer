Youtube Video Player

Basic instructions

This is the first version of a project made with Python 3.9. on Pycharm, using MySQL Workbench 8.0. as database server. 

This project is based on the information stored in the database. It is called "music" and stores all the data related 
to a song (artist, band, album, etc.), that is then displayed in the GUI with Tkinter module. One of the most important 
attributes of the song, that adds another functionality, is the Youtube URL. With VLC Python bindings, a Youtube video
can be played directly from the program. For better understanding here's a sketch of the GUI:

   ------------------------------------------------
   |         1.title               |4.crud buttons |
   |-------------------------------|---------------|
   |                               |               |
   |                               |               |
   |          2.info frame         |               |
   |                               |               |
   |                               |               |
   |-------------------------------|  5.song list  |
   |                               |               |  
   |      3.song commands          |               |
   ------------------------------------------------

All the songs stored in the database are shown in the song list (5) with the artist name. Once selected an item of the
list, the information about that song will be displayed in the "info frame" (2). The media will be ready to play from
the song commands (3), below the information. Then it can be paused or stopped. Besides selecting, songs can also be
changed with the arrow shaped commands.

As this first version still can't add or delete songs from the GUI, songs' attributes must be modified directly in the
db, that's why the music database is also included in my Git. It can be used as example without changes needed. The
purpose is to add this functionalities in the next version of the program by using the crud buttons (4) above the song
listbox (5).

And, lastly, it will let change the user name, and maybe an image, in the title (1).
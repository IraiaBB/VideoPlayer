import tkinter as tk
import vlc
import pafy
from PIL import ImageTk, Image

from db import DBconnection


class Main:

    def __init__(self):
        root = tk.Tk()
        root.state("zoomed")  # full screen
        root['background'] = '#2F4F4F'
        root.wm_title("Youtube Jukebox")

        self.db_connection = DBconnection()   # starting DB connection for the queries

        self.index = 1                # initializing class variables
        self.listbox = tk.Listbox()
        self.my_list = []
        self.media = vlc.MediaPlayer()
        self.lbl_song, self.lbl_artist = tk.Label(), tk.Label()
        self.structure(root)

        root.mainloop()

    def structure(self, root):  # window divided in two main blocks (frames)
        # each one is also divided in smaller frames

        left_frame = tk.Frame(root, bg='#2F4F4F')  # divided in : title, info and song commands
        left_frame.pack(side="left", anchor="nw")

        title_frame = tk.Frame(left_frame, bg='#2F4F4F')  # frame the head
        title_frame.pack(side="top", anchor="nw")

        self.title(title_frame)

        info_frame = tk.Frame(left_frame, bg="#DCDCDC", height=300, width=850, borderwidth=5, relief="groove",
                              highlightbackground='#DCDCDC')  # frame info about song and artist
        info_frame.pack(side="top", anchor="center", padx=(50, 30), pady=(30, 30))
        info_frame.pack_propagate(0)  # fixes the frame to it's dimensions, so it's not flexible depending the content

        self.info_box(info_frame)

        song_frame = tk.Frame(left_frame, bg='#2F4F4F')  # frame main options
        song_frame.pack(side="top", pady=(30, 0), anchor="center")

        self.song_commands(song_frame)

        right_frame = tk.Frame(root, bg="#FFA500", borderwidth=5, highlightbackground='#FFA500')
        right_frame.pack(side="right", anchor="ne", fill="y")  # include the CRUD buttons and the listbox

        bd_frame = tk.Frame(right_frame, bg="#FFA500")
        bd_frame.pack(side="top")

        self.crud_buttons(bd_frame, root)
        self.song_listbox(right_frame)

    def title(self, title_frame):
        # user image
        user_img = tk.Canvas(title_frame, width=150, height=150, bg='#2F4F4F', highlightthickness=0)
        img = ImageTk.PhotoImage(Image.open("img/user.png"))
        img = img.PhotoImage__photo.subsample(3)
        user_img.create_image(20, 20, anchor="nw", image=img)
        user_img.image = img
        user_img.pack(side="left", anchor="n")

        # welcome label
        welcome_lbl = tk.Label(title_frame, text="Welcome, user!", fg='#FFA500', bg='#2F4F4F')
        welcome_lbl.configure(font=("Gabriola", 40, "bold"))
        welcome_lbl.pack(side="left", anchor="n", padx=(50, 30), pady=(50, 10))

        # edit button
        img2 = ImageTk.PhotoImage(Image.open("img/edit.png"))
        img2 = img2.PhotoImage__photo.subsample(5)  # smaller image, in this case, in a scale of 5
        edit_btn = tk.Button(title_frame, image=img2, bg='#2F4F4F')
        edit_btn.image = img2  # needed to keep reference to the image, as tk doesn't
        edit_btn.pack(side="left", anchor="n", pady=(30, 0))

    def info_box(self, info_frame): # here is where the song and artist's info is displayed
        # lbl must be a class variable because there's an event outside that changes their text
        self.lbl_song = tk.Label(info_frame, font="Calibri 15", text="Info song", fg='#D2691E', bg='#DCDCDC', justify="left")
        self.lbl_song.pack(side="left", anchor="nw", padx=(0, 5), expand=True, fill="both")
        self.lbl_artist = tk.Label(info_frame, font="Calibri 15", text="Info artist", fg='#D2691E', bg='#DCDCDC', justify="left")
        self.lbl_artist.pack(side="right", anchor="ne", expand=True, fill="both")

    def song_commands(self, song_frame):  # its purpose is playing the song and navigating through the list
        # previous button
        img_prev = ImageTk.PhotoImage(Image.open("img/prev.png"))
        img_prev = img_prev.PhotoImage__photo.subsample(2)
        prev_btn = tk.Button(song_frame, image=img_prev, bg='#2F4F4F', highlightthickness=0, relief="flat",
                             command=lambda: self.change_song(1))
        prev_btn.image = img_prev
        prev_btn.pack(side="left", anchor="center")

        # play button
        img_play = ImageTk.PhotoImage(Image.open("img/play.png"))
        img_play = img_play.PhotoImage__photo.subsample(2)
        play_btn = tk.Button(song_frame, image=img_play, bg='#2F4F4F', command=lambda: self.get_media().play(),
                             highlightthickness=0, relief="flat")
        play_btn.image = img_play
        play_btn.pack(side="left", anchor="center")
        # pause button
        img_pause = ImageTk.PhotoImage(Image.open("img/pause.png"))
        img_pause = img_pause.PhotoImage__photo.subsample(2)
        pause_btn = tk.Button(song_frame, image=img_pause, bg='#2F4F4F', highlightthickness=0, relief="flat",
                              command=lambda: self.get_media().pause())
        pause_btn.image = img_pause
        pause_btn.pack(side="left", anchor="center")
        # stop button
        img_stop = ImageTk.PhotoImage(Image.open("img/stop.png"))
        img_stop = img_stop.PhotoImage__photo.subsample(2)
        stop_btn = tk.Button(song_frame, image=img_stop, bg='#2F4F4F', highlightthickness=0,
                             command=lambda: self.get_media().stop(), relief="flat")
        stop_btn.image = img_stop
        stop_btn.pack(side="left", anchor="center")

        # next button
        img_next = ImageTk.PhotoImage(Image.open("img/next.png"))
        img_next = img_next.PhotoImage__photo.subsample(2)
        next_btn = tk.Button(song_frame, image=img_next, bg='#2F4F4F', highlightthickness=0, relief="flat",
                             command=lambda: self.change_song(2))
        next_btn.image = img_next
        next_btn.pack(side="left", anchor="center")

    def change_song(self, option):  # navigate to the next or previous song
        selected_song = self.listbox.curselection()[0]  # get current song index in the listbox
        self.listbox.select_clear(selected_song)  # clear current selection with the index

        if option == 1:  # previous button (<<) : subtract 1 to index
            selected_song = selected_song - 1
        else:  # next button (>>) : add 1 to index
            selected_song = selected_song + 1

        self.listbox.select_set(selected_song, last=None)  # set selection with new index
        self.listbox.activate(selected_song)
        self.listbox.selection_anchor(selected_song)

        self.listbox.event_generate('<<ListboxSelect>>')  # activate selection event

    def set_media(self, song_id):  # creation of the media with Youtube URL
        url = self.db_connection.set_url(song_id)  # DB query to get the url
        # creating pafy object of the video
        video = pafy.new(url)

        # getting best stream
        best = video.getbest()

        # creating vlc media player object
        self.media = vlc.MediaPlayer(best.url)

    def crud_buttons(self, bd_frame, root):    # in use in the next version
        # bd buttons
        add_btn = tk.Button(bd_frame, text="ADD", highlightthickness=0, height=3, width=10, font="Helvetica 9 bold",
                            fg='#FFA500', bg='#2F4F4F')
        del_btn = tk.Button(bd_frame, text="DELETE", highlightthickness=0, height=3, width=10,
                            font="Helvetica 9 bold", fg='#FFA500', bg='#2F4F4F')
        up_btn = tk.Button(bd_frame, text="UPDATE", highlightthickness=0, height=3, width=10,
                           font="Helvetica 9 bold", fg='#FFA500', bg='#2F4F4F')
        add_btn.pack(side="left")
        del_btn.pack(side="left", pady=(10, 10), padx=(15, 15))
        up_btn.pack(side="left")

    def song_listbox(self, right_frame):  # creation of the listbox and scrollbars

        list_frame = tk.Frame(right_frame, bg="#FFA500")
        list_frame.pack(side="top", fill="both")

        # listbox
        self.listbox = tk.Listbox(list_frame, height=38, width=50, highlightthickness=0, bg='#2F4F4F',
                                  selectmode="single", fg='#FFA500', selectbackground='#D2691E',
                                  exportselection=False)
        self.listbox.pack(side="left", anchor="nw", expand=True)

        v_scrollbar = tk.Scrollbar(list_frame, width=11)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar = tk.Scrollbar(right_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x", anchor="se")

        # event when selecting an item
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.item_selection(event))

        # listbox songs query
        self.fill_listbox()

        # inserting scrollbars around the list
        self.listbox.config(yscrollcommand=v_scrollbar.set)
        v_scrollbar.config(command=self.listbox.yview)
        self.listbox.config(xscrollcommand=h_scrollbar.set)
        h_scrollbar.config(command=self.listbox.xview)

    def fill_listbox(self):
        self.my_list = self.db_connection.list_extraction()
        # list containing: song name, artist name, song id and artist id.

        self.listbox.delete(0, "end")  # clearing listbox, so we can use the method after adding or deleting a song

        for item in self.my_list:  # filling the list only with the song and artist name
            self.listbox.insert("end", item[0].replace("*", "'") + ", " + item[1])
            # in the DB single quotes are replaced by asterisks for avoiding problems with special characters

        self.set_list(self.my_list)  # calling setter so we can use this list's information later

    def item_selection(self, event):
        # with the list's getter, the id's can be extracted easily
        index = self.listbox.curselection()
        my_list = self.get_list()
        my_row = my_list[index[0]]
        song_id, artist_id = my_row[2], my_row[3]

        self.lbl_song = self.get_lbl_song()
        my_text = self.db_connection.song_info(song_id)  # query for song's details
        self.lbl_song.config(text=my_text)  # insert the result in the corresponding lbl
        self.set_lbl_song(self.lbl_song)

        self.lbl_artist = self.get_lbl_artist()
        my_text2 = self.db_connection.artist_info(artist_id)  # query for artist's details
        self.lbl_artist.config(text=my_text2)
        self.set_lbl_artist(self.lbl_artist)

        self.set_media(song_id)

    # -------- setters & getters -------- #

    def get_list(self):
        return self.my_list

    def set_list(self, my_list):
        self.my_list = my_list

    def get_lbl_song(self):
        return self.lbl_song

    def set_lbl_song(self, lbl_song):
        self.lbl_song = lbl_song

    def get_lbl_artist(self):
        return self.lbl_artist

    def set_lbl_artist(self, lbl_artist):
        self.lbl_artist = lbl_artist

    def get_media(self):
        return self.media


m = Main()


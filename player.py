from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Music Player')
root.iconbitmap("D:\CSE 2100\spotify-logo.ico")
root.geometry("700x400")

#initialize pygame mixer
pygame.mixer.init()

#length of song
def play_time():
    #checking for double timing
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() /1000
    # slider_label.config(text=f'Slider:{int(my_slider.get())} and Song Pos: {int(current_time)} ')
    converted_current_time = time.strftime('%M:%S',time.gmtime(current_time))
    #next song from list
    song = music_box.get(ACTIVE)
    song=f'D:/CSE 2100/Musics/{song}.mp3'
    #song length with mutagen
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
    #increase current time by 1 second
    current_time +=1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length} of {converted_song_length}')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        #update slider position
        slider_position = int(song_length)
        my_slider.config(to=slider_position,value=int(current_time))
    else:
        #update slider position
        slider_position = int(song_length)
        my_slider.config(to=slider_position,value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S',time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')

        #move by 1 sec
        next_time = int(my_slider.get())+1
        my_slider.config(value=next_time)

    
    status_bar.after(1000, play_time)

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir="D:/CSE 2100/Musics/",title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace("D:/CSE 2100/Musics/","")
    song = song.replace(".mp3","")
    music_box.insert(END, song)
#adding many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="D:/CSE 2100/Musics/",title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace("D:/CSE 2100/Musics/","")
        song = song.replace(".mp3","")
        music_box.insert(END, song)       
#   play selected song
def play():
    #set stopped variable to false
    global stopped
    stopped = False
    
    song = music_box.get(ACTIVE)
    song=f'D:/CSE 2100/Musics/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #playtime funtion
    play_time()
    
    
global stopped
stopped = False
#stop song
def stop():
    #reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #stop
    pygame.mixer.music.stop()
    music_box.select_clear(ACTIVE)
    status_bar.config(text='')
    #set stop variable true
    global stopped
    stopped = True
#next song
def next_song():
    global paused
    paused = False
    #reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    
    #current song
    next_one = music_box.curselection()
    next_one = next_one[0]+1
    #next song from list
    song = music_box.get(next_one)
    song=f'D:/CSE 2100/Musics/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #moving active bar
    music_box.selection_clear(0,END)
    music_box.activate(next_one)
    music_box.selection_set(next_one,last=None)
#previous song
def previous_song():
    global paused
    paused = False
    #reset slider and status bar
    status_bar.config(text='')
    my_slider.config(value=0)
    #current song
    next_one = music_box.curselection()
    next_one = next_one[0]-1
    #next song from list
    song = music_box.get(next_one)
    song=f'D:/CSE 2100/Musics/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #moving active bar
    music_box.selection_clear(0,END)
    music_box.activate(next_one)
    music_box.selection_set(next_one,last=None)
    
#delete a song   
def delete_song():
    stop()
    music_box.delete(ANCHOR)
    pygame.mixer.music.stop() 
    
#clear playlist
def delete_all_song():
    stop()
    music_box.delete(0,END)
    pygame.mixer.music.stop()
#global pause
global paused
paused = False    
    
#pause song
def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:    
        pygame.mixer.music.pause()
        paused = True

#createing slider
def slide(x):
    song = music_box.get(ACTIVE)
    song=f'D:/CSE 2100/Musics/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

#volume
def volume(x):
    #volume is float; range: 0 - 1;
    pygame.mixer.music.set_volume(volume_slider.get())
    
#create Master frame
master_frame = Frame(root)
master_frame.pack(pady=20) 
 
#creating playlist box
music_box = Listbox(master_frame, bg = "#183D3D", fg="#FAF1E4", width = 100,selectbackground="gray",selectforeground="black")
music_box.grid(row=0, column=0)

#player control button images
back_btn_img= PhotoImage(file="D:/CSE 2100/previous (Custom).png")
forward_btn_img= PhotoImage(file="D:/CSE 2100/next (Custom).png")
play_btn_img= PhotoImage(file="D:/CSE 2100/play (Custom).png")
pause_btn_img= PhotoImage(file="D:/CSE 2100/pause-button (Custom).png")
stop_btn_img= PhotoImage(file="D:/CSE 2100/stop (Custom).png")

#player control frame
control_frame = Frame(master_frame)
control_frame.grid(row=1,column=0,pady=20)

#volume label
volume_frame = LabelFrame(master_frame,text="Volume\n0")
volume_frame.grid(row=0,column=1,padx=20)
#player control buttons
back_btn = Button(control_frame, image=back_btn_img, borderwidth=0,command=previous_song)
forward_btn = Button(control_frame, image=forward_btn_img, borderwidth=0,command=next_song)
play_btn = Button(control_frame, image=play_btn_img, borderwidth=0,command=play)
pause_btn = Button(control_frame, image=pause_btn_img, borderwidth=0,command=lambda: pause(paused))
stop_btn = Button(control_frame, image=stop_btn_img, borderwidth=0,command=stop)

back_btn.grid(row=0, column=0,padx=10)
forward_btn.grid(row=0, column=4,padx=10)
play_btn.grid(row=0, column=1,padx=10)
pause_btn.grid(row=0, column=2,padx=10)
stop_btn.grid(row=0, column=3,padx=10)

#creating menu
my_menu = Menu(root)
root.config(menu=my_menu)

#adding song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add songs", menu = add_song_menu)
#add_song_menu.add_command(label="Add one song to Playlist", command=add_song)

#add many songs
add_song_menu.add_command(label="Add Musics to Playlist", command=add_many_songs)
#delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Musics",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete Selected Music from Playlist",command=delete_song)
remove_song_menu.add_command(label="Clear Playlist",command=delete_all_song)

#create status bar
status_bar = Label(root, text='',bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#slider
my_slider = ttk.Scale(master_frame, from_=0, to=100,orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2,column=0,pady=10)

#volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1,orient=VERTICAL, value=0.5, command=volume, length=125)
volume_slider.pack(pady=10)

root.mainloop()
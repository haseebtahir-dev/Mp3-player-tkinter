from tkinter import *
import pygame
import os
from tkinter import filedialog
from tkinter import END
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from PIL import Image, ImageTk

root = Tk()
style = ttk.Style()
style.theme_use('default')
root.title('PyBeat')
root.geometry('500x400')
icon_folder = 'icons'
icon_file = 'icon.png'
icon_path = os.path.join(icon_folder, icon_file)

icon = PhotoImage(file=icon_path)
root.iconphoto(True, icon)

pygame.mixer.init()

controls_frame = Frame(root)  # Define controls_frame here
controls_frame.pack()

#play time 
def PLayTime():
    if stopped:
        return
    
    current_time = pygame.mixer.music.get_pos() / 1000
    
    # Convert to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    # Get song
    song = song_box.get(ACTIVE)
    song = os.path.join('audio_files', f'{song}.mp3')

    # Load song with mutagen
    song_mut = MP3(song)

    # Get song length
    global song_len
    song_len = song_mut.info.length
    converted_song_len = time.strftime('%M:%S', time.gmtime(song_len))
    
    # Update slider to position
    current_time += 1
    if int(music_slider.get()) == int(song_len):
        status_bar.config(text = f'Time Elapsed:{converted_song_len}')
    elif paused:
        pass
    elif int(music_slider.get()) == int(current_time):
        slider_position = int(song_len)
        music_slider.config(to=slider_position,value=int(current_time))
    else:
        slider_position = int(song_len)
        music_slider.config(to=slider_position,value=int(music_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(music_slider.get())))
        status_bar.config(text = f'Time Elapsed: {converted_current_time} of {converted_song_len}  ')
        next_time = int(music_slider.get()) + 1
        music_slider.config(value=next_time)
    
    # Call PlayTime function after (1 second)
    root.after(1000, PLayTime) 


#add song
def AddSong():
    
    song_path = filedialog.askopenfilename(initialdir='audio_file/', title='Choose a Song', filetypes=(('mp3 Files', '*.mp3'),))
    song_name = os.path.splitext(os.path.basename(song_path))[0]
    song_box.insert(END, song_name)

#addmanysong
def AddManySong():

    songs_paths = filedialog.askopenfilenames(initialdir='audio_file/', title='Choose Songs', filetypes=(('mp3 Files', '*.mp3'),))
    for song_path in songs_paths:
        song_name = os.path.splitext(os.path.basename(song_path))[0]
        song_box.insert(END, song_name)

#update playbutton image 
def update_play_button_image():
    global play_btn_img_normal, pause_btn_img, pause_btn_img_highlighted_tk
    if pygame.mixer.music.get_busy() and not paused:
        play_btn.config(image=pause_btn_img_highlighted_tk)
    else:
        play_btn.config(image=play_btn_img)

# Update pause button image
def update_pause_button_image():
    global play_btn_img_normal, pause_btn_img_highlighted_tk, pause_btn_img_highlighted_tk
    if pygame.mixer.music.get_busy() and paused:
        pause_btn.config(image=pause_btn_img_highlighted_tk)
    else:
        pause_btn.config(image=pause_btn_img)

#playing song
def PlaySong():
    global stopped, paused
    stopped = False
    if song_box.curselection():
        selected_song_index = song_box.curselection()[0]
        selected_song_name = song_box.get(selected_song_index)
        song_path = os.path.join('audio_files', f'{selected_song_name}.mp3')

        if not pygame.mixer.music.get_busy() or paused:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(loops=0)
            PLayTime()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True
        update_play_button_image()  
        update_pause_button_image() 
    else:
        print("Please select a song to play.")

#stop playing song
global stopped
stopped = False
def Stop():
    #rest slider bar and status bar
    status_bar.config(text=' ')
    music_slider.config(value=0)
     
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    #clear status bar
    status_bar.config(text=' ')

    global stopped
    stopped = True
    play_btn.config(image=play_btn_img_normal)
    pause_btn.config(image=pause_btn_img_normal_tk)

#next song
def NextSong():
    status_bar.config(text=' ')
    music_slider.config(value=0)
    next_index = (song_box.curselection()[0] + 1) % song_box.size()
    selected_song_name = song_box.get(next_index)
    song_path = os.path.join('audio_files', f'{selected_song_name}.mp3')
    
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)
   
    song_box.selection_clear(0, END)
    song_box.selection_set(next_index)
    song_box.activate(next_index)

#previous song
def PreviousSong():
    status_bar.config(text=' ')
    music_slider.config(value=0)
    next_index = (song_box.curselection()[0] - 1) % song_box.size()
    selected_song_name = song_box.get(next_index)
    song_path = os.path.join('audio_files', f'{selected_song_name}.mp3')
    
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)
   
    song_box.selection_clear(0, END)
    song_box.selection_set(next_index)
    song_box.activate(next_index)

#delete one song
def DeleteSong():
    Stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#delete all song
def DeleteAllSong():
    Stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()

#pause 
global paused
paused = False

def Pause(x):
    global paused
    if pygame.mixer.music.get_busy():
        if paused:
            pygame.mixer.music.unpause()
            paused = False
        else:
            pygame.mixer.music.pause()
            paused = True
        update_play_button_image()  
        update_pause_button_image() 

#slider function
def Slide(x):
    selected_song_index_tuple = song_box.curselection()
    if selected_song_index_tuple: 
        selected_song_index = selected_song_index_tuple[0]
        selected_song_name = song_box.get(selected_song_index)
        song_path = os.path.join('audio_files', f'{selected_song_name}.mp3')
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0, start=int(music_slider.get()))

#volume function
def volume(x):
    volume_level = volume_slider.get()
    pygame.mixer.music.set_volume(volume_level)

master_frame = Frame(root)
master_frame.pack(pady=20)

#create playlist
song_box = Listbox(master_frame,bg='#000000',fg='#00FFFF',width=60,selectbackground='#008080',selectforeground='#FFFFFF', bd=2, relief="solid")
song_box.grid(row=0,column=0)

#player control button image 
back_btn_img = PhotoImage(file='icons/icons8-back-48.png')
forward_btn_img = PhotoImage(file='icons/icons8-forward-48.png')
play_btn_img = PhotoImage(file='icons/icons8-play-48.png')
pause_btn_img = PhotoImage(file='icons/icons8-pause-48.png')
stop_btn_img = PhotoImage(file='icons/icons8-stop-48.png')
play_btn_img_highlighted_tk = PhotoImage(file='icons/icons8-play-button-48 green.png')
play_btn_img_normal = PhotoImage(file='icons/icons8-play-48.png')
pause_btn_img_highlighted_tk = PhotoImage(file='icons/icons8-pause- color.png')
pause_btn_img_normal_tk = PhotoImage(file='icons/icons8-pause-48.png')


controls_frame = Frame(master_frame)
controls_frame.grid(row=1,column=0,pady=20)

# Volume Label Frame
volume_frame = LabelFrame(master_frame, text="")
volume_frame.grid(row=0, column=1, padx=30)

#player control buttons
back_btn = Button(controls_frame, image=back_btn_img, borderwidth=0, command=PreviousSong, width=40)
forward_btn = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=NextSong, width=40)
play_btn = Button(controls_frame, image=play_btn_img, borderwidth=0, command=PlaySong, width=40)
pause_btn = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda:Pause(paused), width=40)
stop_btn = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=Stop, width=40)

back_btn.grid(row=0,column=0,padx=32)
forward_btn.grid(row=0,column=1,padx=32)
play_btn.grid(row=0,column=2,padx=32)
stop_btn.grid(row=0,column=4,padx=32)

#create a menu bar
my_menu = Menu(master_frame)
root.config(menu=my_menu)

#add song
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Add Songs', menu=add_song_menu, font=('Helvetica', 10, 'bold'), foreground='#FFFFFF', background='#333333')

# Add One Song to Playlist
add_song_menu.add_command(label='Add One Song to Playlist', command=AddSong, font=('Helvetica', 10), foreground='#000000', background='#CCCCCC')

# Add Many Songs to Playlist
add_song_menu.add_command(label='Add Many Songs to Playlist', command=AddManySong, font=('Helvetica', 10), foreground='#000000', background='#CCCCCC')

# Remove Songs menu
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label='Remove Songs', menu=remove_song_menu, font=('Helvetica', 10, 'bold'), foreground='#FFFFFF', background='#333333')

# Delete A Song from Playlist
remove_song_menu.add_command(label='Delete A Song from Playlist', command=DeleteSong, font=('Helvetica', 10), foreground='#000000', background='#CCCCCC')

# Delete All Songs from Playlist
remove_song_menu.add_command(label='Delete All Songs from Playlist', command=DeleteAllSong, font=('Helvetica', 10), foreground='#000000', background='#CCCCCC')

#status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E, bg='#333333', fg='#FFFFFF')
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create slider
style.configure("Music.Horizontal.TScale", troughcolor='#000000', sliderlength=20, sliderthickness=10, background='#008080', foreground='#FFFFFF')
music_slider = ttk.Scale(master_frame, from_=0, to=100, orient='horizontal', value=0, length=360, style="Music.Horizontal.TScale", command=Slide)
music_slider.grid(row=2,column=0, pady=20)

# Create Volume Slider
style.configure("Volume.Vertical.TScale", troughcolor='#666666', sliderlength=20, sliderthickness=8, background='#000000', foreground='#FFD700')
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient='vertical', value=1, command=volume, length=130, style="Volume.Vertical.TScale")
volume_slider.pack(pady=10)

root.mainloop()
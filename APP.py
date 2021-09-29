# Application to develop pitch recognition
import os                                                           # Used to change directories for different file locations
import tkinter as tk                                                # Graphic user interface (GUI)
import random                                                       # Used to generate random numbers
import winsound as w                                                # Can only play sounds from 37Hz to 32,767Hz(whole numbers)
import scipy as sp                                                  # Imports scipy science things
import scipy.io.wavfile                                             # This allows scipy to read in a WAV audio file as numpy arrays
import numpy as np                                                  # Imports numpy to do math things 
import sounddevice as sd                                            # Allows wav files to be played
import time as t                                                    # This will be used to control the time before another command
import threading as th

desktop = 'C:\\Users\\Administrator\\Desktop'
admin = 'C:\\Users\\Administrator'

#Define notes in dictionary, starts in first octave except for A#(starting in 0)
Dict = { 
         1:[55,110,220,440,880,1760,3520],                            # A
         2:[58.2705,116.541,233.082,466.164,932.328,1864.66,3729.31], # A sharp or B flat
         3:[61.7354,123.471,246.942,493.883,987.767,1975.53,3951.07], # B 
         4:[32.7032,65.4064,130.813,261.626,523.251,1046.50,2093.00], # C
         5:[34.6478,69.2957,138.591,277.183,554.365,1108.73,2217.46], # C sharp or D flat
         6:[36.7081,73.4162,146.832,293.665,587.330,1174.66,2349.32], # D 
         7:[38.8909,77.7817,155.563,311.127,622.254,1244.51,2489.02], # D sharp or E flat
         8:[41.2034,82.4069,164.814,329.628,659.255,1318.51,2637.02], # E
         9:[43.6535,87.3071,174.614,349.228,698.456,1396.91,2793.83], # F 
        10:[46.2493,92.4986,184.997,369.994,739.989,1479.98,2959.96], # F sharp or G flat
        11:[48.9994,97.9989,195.998,391.995,783.991,1567.98,3135.96], # G
        12:[51.9131,103.826,207.652,415.305,830.609,1661.22,3322.44]  # G sharp or A flat
       }

# Import the audio file for the secific note you want
os.chdir(desktop + '\\ClassicalWav')
rate, C = scipy.io.wavfile.read("K545.wav")  
rate, DB = scipy.io.wavfile.read("NocturneC#.wav")
rate, D = scipy.io.wavfile.read("MinuetG.wav")
rate, EB = scipy.io.wavfile.read("LaCampanella.wav")
rate, E = scipy.io.wavfile.read("FurElise.wav")
rate, F = scipy.io.wavfile.read("onepunch.wav")
rate, GB = scipy.io.wavfile.read("riyuu.wav")
os.chdir(admin)
rate, G = scipy.io.wavfile.read("EineKlein.wav")
rate, AB = scipy.io.wavfile.read("MinuteWaltz.wav")
rate, A = scipy.io.wavfile.read("FairyFountain.wav")
rate, BB = scipy.io.wavfile.read("GrandeValse.wav")
rate, B = scipy.io.wavfile.read("Rage1.wav")

window = tk.Tk()                                                           # Creates window
window.title("Acquired Perfect Pitch")                                     # Set window title
heading = tk.Label(window, text="APP",font=('Comic Sans MS' , 40, 'bold'), fg = 'BLACK').pack() # Adds a title to the content within the window
user_prompt = tk.Label(window, text="What note is this? ", font=('Comic Sans MS' , 19, 'bold'), fg = 'BLACK').place(x=15,y=197) # Question box
note_help = tk.Label(window, text="Sharp/Flat notes must be entered with the flat name, F# = Gb", font=('Comic Sans MS' , 10, 'underline'), fg = 'Purple').place(x=250,y=150) # Tip box
window.geometry("700x650+0+0")                                             # Set window dimensions and starting point (0+0 is the top left) 

note = tk.StringVar()                                                      # Gets a string
entry_space = tk.Entry(window, textvariable = note, width = 25, bg = 'white').place(x=328,y=210) # Creates a box for a user input            

Notename = ['A','BB','B','C','DB','D','EB','E','F','GB','G','AB'] # Random integer a also chooses the notename. (notename = notename[a-1])
cmsg = "" #Message for when submission is correct
imsg = "" #Message for when submission is incorrect
current_song = "" #Message to display current song in the music library

a = 0                                           # Stores value of randomizer for lettername of pitch
freq = 0                                        # Stores value of frequency of pitch
correct = 0                                     # Store amount of guesses that are correct
wrong   = 0                                     # Store amount of guesses that are incorrect  
submits = 0                                     # Used to stop user from submitting correct answer multiple times
def play_note():
    global a, freq, submits, imsg, current_song, cmsg                         # Allows us to update a global variable
    cleartext()
    a = random.randint(1,12)                        # This chooses the letter name of the pitch
    b = random.randint(3,6)                         # This chooses the frequency of the pitch (headphones(1,6),no headphones(3,6))
    freq = round(Dict[a][b])                        # Chooses the specific frequency to pass into winsound
    w.Beep(freq,1000)                               # This plays the randomly chosen frequency for some duration of time
    window.update()
    submits = 0
    
def replay():
    global imsg, current_song, cmsg
    try:
        w.Beep(freq,1000)                           # Plays a sound at certain frequency
    except ValueError:
        cleartext()
        error = tk.Label(window, text='How can you replay nothing!', font=('ariel' , 19, 'bold'), fg = 'RED').place(x=20,y=550)
        window.update()
    
def score():
        global correct, wrong, imsg, current_song, cmsg       # Allows access to edit global variable
        entry_space = tk.Entry(window, textvariable = note, width = 25, bg = 'white').place(x=328,y=210) # Creates a box for a user input     
        try:
            cleartext()
            Final = tk.Label(window, text='You got ' + str(float(correct/(correct+wrong))*100) + '% right answering ' + str(correct+wrong) + ' questions!', font=('ariel' , 19, 'bold'), fg = 'RED').place(x=20,y=550)
            window.update()
        except ZeroDivisionError:
            cleartext()
            error = tk.Label(window, text='How about you answer a question first!', font=('ariel' , 19, 'bold'), fg = 'RED').place(x=20,y=550)
            window.update()
def stop():
    sd.stop()                # Stops playing sound
    
# List of song names    
song_bank = ['Sonata number 16, Mozart','Nocturne in C# minor, Chopin','Minuet in G major, Bach','La Campanella, Franz Liszt','Fur Elise, Beethoven','The Hero, Jam Project',
                'Yasashisa no riyuu, ChouCho','Eine klein Nacht Musik, Mozart','Minute Waltz, Chopin',"Great Fairy Fountain, Legend of Zelda","Grande Valse Brilliante, Chopin",
                'Rondo a Capriccio, Beethoven'] 

s = 1                        # stores values for the song bank title
        
def show_library():
    global current_song, imsg, current_song, cmsg
    newwindow = tk.Tk()                                                           # Creates window
    newwindow.title("Welcome to the Library")                                     # Set window title
    heading = tk.Label(newwindow, text="Music Library",font=('ariel' , 40, 'bold'), fg = 'Green').pack() # Adds a title to the content within the window
    label = tk.Label(newwindow, text="Current Song, Composer:", font=('ariel' , 25, 'bold'), fg = 'Purple')
    label.place(x=20,y=210)
    window.geometry("600x600+0+0")           # Set window dimensions and starting point (0+0 is the top left)  
        
    def play_song(): 
        global s, current_song, imsg, cmsg
        if s == 1: 
            sd.play(C)
            song = song_bank[s-1]          
            cleartext()
            current_song = tk.Label(newwindow, text=song, font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 2: 
            sd.play(DB)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song, font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 3:
            sd.play(D)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 4:
            sd.play(EB)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 5: 
            sd.play(E)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 6: 
            sd.play(F,48000)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 7: 
            sd.play(GB,48000)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 8:
            sd.play(G)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 9:
            sd.play(AB,48000)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 10: 
            sd.play(A)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 11:
            sd.play(BB)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s == 12:
            sd.play(B)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s > 12: 
            s=1
            sd.play(C)
            song = song_bank[s-1]                                                                                       # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        elif s < 1: 
            s=12  
            sd.play(B)
            song = song_bank[s-1]                # Gets song from the song bank based on indice of s
            cleartext()
            current_song = tk.Label(newwindow, text=song , font = ('ariel',25,'bold'), fg = 'Purple')
            current_song.place(x=470,y=210)            # Displays current song message
            s+=1
        window.update()
        
    def play_previous():
        global s, imsg, cmsg, current_song       # Allows access to edit global variable
        cleartext()
        s-=2                                     # s = s-2
        play_song()                              # Codemasters defined function
    
    def exit():
        newwindow.destroy()                      # Destroys window
        
    # Create buttons that user can click taht also sets off a certain command or action
    Play_n = tk.Button(newwindow, text='Play Next',width=20, height=5, bg='Yellow', command = play_song).place(x=500,y=350)
    Stop = tk.Button(newwindow, text='Stop Song',width=20, height=5, bg='Yellow', command = stop).place(x=665,y=350)
    Play_p = tk.Button(newwindow, text='Play Previous',width=20, height=5, bg='Yellow', command = play_previous).place(x=500,y=450)
    Play_n = tk.Button(newwindow, text='Exit',width=20, height=5, bg='Yellow', command = exit).place(x=665,y=450)

def do_it():           
    global wrong, correct, submits, imsg, current_song, cmsg                  # Allows access to edit a global variable
    Guessed = note.get()                            # Gets whatever the user typed in the entry box
    if submits == 0:
        if Guessed.upper() == Notename[a-1]:            # If correct adds a point to the correct points
            cleartext()
            cmsg = tk.Label(window, text='This is correct, keep on going!  :)', font=('ariel' , 19, 'bold'), fg = 'Green')
            cmsg.place(x=20,y=550)
            correct += 1
            entry_space = tk.Entry(window, textvariable = note, width = 25, bg = 'LightGreen').place(x=328,y=210) # Creates a box for a user input            
            window.update()

        if Guessed.upper() != Notename[a-1]:                # If incorrect adds a point to the incorrect points 
            wrong += 1
            entry_space = tk.Entry(window, textvariable = note, width = 25, bg = 'red').place(x=328,y=210) # Creates a box for a user input            
            if Notename[a-1] == "C":
                cleartext()
                imsg = tk.Label(window, text='~That note was C, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(C,44100) # Plays the audio for C note
                t.sleep(6)       # Waits a specified amount of time before executing the next line of code
                sd.stop()        # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "DB":
                cleartext()
                imsg = tk.Label(window, text='~That note was Db, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(DB,44100) # Plays the audio for DB note
                t.sleep(9)        # Waits a specified amount of time before executing the next line of code
                sd.stop()         # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "D":
                cleartext()
                imsg = tk.Label(window, text='~That note was D, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(D,44100) # Plays the audio for D note
                t.sleep(3)       # Waits a specified amount of time before executing the next line of code
                sd.stop()        # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "EB": 
                cleartext()
                imsg = tk.Label(window, text='~That note was Eb, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(EB,44100) # Plays the audio for EB note
                t.sleep(16)       # Waits a specified amount of time before executing the next line of code
                sd.stop()         # Stops wav file from playing 
                window.update()
            elif Notename[a-1] == "E":
                cleartext()
                imsg = tk.Label(window, text='~That note was E, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(E,44100) # Plays the audio for E note
                t.sleep(7)       # Waits a specified amount of time before executing the next line of code
                sd.stop()        # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "F":
                cleartext()
                imsg = tk.Label(window, text='~That note was F, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(F,48000)  # Plays the audio for F note
                t.sleep(10)       # Waits a specified amount of time before executing the next line of code
                sd.stop()         # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "GB":
                cleartext()
                imsg = tk.Label(window, text='~That note was Gb, Sing tihs tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(GB,48000) # Plays the audio for GB note
                t.sleep(6)        # Waits a specified amount of time before executing the next line of code
                sd.stop()         # Stops wav file from playing 
                window.update()
            elif Notename[a-1] == "G":
                cleartext()
                imsg = tk.Label(window, text='~That note was G, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(G,44100) # Plays the audio for G note
                t.sleep(6)       # Waits a specified amount of time before executing the next line of code
                sd.stop()        # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "AB":
                cleartext()
                imsg = tk.Label(window, text='~That note was Ab, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(AB,48000) # Plays the audio for AB note
                t.sleep(4)        # Waits a specified amount of time before executing the next line of code
                sd.stop()         # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "A":
                cleartext()
                imsg = tk.Label(window, text='~That note was A, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(A,44100) # Plays the audio for A note
                t.sleep(6)       # Waits a specified amount of time before executing the next line of code
                sd.stop()        # Stops wav file from playing
                window.update()
            elif Notename[a-1] == "BB":
                cleartext()
                imsg = tk.Label(window, text='~That note was Bb, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(BB,44100) # Plays the audio for BB note
                t.sleep(8)        # Waits a specified amount of time before executing the next line of code
                sd.stop()         # Stops wav file from playing 
                window.update()
            elif Notename[a-1] == "B":
                cleartext()
                imsg = tk.Label(window, text='~That note was B, Sing this tune to remember~', font=('ariel' , 19, 'bold'), fg = 'RED')
                imsg.place(x=20,y=550)
                sd.play(B,44100) # Plays the audio for B note
                t.sleep(5.5)     # Waits a specified amount of time before executing the next line of code
                sd.stop()        # Stops wav file from playing 
                window.update()
            else: none
        submits+=1
        show_correct()
        window.update()
        
def cleartext():
    global imsg, current_song, cmsg
    try:
        imsg.destroy()
        current_song.destroy()
        cmsg.destroy()
    except:
        print("couldn't destroy")
        pass
    window.update()       
    
def refresh():
    global correct, wrong, imsg, current_song, cmsg     # Allows access to edit a global variable
    cleartext()
    correct = 0              # Defines variable to be reset (aka zeroed)
    wrong = 0                # Defines variable to be reset (aka zeroed)
    show_correct()
    
def show_correct():
    global correct, imsg, current_song, cmsg
    cleartext()
    showit = tk.Label(window, text ='Correct: ' + str(correct), font=('Comic Sans MS' , 15, 'bold'), fg = 'green')
    showit.place(x=500,y=200) # Show correct only to keep them motivated
    window.update()        
    
# Creates buttons that the user can click and then a command or action is done (action can also equal None, which would do... Nothing)
submit = tk.Button(window, text='Submit Guess',width=20, height=5, bg='LightBlue', command = do_it).place(x=250,y=350)    # Creates a button that can complete an action when clicked
listen = tk.Button(window, text='Play Note',width=20, height=5, bg='LightBlue', command = play_note).place(x=250,y=250)    # Creates a button that can complete an action when clicked
replay = tk.Button(window, text='Replay',width=20, height=5, bg='LightBlue', command = replay).place(x=415,y=250)    # Creates a button that can complete an action when clicked
exit = tk.Button(window, text='Score',width=20, height=5, bg='LightBlue', command = score).place(x=415,y=350)    # Creates a button that can complete an action when clicked
Library = tk.Button(window, text='Music Library',width=20, height=5, bg='LightBlue', command = show_library).place(x=250,y=450)  # Creates a button that opens up the music library
Refresh = tk.Button(window, text='Refresh Score',width=20, height=5, bg='LightBlue', command = refresh).place(x=415,y=450)  # Creates a button that refreshes the score 

window.update()
window.mainloop()               # This actually shows the window and all updates

import urllib.request #Used to request url access

import numpy.random.mtrand
from bs4 import BeautifulSoup # used for html parsing
import tkinter as tk #Build in a window
import pykakasi #translating from kanji to hiragana
import numpy as np #math such as random numbers
import ssl #Used for certificate to get into website

#Goal: Get random kanji(漢字) from a site, find example sentences and pronunciation help(furigana)

#Level refers to the JLPT levels of N5->N1
level = "N5"
def change_level_n5():
    global level
    level = "N5"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.grid(row = 0, column = 0)
    window.update()

def change_level_n4():
    global level
    level = "N4"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.grid(row = 0, column = 0)
    window.update()

def change_level_n3():
    global level
    level = "N3"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.grid(row = 0, column = 0)
    window.update()

def change_level_n2():
    global level
    level = "N2"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.grid(row = 0, column = 0)
    window.update()

def change_level_n1():
    global level
    level = "N1"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.grid(row = 0, column = 0)
    window.update()



def get_kanji():
    global jp_click_value, en_click_value, place_kanji, place_kunyomi, place_meaning, place_hiragana, place_sentence1, place_onyomi, sentence1, sentence2, place_sentence2, kanji_str
    clear_text()
    en_click_value = 0
    jp_click_value = 0
    url = 'https://kanji.fm4dd.com/kanji-random.php?type=JLPT&level=' + level

    request = urllib.request.Request(url)
    content = urllib.request.urlopen(request, context=ssl._create_unverified_context())

    parse = BeautifulSoup(content, 'html.parser')

    kanji = parse.find_all('td', attrs = {'class' : 'kanji'})
    meaning = parse.find(attrs = {'class' : 'description'})
    kunyomi = meaning.find_next_sibling()
    onyomi = kunyomi.find_next_sibling()

    kanji_str = str(kanji)[19]

    meaning_str = str(meaning)
    kunyomi_str = str(kunyomi)
    onyomi_str = str(onyomi)
    sentence1 = ""
    sentence2 = ""

    parsed_meaning = meaning_str[ meaning_str.find("\">")+1 : meaning_str.find("</") ].replace('>', "")
    parsed_kunyomi = kunyomi_str[ kunyomi_str.find("\">")+1 : kunyomi_str.find("</") ].replace('>', "")
    parsed_onyomi = onyomi_str[ onyomi_str.find("\">")+1 : onyomi_str.find("</") ].replace('>', "")

    place_kanji = tk.Label(window, text = kanji_str, font=('ariel', 30), fg = 'maroon2', bg = "black")
    place_kanji.grid(row = 1, column = 1, columnspan = 5)
    place_meaning = tk.Label(window, text = parsed_meaning, font=('ariel', 10, 'bold'), fg = 'green', bg = "black")
    place_meaning.grid(row = 2, column = 1, columnspan = 5)
    place_kunyomi = tk.Label(window, text = parsed_kunyomi, font=('ariel', 10), fg = 'green', bg = "black")
    place_kunyomi.grid(row = 3, column = 1, columnspan = 5)
    place_onyomi = tk.Label(window, text = parsed_onyomi, font=('ariel', 10), fg = 'green', bg = "black")
    place_onyomi.grid(row = 4, column = 1, columnspan = 5)

    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.grid(row = 0, column = 0)
    window.update()

def example_sentence():
    #Go to website where we will get sentences for certain kanji
    global place_kanji, place_kunyomi, place_meaning, place_hiragana, place_sentence1, place_onyomi, sentence2, place_sentence2, kanji_str, sentence1, jp_click_value, en_click_value
    #users can be found by right click->Inspect element on the page->Network: look under Headers
    try:
        place_sentence1.destroy()
        place_sentence2.destroy()
        place_hiragana.destroy()
    except:
        pass
    jp_click_value = 0
    en_click_value = 0

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    #user_agent = 'https://partner.googleadservices.com/gampad/cookie.js?domain=www.tanoshiijapanese.com&callback=_gfp_s_&client=ca-pub-9013233654782665&cookie=ID%3D462e2fed85d9353f-22af4cecb5ba00ba%3AT%3D1628815954%3ART%3D1628815954%3AS%3DALNI_MZoaM4GhA_FujDYqDzkedca0GiCeQ'
    url = "https://www.tanoshiijapanese.com/dictionary/sentences.cfm?j=" + urllib.parse.quote(kanji_str, safe = '')
    headers={'User-Agent':user_agent}

    request = urllib.request.Request(url,None,headers) #The assembled request, parameters if headers needed(url,None,headers)
    response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
    content = response.read().decode("utf-8")

    parse = BeautifulSoup(content, 'html.parser')

    class_sm = parse.find_all("div", attrs = {"class" : 'sm'})
    #print(class_sm)

    #Choose a random example sentence, could always add more or less variation by changing numbers, pattern with options is just n+3
    options = [1,4,7,10,13,16]
    randomizer = numpy.random.mtrand.randint(0,6)
    chosen = options[randomizer]

    try:
        sentence1 = str(class_sm[chosen])
        sentence2 = str(class_sm[chosen])
        sentence1 = sentence1[sentence1.find("p\">") + 3: sentence1.find("</div>")]
        sentence2 = sentence2[sentence2.find("en\">") + 4: sentence2.find(".</div>")].replace("</div>","").replace("</div", "")

    except:
        sentence1 = "例文が見つかりません、ごめんね。"
        sentence2 = "No example sentences found!"

    #Make necessary elements appear in a window
    place_sentence1 = tk.Label(window, text = sentence1, font=('ariel', 11), fg = 'pink', bg = "black")
    place_sentence1.grid(row = 10, column = 1, columnspan = 5)
    window.update()

def clear_text():
    global place_kanji, place_kunyomi, place_meaning, place_hiragana, place_sentence1, place_onyomi, sentence2, place_sentence2
    try:
        place_kanji.destroy()
        place_meaning.destroy()
        place_kunyomi.destroy()
        place_onyomi.destroy()
        place_sentence1.destroy()
        place_hiragana.destroy()
        place_sentence2.destroy()
    except:
        pass
    window.update()

#code to translate text to hiragana
def translate_hiragana():
    global jp_click_value, sentence1, kanji_str, parsed_meaning, parsed_kunyomi, parsed_onyomi, place_hiragana, sentence2, place_sentence2
    hiragana = ''
    if jp_click_value == 0:
        translate = pykakasi.kakasi()
        result = translate.convert(sentence1)
        for iter in result:
            for key in iter:
                if key == 'hira':
                    hiragana += iter[key]
        place_hiragana = tk.Label(window, text = hiragana, font=('ariel', 11), fg='aquamarine', bg='black')
        place_hiragana.grid(row = 9, column = 1, columnspan = 5)
        jp_click_value+=1
        window.update()

def translate_english():
    global en_click_value, sentence1, kanji_str, parsed_meaning, parsed_kunyomi, parsed_onyomi, place_hiragana, sentence2, place_sentence2
    if en_click_value == 0:
        place_sentence2 = tk.Label(window, text=sentence2, font=('ariel', 11), fg='aquamarine', bg="black", height= 2)
        place_sentence2.grid(row = 8, column = 1, columnspan = 5)
        en_click_value += 1
        window.update()

def search_any():
    global place_kanji, place_kunyomi, place_meaning, place_hiragana, place_sentence1, place_onyomi, sentence2, place_sentence2, kanji_str, sentence1, jp_click_value, en_click_value
    # users can be found by right click->Inspect element on the page->Network: look under Headers

    clear_text()
    jp_click_value = 0
    en_click_value = 0
    try:
        kanji_str = entry.get()
    except: 
        print("Invalid Entry")

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "https://www.tanoshiijapanese.com/dictionary/sentences.cfm?j=" + urllib.parse.quote(kanji_str, safe='') + "&search=Search+>"
    headers = {'User-Agent': user_agent}

    request = urllib.request.Request(url, None, headers)  # The assembled request, parameters if headers needed(url,None,headers)
    response = urllib.request.urlopen(request, context=ssl._create_unverified_context())
    content = response.read().decode("utf-8")

    parse = BeautifulSoup(content, 'html.parser')

    class_sm = parse.find_all("div", attrs={"class": 'sm'})
    # print(class_sm)

    # Choose a random example sentence, could always add more or less variation by changing numbers, pattern with options is just n+3
    options = [1, 4, 7, 10, 13, 16]
    randomizer = numpy.random.mtrand.randint(0, 6)
    chosen = options[randomizer]

    # Make necessary elements appear in a window
    place_kanji = tk.Label(window, text=kanji_str, font=('ariel', 30), fg='maroon2', bg="black")
    place_kanji.grid(row = 1, column = 1, columnspan = 5)
    window.update()
  
window = tk.Tk()
window.configure(bg = 'black')
window.geometry("400x400")

tk.Grid.columnconfigure(window, index=3, weight = 1)
tk.Grid.rowconfigure(window, index=3, weight = 1)

entry = tk.StringVar()
kanji_str = ""
sentence1 = ""
sentence2 = ""
place_sentence2 = ""
place_sentence1 = ""
place_hiragana = ""
place_meaning, place_kunyomi, place_kanji = "", "", ""
place_onyomi = ""
en_click_value = 0
jp_click_value = 0

place_meaning_title = tk.Label(window, text="意味:", font=('ariel', 10, 'bold'), fg='green', bg="black").grid(row = 2, column = 0)
place_kunyomi_title = tk.Label(window, text="訓読み:", font=('ariel', 10), fg='green', bg="black").grid(row = 3, column = 0)
place_onyomi_title = tk.Label(window, text="音読み:", font=('ariel', 10), fg='green', bg="black").grid(row = 4, column = 0)

get_kanji_button = tk.Button(window, text="New", command=get_kanji, bg='black', fg='pink', width = 8, height = 1).grid(row = 12, column = 0)
example_sentence_button = tk.Button(window, text="Example", command=example_sentence, bg='black', fg='pink', width = 8, height = 1).grid(row = 12, column = 1)
hiragana_button = tk.Button(window, text="Hiragana", command=translate_hiragana, bg='black', fg="pink", width = 8, height = 1).grid(row = 12, column = 2)
english_button = tk.Button(window, text="English", command=translate_english, bg='black', fg="pink", width = 8, height = 1).grid(row = 12, column = 3)

n5_button = tk.Button(window, text="N5", command=change_level_n5, bg='black', fg='pink').grid(row = 0, column = 1)
n4_button = tk.Button(window, text="N4", command=change_level_n4, bg='black', fg='pink').grid(row = 0, column = 2)
n3_button = tk.Button(window, text="N3", command=change_level_n3, bg='black', fg='pink').grid(row = 0, column = 3)
n2_button = tk.Button(window, text="N2", command=change_level_n2, bg='black', fg='pink').grid(row = 0, column = 4)
n1_button = tk.Button(window, text="N1", command=change_level_n1, bg='black', fg='pink').grid(row = 0, column = 5)

submit_entry_button = tk.Button(window, text="submit", height= 1,command=search_any, bg='grey', fg='white').grid(row = 12, column = 4)
entry_space = tk.Entry(window, textvariable = entry, width=15, bg="grey", fg="white").grid(row = 12, column = 5)

window.mainloop()

### Tasks
#fix getting the same example sentence in a row
#Title screen? (maybe)
#Add meaning for words entered into text boxes, use dictionary that will tell possible meanings if only hiragana is entered

#####History
#was able to get kanji and put it in a file
#Trouble when grabbing last line of file
#switched to putting kanji in tkinter
#url was having encoding issues when searching a url with kanji in it
#got encoding working and used headers to access sites
#fixed buttons distance, can now get multiple example sentences for same kanji, updated the way that sentences are extracted
#added a universal search so people can study not only kanji but words or phrases they want
#Converted to grid method and made it so that as window expands widgets dynamically expand as well

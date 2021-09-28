import urllib.request #Used to request url access

import numpy.random.mtrand
from bs4 import BeautifulSoup # used for html parsing
import tkinter as tk #Build in a window
import pykakasi #translating from kanji to hiragana
import numpy as np #math such as random numbers
import certifi
import ssl

#Goal: Get random kanji(漢字) from a website, provide example sentences and pronunciation help (furigana) in hiragana

#Level refers to the JLPT levels of N5->N1
level = "N5"
def change_level_n5():
    global level
    level = "N5"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.place(x=window_width - window_width / 1.01, y=window_height / 60)
    window.update()

def change_level_n4():
    global level
    level = "N4"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.place(x=window_width - window_width / 1.01, y=window_height / 60)
    window.update()

def change_level_n3():
    global level
    level = "N3"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.place(x=window_width - window_width / 1.01, y=window_height / 60)
    window.update()

def change_level_n2():
    global level
    level = "N2"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.place(x=window_width - window_width / 1.01, y=window_height / 60)
    window.update()

def change_level_n1():
    global level
    level = "N1"
    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.place(x=window_width - window_width / 1.01, y=window_height / 60)
    window.update()

window = tk.Tk()
window.configure(bg = 'black')
window_width = 700
window_height = 400 #window height less than 400 makes tkinters boxes overlap
window.geometry(str(window_width) + 'x' + str(window_height) + "+500+200")

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

def get_kanji():
    global jp_click_value, en_click_value, place_kanji, place_kunyomi, place_meaning, place_hiragana, place_sentence1, place_onyomi, sentence1, sentence2, place_sentence2, kanji_str
    clear_text()
    en_click_value = 0
    jp_click_value = 0
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent}
    url = 'https://kanji.fm4dd.com/kanji-random.php?type=JLPT&level=' + level

    request = urllib.request.Request(url, None, headers)
    
    response = urllib.request.urlopen(request, context = ssl._create_unverified_context())
    content = response.read().decode("utf-8")

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

    place_kanji = tk.Label(window, text = kanji_str, font=('ariel', 50), fg = 'maroon2', bg = "black")
    place_kanji.place(x = window_width-window_width/1.75, y = window_height/10)
    place_meaning = tk.Label(window, text = parsed_meaning, font=('ariel', 15, 'bold'), fg = 'green', bg = "black")
    place_meaning.place(x = window_width/4, y = window_height - window_height/1.38)
    place_kunyomi = tk.Label(window, text = parsed_kunyomi, font=('ariel', 10), fg = 'green', bg = "black")
    place_kunyomi.place(x=window_width / 4, y=window_height - window_height / 1.75)
    place_onyomi = tk.Label(window, text = parsed_onyomi, font=('ariel', 10), fg = 'green', bg = "black")
    place_onyomi.place(x = window_width/4, y = window_height - window_height/2.25)

    # place_meaning_title = tk.Label(window, text="意味:", font=('ariel', 15, 'bold'), fg='green', bg="black").place(
    #     x=window_width / 12, y=window_height - window_height / 1.38)
    # place_kunyomi_title = tk.Label(window, text="訓読み:", font=('ariel', 10), fg='green', bg="black").place(
    #     x=window_width / 12, y=window_height - window_height / 1.75)
    # place_onyomi_title = tk.Label(window, text="音読み:", font=('ariel', 10), fg='green', bg="black").place(
    #     x=window_width / 12, y=window_height - window_height / 2.25)

    level_label = tk.Label(window, text="Level: " + level, font=("ariel", 10), fg="pink", bg="black")
    level_label.place(x=window_width - window_width / 1.01, y=window_height / 60)
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
    response = urllib.request.urlopen(request)
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
    place_sentence1 = tk.Label(window, text = sentence1, font=('ariel', 10), fg = 'pink', bg = "black")
    place_sentence1.place(x = window_width/12, y = window_height - window_height/5)
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
        place_hiragana = tk.Label(window, text = hiragana, font=('ariel', 8), fg='aquamarine', bg='black')
        place_hiragana.place(x=window_width / 12, y=window_height - window_height / 4.2)
        jp_click_value+=1
        window.update()

def translate_english():
    global en_click_value, sentence1, kanji_str, parsed_meaning, parsed_kunyomi, parsed_onyomi, place_hiragana, sentence2, place_sentence2
    if en_click_value == 0:
        place_sentence2 = tk.Label(window, text=sentence2, font=('ariel', 9), fg='aquamarine', bg="black", height= 1)
        place_sentence2.place(x=window_width / 12, y=window_height - window_height / 3.5)
        en_click_value += 1
        window.update()

def search_any():
    global place_kanji, place_kunyomi, place_meaning, place_hiragana, place_sentence1, place_onyomi, sentence2, place_sentence2, kanji_str, sentence1, jp_click_value, en_click_value
    # users can be found by right click->Inspect element on the page->Network: look under Headers
    try:
        clear_text()
    except:
        pass
    jp_click_value = 0
    en_click_value = 0
    kanji_str = entry.get()

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    url = "https://www.tanoshiijapanese.com/dictionary/sentences.cfm?j=" + urllib.parse.quote(kanji_str, safe='') + "=&search=Search+>"
    headers = {'User-Agent': user_agent}

    request = urllib.request.Request(url, None,headers)  # The assembled request, parameters if headers needed(url,None,headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode("utf-8")

    parse = BeautifulSoup(content, 'html.parser')

    class_sm = parse.find_all("div", attrs={"class": 'sm'})
    # print(class_sm)

    # Choose a random example sentence, could always add more or less variation by changing numbers, pattern with options is just n+3
    options = [1, 4, 7, 10, 13, 16]
    randomizer = numpy.random.mtrand.randint(0, 6)
    chosen = options[randomizer]

    # Make necessary elements appear in a window
    place_kanji = tk.Label(window, text=kanji_str, font=('ariel', 50), fg='maroon2', bg="black")
    place_kanji.place(x=window_width - window_width / 1.75, y=window_height / 10)
    window.update()

place_meaning_title = tk.Label(window, text="意味:", font=('ariel', 15, 'bold'), fg='green', bg="black").place(x=window_width / 12, y=window_height - window_height / 1.38)
place_kunyomi_title = tk.Label(window, text="訓読み:", font=('ariel', 10), fg='green', bg="black").place(x=window_width / 12, y=window_height - window_height / 1.75)
place_onyomi_title = tk.Label(window, text="音読み:", font=('ariel', 10), fg='green', bg="black").place(x=window_width / 12, y=window_height - window_height / 2.25)

get_kanji_button = tk.Button(window, text="New", command=get_kanji, bg='black', fg='pink', width = 8, height = 1).place(x=window_width * (7/12), y=window_height - window_height / 8)
hiragana_button = tk.Button(window, text="Hiragana", command=translate_hiragana, bg='black', fg="pink", width = 8, height = 1).place(x=window_width * (3/12), y=window_height - window_height / 8)
english_button = tk.Button(window, text="English", command=translate_english, bg='black', fg="pink", width = 8, height = 1).place(x=window_width * (1/12), y=window_height - window_height / 8)
example_sentence_button = tk.Button(window, text="Examples", command=example_sentence, bg='black', fg='pink', width = 8, height = 1).place(x=window_width *(5/12), y=window_height - window_height / 8)

n5_button = tk.Button(window, text="N5", command=change_level_n5, bg='black', fg='pink').place(x=window_width *(2/12), y=window_height - window_height / 1.01)
n4_button = tk.Button(window, text="N4", command=change_level_n4, bg='black', fg='pink').place(x=window_width *(4/12), y=window_height - window_height / 1.01)
n3_button = tk.Button(window, text="N3", command=change_level_n3, bg='black', fg='pink').place(x=window_width *(6/12), y=window_height - window_height / 1.01)
n2_button = tk.Button(window, text="N2", command=change_level_n2, bg='black', fg='pink').place(x=window_width *(8/12), y=window_height - window_height / 1.01)
n1_button = tk.Button(window, text="N1", command=change_level_n1, bg='black', fg='pink').place(x=window_width *(10/12), y=window_height - window_height / 1.01)

submit_entry_button = tk.Button(window, text="submit", height= 1,command=search_any, bg='grey', fg='white').place(x=window_width *(11/12), y=window_height - window_height / 8)
entry_space = tk.Entry(window, textvariable = entry, width=15, bg="grey", fg="white").place(x=window_width *(9.35/12), y=window_height - window_height / 8, height=25)
window.mainloop()

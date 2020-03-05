from googletrans import Translator
import json
import random
import tkinter as tk
from functools import partial
filename = "common.json"
MAX_LVL = 50

def set_words():
    with open(filename) as json_file:
        data = json.load(json_file)["commonWords"]
        with open("data.json", 'w') as outfile:
            outfile.write(json.dumps({str(int(MAX_LVL/2)): data}))


def get_current_file():
    d = {}
    with open("data.json") as json_file:

        d = json.load(json_file)

    return d

def set_word_lvl( word, lvl, old_lvl):
    if lvl > MAX_LVL:
       return

    print(f"changing lvl of {word} from {old_lvl} to {lvl}")

    data = get_current_file()
    print("current file", data)

    if data.get(str(lvl)):
        data[str(lvl)].append(word)
    else:
        data[str(lvl)] = [word]

    data[str(old_lvl)].remove(word)

    # wipes all data
    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)
    loop()


translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])


def get_word_of_that_lvl(lvl):
   print("lvl is", lvl)
   data = get_current_file()
   if data.get(str(lvl)):
      print(data)
      words = data[str(lvl)]
      print("words is", words)
      random.shuffle(words)
      return words
   return None

      # for word in words:
      #    translation = translator.translate(word, dest='ru')
      #    print(translation.origin, ' -> ', translation.text)


#start with max diff level
def lvl_exists(lvl):
    return get_current_file().get(str(lvl))

def get_rand_lvl():
    cur_max_lvl = int(max(get_current_file().keys()))
    lvls = []
    chance = []
    for c in range(1, cur_max_lvl+1):
        if lvl_exists(c):
            lvls.append(c)
    print("lvls", lvls)

    for lvl in lvls:
        print(f"{lvl} of {lvl}")
        for a in range(lvl * len(get_word_of_that_lvl(lvl))):
            chance.append(lvl)
    print(chance)
    random.shuffle(chance)
    print(chance)
    return chance[0]



def rand_word():

    lvl = get_rand_lvl()
    words = get_word_of_that_lvl(lvl)
    if words:
        translation = translator.translate(words[0], dest='ru')
        return [lvl, translation.origin, translation.text]

         # print(translation.origin, ' -> ', translation.text)
         # if input(">") == "1":
         #    set_word_lvl(word, lvl-1, lvl)
         # else:
         #    set_word_lvl(word, lvl+1, lvl)
    # elif lvl-1 != 0:
    #     start(lvl-1)


#set_words()
#start(int(max(get_current_file().keys())))

def show_answer(answer):
    answ["text"] = answer
    print("change answ to", answer)


def show_word(word):
    w["text"] = word


ik = None

def loop():

    global w, answ, ik, idk, show_answ

    print("called loop")

    dat = rand_word()
    lvl = dat[0]
    word = dat[1]
    answer = dat[2]
    print("lvl:", lvl, "\n", f"word: {word} \n answer: {answer} \n ")
    show_word(word)
    show_answer("")


    def show_answer__():
        print("answer is", answer)
        show_answer(answer)

    def set_w_l():
        print("call")
        set_word_lvl(word, lvl - 1, lvl)


    #print(show_answ["command"])

    #show_answ.bind(show_answer__)
    if not ik:
        show_answ = tk.Button(root, text='show answer', command=show_answer__)
        ik = tk.Button(root, text='knew', command=partial(set_w_l) )
        idk = tk.Button(root, text='idk', command=partial(set_word_lvl, word, lvl + 1, lvl))

        ik.pack()
        idk.pack()
        answ.pack()
        w.pack()
        show_answ.pack()
    else:
        show_answ.destroy()
        ik.destroy()
        idk.destroy()

        show_answ = tk.Button(root, text='show answer', command=show_answer__)
        ik = tk.Button(root, text='knew', command=partial(set_w_l))
        idk = tk.Button(root, text='idk', command=partial(set_word_lvl, word, lvl + 1, lvl))

        ik.pack()
        idk.pack()
        answ.pack()
        w.pack()
        show_answ.pack()



root = tk.Tk()
w = tk.Label(root, height=10, width=30)
answ = tk.Label(root, height=10, width=30)

loop()
root.mainloop()


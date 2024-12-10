import PySimpleGUI as sg
from PIL import Image
import speech_recognition as sr
import asyncio
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import webbrowser
import pyautogui
from pytesseract import pytesseract
from PIL import ImageGrab
import time
def scroll(text):
    here = False
    time.sleep(1)
    while here == False:
        pyautogui.scroll(-1000)
        image = ImageGrab.grab(bbox = (550, 150, 1300, 1000))
        image.save('scrinshot.png')
        image = Image.open('scrinshot.png')
        text2 = pytesseract.image_to_string(image).split()
        for i in text2:
            if i.lower() in text:
                here = True
                #pyautogui.moveTo(pyautogui.locateCenterOnScreen('scrinshot.png'))
                #pyautogui.click()  
        #pyautogui.scroll(-500)
    pass
def answer(text):
    with open('dialogues.txt', encoding='utf-8') as f:
        content = f.read()
    blocks = content.split('\n')
    dataset = []
    for block in blocks:
        replicas = block.split('\\')[:2]
        if len(replicas) == 2:
            pair = [replicas[0], replicas[1]]
            if pair[0] and pair[1]:
                dataset.append(pair)
    X_text = []
    y = []
    for question, answer in dataset[:10000]:
        X_text.append(question)
        y += [answer]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_text)
    clf = LogisticRegression()
    clf.fit(X, y)
    text_vector = vectorizer.transform([text.lower()]).toarray()[0]
    question = clf.predict([text_vector])[0]
    return question  
async def talk():
    r = sr.Recognizer()
    print('I am ready')
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        data = r.record(source, duration=5)
        text = r.recognize_google(data,language='ru')
    return text
def open_reddit():
    f = open('keys.txt', 'r')
    text = f.read().split()
    text2 = ''
    for i in text:
        text2 += i
        text2 += ' '
    layout3 = [[sg.Push(), sg.Text('Ключевые слова', size = (50, 1), key = '-title-', font = 'Helvetica 16'), sg.Push()],
               [sg.Input(text2, key = '-key-', font = 'Helvetica 16', size = (400, 400))],
               [sg.Button('Отправить', key = '-redact-')]
]
    f.close()
    window3 = sg.Window('Ключевые слова', layout3, size = (500, 500))
    while True:
        event, values = window3.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-redact-':
            f = open('keys.txt', 'w')
            f.write(window3['-key-'].get())
            f.close()
            break
    window3.close()
    webbrowser.open('https://www.reddit.com')
    f = open('keys.txt', 'r')
    text = f.read().split()
    layout4 = [[sg.Push(), sg.Button('Далее', key = '-continue-'), sg.Push()]
    ]
    window4 = sg.Window('Далее', layout4, size = (500, 100))
    while True:
        event, values = window4.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == '-continue-':
            scroll(text)
    window4.close()
    text3 = ''
    for i in text:
        text3 += i
        text3 += ' '
    f.close()
    f = open('keys.txt', 'w')
    f.write(text3)
    f.close()
    pass
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
image = Image.open(r'orig-round.png')
image.thumbnail((200, 200))
image.save('avatar.png')
sg.theme('Dark Purple1') 
layout = [[sg.Push(), sg.Image('avatar.png', key = '-AVATAR-'), sg.Push()], 
          [sg.Push(), sg.Button('Говорить', key = '-START-'), sg.Push(), sg.Button('Написать', key = '-write-'), sg.Push()], 
          [sg.Text('Привет! Я - Лина, твой виртаульный помощник', size = (50, 2), key = '-text-', font = 'Helvetica 16')],
          [sg.Text('', size = (50, 1), key = '-timer-', font = 'Helvetica 16')]
]
window = sg.Window('Лина', layout, size = (500, 500))
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-START-':
        text = asyncio.run(talk())
        result = answer(text)
        if result == 'open_reddit':
            window['-timer-'].update('>> Открываю')
            open_reddit()
        elif result == 'close':
            break
        else:
            window['-timer-'].update('>> ' + result)
    if event == '-write-':
        layout2 = [[sg.Button('Отправить', key = '-send-'), sg.Input(key = '-input-')]]
        window2 = sg.Window('Писать', layout2, size= (500, 100))
        while True:
            event, values = window2.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == '-send-':
                result = answer(window2['-input-'].get())
                if result == 'open_reddit':
                    window['-timer-'].update('>> Открываю')
                    window2.close()
                    open_reddit()
                elif result == 'close':
                    print('Back')
                    window.close()
                else:
                    window['-timer-'].update('>> ' + result)
                    window2.close()
            break
        window2.close()
window.close()

import cv2, os
from pygame import mixer

def do_photo(name, path):
    cap = cv2.VideoCapture(0) # Включаем первую камеру
    for i in range(30): cap.read() # "Прогреваем" камеру, чтобы снимок не был тёмным 
    ret, frame = cap.read() # Делаем снимок 
    #frame = frame[300, 150] обрезать фото
    photo_file = '{}/{}'.format(os.path.join(path, 'static/photo'),name)
    cv2.imwrite(photo_file, frame) # Записываем в файл
    cap.release() # Отключаем камеру
    return ''

def play_music(mp3_file:str):
    mixer.init()
    mixer.music.load(mp3_file)
    mixer.music.play()
from threading import Thread
from pygame import mixer
import os
import json
import random

mixer.init()  # инициализируем плеер

class Music:
    def __init__(self):
        self.music_playing = False
        self.music_list = []
        self.current_music_index = -1
        self.thread_running = False  # добавляем переменную для хранения состояния потока

    def play_music(self, music_file):
        """Функция для воспроизведения музыкального файла"""
        mixer.music.load(music_file)
        mixer.music.play()
        self.music_playing = True
        self.current_music_index = len(self.music_list)
        self.music_list.append(music_file)  # добавляем проигрываемую музыку в список

    def stop_music(self):
        """Функция для остановки текущей музыки"""
        mixer.music.stop()
        self.music_playing = False
    
    def fade_music(self,time:int=1000):
        """Функция для затухания музыки перед остановкой"""
        mixer.music.fadeout(time) # затушить музыку за 1 секунду

    def is_music_playing(self):
        """Функция для проверки, играет ли музыка в данный момент"""
        return self.music_playing

    def check_music_list(self):
        """Функция для проверки наличия более одного музыкального файла в списке и постановки следующего файла на воспроизведение"""
        if len(self.music_list) > 1:
            self.current_music_index += 1
            if self.current_music_index >= len(self.music_list):
                self.current_music_index = 0
            mixer.music.queue(self.music_list[self.current_music_index])
        elif len(self.music_list) == 1:  # если в списке только один музыкальный файл, проигрываем его снова
            mixer.music.queue(self.music_list[0])

    def clear_music_list(self):
        """Функция для очистки списка музыки"""
        self.music_list = []
        self.current_music_index = -1

    def add_music_to_list(self, music_file):
        """Функция для добавления одного музыкального файла в список музыки"""
        self.music_list.append(music_file)

    def add_multiple_music_to_list(self, music_folder):
        """Функция для добавления нескольких музыкальных файлов из папки в список музыки"""
        for file in os.listdir(music_folder):
            if file.endswith(".mp3"):  # добавляем только файлы .mp3
                self.add_music_to_list(os.path.join(music_folder, file))

    def add_music_list_to_queue(self, music_list):
        """Функция для добавления списка музыки в очередь на воспроизведение"""
        for music_file in music_list:
            self.add_music_to_list(music_file)

    def add_music_from_json(self, json_file):
        """Функция для чтения списка музыки из json файла и добавления ее в список музыки"""
        with open(json_file, 'r') as f:
            music_data = json.load(f)
            for music_file in music_data["music"]:
                self.add_music_to_list(music_file)

    def shuffle_music_list(self):
        """Функция для перемешивания списка музыки"""
        random.shuffle(self.music_list)

    def repeat_music(self, times):
        """Функция для повтора текущего музыкального файла несколько раз"""
        if self.is_music_playing():
            mixer.music.queue(self.music_list[self.current_music_index] * times)

    def change_volume(self, volume):
        """Функция для изменения громкости"""
        mixer.music.set_volume(volume)

    def get_current_index(self):
        """Функция для получения индекса текущего музыкального файла в списке музыки"""
        return self.current_music_index

    def get_length_of_music_list(self):
        """Функция для получения количества музыкальных файлов в списке музыки"""
        return len(self.music_list)

    def run_check_music_list_in_background(self):
        """Функция, которая запускает метод check_music_list в фоновом режиме для непрерывной проверки и воспроизведения следующей музыки"""
        self.thread_running = True  # устанавливаем флаг запуска потока
        t = Thread(target=self.continuously_check_music_list)
        t.daemon = True
        t.start()

    def continuously_check_music_list(self):
        """Функция, которая непрерывно проверяет, играет ли музыка в данный момент, и если нет, вызывает метод check_music_list"""
        while self.thread_running:  # проверяем флаг работы потока
            if not self.is_music_playing():
                self.check_music_list()
            mixer.get_busy()  # чтобы играло в фоновом режиме без остановки воспроизведения музыки

    def stop_check_music_list(self):
        """Функция для остановки потока проверки списка музыки"""
        self.thread_running = False  # изменяем флаг работы потока\n\n
        
    def __del__(self):        
        "Функция для очистки памяти и остановки потока при удалении объекта"""
        self.stop_check_music_list()  # останавливаем поток, если он был запущен
        mixer.quit()  # выключаем плеер

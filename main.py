import tkinter  # работа с графикой
import pygame   # в данном случае для звука


class Sound:  # класс для работы со звуком
    def __init__(self):
        pygame.mixer.init()  # готовим библиотеку к работе со звуком
        self.put_true = pygame.mixer.Sound('clickButton.mp3')  # загружаем звука попадения в свободную ячейку
        self.put_false = pygame.mixer.Sound('clickError.mp3')  # загружаем звука попадения в занятую ячейку

    def play_true(self):  # проигрываем звук тру
        self.put_true.play()

    def play_false(self):  # проигрываем звук фолс
        self.put_false.play()


class Grafik(tkinter.Canvas):  # класс для работы с графикой
    def __init__(self, window):
        super().__init__(window, width=900, height=900, bg='black')

    def create_playing_field(self):  # метод для создания игрового поля
        self.create_line(300, 0, 300, 900, width=3, fill='green')
        self.create_line(600, 0, 600, 900, width=3, fill='green')
        self.create_line(0, 300, 900, 300, width=3, fill='green')
        self.create_line(0, 600, 900, 600, width=3, fill='green')

    def create_cross(self, x0, y0, x, y):  # метод для отрисовки крестика
        x0 += 20
        y0 += 20
        x -= 20
        y -= 20
        self.create_line(x0, y0, x, y, width=5, fill='red')
        self.create_line(x, y0, x0, y, width=5, fill='red')

    def create_zero(self, x0, y0, x, y):  # метод для отрисовки нолика
        x0 += 20
        y0 += 20
        x -= 20
        y -= 20
        self.create_oval(x0, y0, x, y, outline='blue', width=5)

    def create_move(self, player, x0, y0, x, y):  # метод выбирающий что отрисовать крестик или нолик
        # принимает в параметры игрока, то есть крестик или нолик и координаты где ставить тот или иной знак
        if player == 'x':
            self.create_cross(x0, y0, x, y)
        else:
            self.create_zero(x0, y0, x, y)

    def create_wind_player(self, player):  # метод для создания окна в случае победы одного из игроков
        self.delete('all')
        self.config(bg='black')
        self.create_text(450, 450, text=f'Победил игрок {player}!', font=('Arial', 30), fill='yellow')

    def create_draw_wind(self):  # метод для создания окна в случае ничьи
        self.delete('all')
        self.config(bg='black')
        self.create_text(450, 450, text='Ничья!', font=('Arial', 30), fill='yellow')


class Rules:  # класс с правилами игры
    def __init__(self):
        self.field = [
                      ['', '', ''],
                      ['', '', ''],
                      ['', '', '']
                      ]
        self.move = 0  # переменная отслеживающая ходы

    def check_win(self, player):  # проверка на победу
        for i in range(3):
            if self.field[0][i] == self.field[1][i] == self.field[2][i] == player:    # проверка по горизонтале
                game.create_wind_player(player)
            elif self.field[i][0] == self.field[i][1] == self.field[i][2] == player:  # проверка по вертикале
                game.create_wind_player(player)
        if self.field[0][0] == self.field[1][1] == self.field[2][2] == player:        # проверка по горизонтале
            game.create_wind_player(player)
        elif self.field[0][2] == self.field[1][1] == self.field[2][0] == player:      # проверка по гориизонтале
            game.create_wind_player(player)

    def check_draw(self):  # проверка на ничью
        cell_ocup_count = 0
        for row in self.field:
            for el in row:
                if el != '':
                    cell_ocup_count += 1
        if cell_ocup_count == 9:
            game.create_draw_wind()

    def check_player_move(self):  # определяет какой игрок ходит х или о и возращает это результат
        self.move += 1
        if self.move % 2 == 1:
            player = 'x'
        else:
            player = 'o'
        return player


class Dates(Rules):  # класс для который обрабатывает входные данные, то есть клик мыши по какой-либо части холста
    def get_mouse_click(self, event):  # получаем координаты клика и вызываем функцию которая ставит туда знак
        x, y = event.x, event.y
        self.choice_cell(x, y)

    def choice_cell(self, dx, dy):  # выбираем ячейку куда ставить знак
        for i in range(3):  # пробегаем по каждой клетке на холсте
            for j in range(3):
                x0, y0, x, y = i * 300, j * 300, i * 300 + 300, j * 300 + 300   # проверяем в этих координатах
                if x0 < dx < x and y0 < dy < y and self.field[i][j] == '':  # если да то ставим знак
                    player = rules.check_player_move()    # проверяем какой знак ставить
                    game.create_move(player, x0, y0, x, y)  # ставим выбранный знак
                    sound.play_true()                     # проигрываем звук свободной ячейки
                    self.field[i][j] = player             # передаем в список значение которое нужно поставить (х или о)
                    self.check_win(player)                # делаем проверку на победу
                    self.check_draw()                     # делаем проверку на ничью
                    return                                # завершаем выполнение функции чтобы не проигрывался звук фолс
        sound.play_false()  # проигрывать этот звук в случае попадания в занятую ячейку


# создаем окно
tk_window = tkinter.Tk()
tk_window.title('TicTacToe')
game = Grafik(tk_window)
game.pack()

# создаем игровое поле
game.create_playing_field()

# создаем экземпляры классов
rules = Rules()
dates = Dates()
sound = Sound()

# привязываем клик мыши к вызову метода обработки данных
game.bind('<Button-1>', dates.get_mouse_click)

# запускаем окно и удерживаем его открытым
tk_window.mainloop()

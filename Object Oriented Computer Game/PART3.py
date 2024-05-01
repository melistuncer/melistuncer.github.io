from ast import Str
import sys, pygame, time, random
pygame.init()
pygame.font.init()


class Game_Launcher:
    CAR_IMAGE = pygame.image.load("greencar.png")
    COIN_IMAGE = pygame.image.load("coin.png")
    HOLE_IMAGE = pygame.image.load("hole.png")
    TREE_IMAGE = pygame.image.load("tree.png")
    FUEL_IMAGE = pygame.image.load("fuel.png")
    HEALTH_IMAGE = pygame.image.load("heart.png")
    GAS_IMAGE = pygame.image.load("fuel.png")

    size = width, height = 1000, 780
    screen = pygame.display.set_mode(size)
    background = pygame.transform.scale(pygame.image.load("asphalt.jpg"), size)
    cropped_background = pygame.Surface.subsurface(background, 0, 656, 1000, 124)

    posx_list = [75,275,475,675]
    list = []

    CAR = []
    STRIPS = []
    OBJECTS = []
    LEVELS = []
    OBSTACLES =[]

    def __init__(self, value):
        self._bool = value
        self._bool2 = True
        self._playing_time = 0
        self._level = 1
        self._remote_control = False

    def starting_screen(self):
        if self._bool2:
            font = pygame.font.SysFont("timesnewroman", 30)
            font2 = pygame.font.SysFont("timesnewroman", 35)
            text1 = font.render("- Press '''p''' to start game.", 1, (255,170,50))
            text2 = font.render("- Press '''a''' to move car left.", 1, (255,170,50))
            text3 = font.render("- Press '''d''' to move car right.", 1, (255,170,50))
            text4 = font.render("* Level increases every 30 seconds.", 1, (25,195,255))
            text5 = font.render("* During the last 10 seconds of each level, ", 1, (25,195,255))
            text6 = font.render("the control keys switch places.", 1, (25,195,255))
            text7 = font2.render("Have fun!", 1, (255,100,150))
            Game_Launcher.screen.blit(text1, (150, 150))
            Game_Launcher.screen.blit(text2, (150, 200))
            Game_Launcher.screen.blit(text3, (150, 250))
            Game_Launcher.screen.blit(text4, (150, 350))
            Game_Launcher.screen.blit(text5, (150, 400))
            Game_Launcher.screen.blit(text6, (150, 450))
            Game_Launcher.screen.blit(text7, (150, 550))

    def create_objects(self):
        Game_Launcher.random_picker()
        car = Car(450, 456, Game_Launcher.CAR_IMAGE, Game_Launcher.screen)
        Game_Launcher.CAR.append(car)
        strip1 = Strip(195, 0, 2, Game_Launcher.screen)
        strip2 = Strip(395, 0, 2, Game_Launcher.screen)
        strip3 = Strip(595, 0, 2, Game_Launcher.screen)
        strip_4 = Strip(195,260, 2, Game_Launcher.screen)
        strip_5 = Strip(395,260, 2, Game_Launcher.screen)
        strip_6 = Strip(595,260, 2, Game_Launcher.screen)
        strip_7 = Strip(195,520, 2, Game_Launcher.screen)
        strip_8 = Strip(395,520, 2, Game_Launcher.screen)
        strip_9 = Strip(595,520, 2, Game_Launcher.screen)
        Game_Launcher.STRIPS.extend([strip1, strip2, strip3, strip_4, strip_5, strip_6, strip_7, strip_8, strip_9])
        coin = Coin(0, Game_Launcher.COIN_IMAGE, Game_Launcher.list, 2, Game_Launcher.screen)
        Game_Launcher.OBJECTS.append(coin)
        fuel = Fuel(0, Game_Launcher.FUEL_IMAGE, Game_Launcher.list, 2, Game_Launcher.screen)
        Game_Launcher.OBJECTS.append(fuel)
        tree = Tree(0, Game_Launcher.TREE_IMAGE, Game_Launcher.list, 2, Game_Launcher.screen)
        Game_Launcher.OBSTACLES.append(tree)
        hole = Hole(0, Game_Launcher.HOLE_IMAGE, Game_Launcher.list, 2, Game_Launcher.screen)
        Game_Launcher.OBSTACLES.append(hole)
        Game_Launcher.OBJECTS.extend([tree, hole])

        health = Health(Game_Launcher.screen, Game_Launcher.HEALTH_IMAGE)
        Game_Launcher.LEVELS.append(health)
        score = Score(Game_Launcher.screen, Game_Launcher.COIN_IMAGE)
        Game_Launcher.LEVELS.append(score)
        gas = Gas(Game_Launcher.screen, Game_Launcher.GAS_IMAGE)
        Game_Launcher.LEVELS.append(gas)


    def random_picker():
        while len(Game_Launcher.list) < 4:
            item = random.choice(Game_Launcher.posx_list)
            Game_Launcher.list.append(item)
            Game_Launcher.posx_list.remove(item)
        return list

    def working(self):
        self._bool = True
        self._bool2 = False

    def not_working(self):
        self._bool = False
        
    def move_car_left(self):
        for car in Game_Launcher.CAR:
            car.move_left()

    def move_car_right(self):
        for car in Game_Launcher.CAR:
            car.move_right()

    def remote_control_move_left(self):
        for car in Game_Launcher.CAR:
            car.remote_control_move_left()

    def remote_control_move_right(self):
        for car in Game_Launcher.CAR:
            car.remote_control_move_right()  

    def shuffle(self):
        if Game_Launcher.OBJECTS[0].return_posy() < 840 and Game_Launcher.OBJECTS[0].return_posy() > 792:
            Game_Launcher.random_picker()
            Game_Launcher.posx_list.extend([75, 275, 475, 675])
            Game_Launcher.list.clear()
            Game_Launcher.random_picker()
            for object in Game_Launcher.OBJECTS:
                object.change_lane(Game_Launcher.list)
                object.select_lane()

    def blit_window(self):
        level = self._level
        main_font = pygame.font.SysFont("timesnewroman", 30)

        Game_Launcher.screen.blit(Game_Launcher.background, (0,0))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        Game_Launcher.screen.blit(level_label,(350,10))

        for car in Game_Launcher.CAR:
            car.show()
        for item in Game_Launcher.STRIPS:
            item.show()
            item.move()
        for object in Game_Launcher.OBJECTS:
            object.move()
            object.show()
            object.hide_self(Game_Launcher.CAR[0])
        for obstacle in Game_Launcher.OBSTACLES:
            obstacle.lose_health(Game_Launcher.CAR[0], Game_Launcher.LEVELS[0])
        for level in Game_Launcher.LEVELS:
            level.show()
        pygame.display.update()

    def get_score(self):
        Game_Launcher.OBJECTS[0].get_score(Game_Launcher.CAR[0], Game_Launcher.LEVELS[1])

    def get_fuel(self):
        Game_Launcher.OBJECTS[1].get_fuel(Game_Launcher.CAR[0], Game_Launcher.LEVELS[2])

    def lose_fuel(self):
        Game_Launcher.LEVELS[2].lose_fuel()

    def speed_up(self):
        self._playing_time += clock.get_time()/1000
        if self._playing_time >= 30:
            for strip in Game_Launcher.STRIPS:
                strip.speed_up()
            for object in Game_Launcher.OBJECTS:
                object.speed_up()
            self._playing_time = 0
            self._level += 1

    def remote_control(self):
        if self._playing_time > 20 and self._playing_time < 30:
            self._remote_control = True
        else:
            self._remote_control = False

    def lose_game(self):
        if Game_Launcher.LEVELS[0].lose_game():
            self._bool = False
            score = Game_Launcher.LEVELS[1].return_value()
            pygame.draw.rect(Game_Launcher.screen, (255,255,255), (300,240,400,400))
            font = pygame.font.Font('freesansbold.ttf', 32)
            text1 = font.render("Your life is over!", True, (100,200,250))
            text2 = font.render(f"Your Score: {score}", 1, (255,0,100))
            Game_Launcher.screen.blit(text1, (370, 350))
            Game_Launcher.screen.blit(text2, (390, 450))

        elif Game_Launcher.LEVELS[2].lose_game():
            self._bool = False
            score = Game_Launcher.LEVELS[1].return_value()
            pygame.draw.rect(Game_Launcher.screen, (255,255,255), (300,240,400,400))
            font = pygame.font.Font('freesansbold.ttf', 32)
            text1 = font.render("You are out of fuel!", True, (100,200,250))
            text2 = font.render(f"Your Score: {score}", 1, (255,0,100))
            Game_Launcher.screen.blit(text1, (350, 350))
            Game_Launcher.screen.blit(text2, (390, 450))
        

class Car:
    def __init__(self, x, y, image, screen):
        self._posx = x
        self._posy = y
        self._image = image
        self._screen = screen
        self._sized = pygame.transform.smoothscale(self._image, (100,200))
        self._lane = 3
        self._remote_control = False

    def show(self):
        self._screen.blit(self._sized, (self._posx, self._posy))

    def move_left(self):
        if self._posx -200 > 0:
            self._posx -= 200
            self._lane -= 1
        else:
            pass
    
    def move_right(self):
        if self._posx + 200 < 800:
            self._posx += 200
            self._lane += 1
        else:
            pass

    def remote_control_move_left(self):
        if self._posx + 200 < 800:
            self._posx += 200
            self._lane += 1
        else:
            pass

    def remote_control_move_right(self): 
        if self._posx -200 > 0:
            self._posx -= 200
            self._lane -= 1
        else:
            pass

    def return_posy(self):
        return self._posy

    def return_lane(self):
        return self._lane

class Strip:
    def __init__(self, x, y, speed, screen):
        self._posx = x
        self._posy = y
        self._speedy = speed
        self._screen = screen

    def show(self):
        pygame.draw.rect(self._screen, (255,255,255), (self._posx, self._posy,10,50))

    def move(self):
        self._posy += self._speedy
        if self._posy >= 780:
            self._posy = 0

    def speed_up(self):
        self._speedy += 2


class Objects:
    def __init__(self, y, image, list, speed, screen):
        self._posy = y
        self._image = image
        self._scaled = pygame.transform.smoothscale(self._image, (50,50))
        self._screen = screen
        self._possible_posx = [75,275,475,675]
        self._lane_list = list
        self._speedy = speed

    def move(self):
        self._posy += self._speedy
        if self._posy >= 840:
            self._posy = 0

    def select_lane(self):
       self._lane = self._possible_posx.index(self._posx) + 1

    def show(self):
        self._screen.blit(self._scaled, (self._posx, self._posy))

    def hide_self(self, car):   
        transparent = (0,0,0,0)
        if self._posy + 48 == car._posy:
            if self._lane == car._lane:
                self._scaled.fill(transparent)
        if self._posy == 0:
            self._scaled = pygame.transform.smoothscale(self._image, (50,50))
            
    def speed_up(self):
        self._speedy += 2

    def return_posy(self):
        return self._posy

class Coin(Objects):
    def __init__(self, y, image, list, speed, screen):
        super().__init__(y, image, list, speed, screen)
        self._posx = self._lane_list[0]
        self.select_lane()

    def change_lane(self, list):
        self._posx = list[0]

    def get_score(self, car, score):
        if self._posy +48 == car.return_posy():
            if car.return_lane() == self._lane:
                score.get_score()

class Fuel(Objects):
    def __init__(self, y, image, list, speed, screen):
        super().__init__(y, image, list, speed, screen)
        self._posx = self._lane_list[1]
        self.select_lane()

    def change_lane(self, list):
        self._posx = list[1]

    def get_fuel(self, car, gas):
        if self._posy +48== car.return_posy():
            if car.return_lane() == self._lane:
                gas.get_fuel()

class Obstacles(Objects):
    def __init__(self, y, image, list, speed, screen):
        super().__init__(y, image, list, speed, screen)

    def lose_health(self, car, health_level):
        if self._posy +48 == car.return_posy():
            if car.return_lane() == self._lane:
                health_level.decrease_health()

class Tree(Obstacles):
    def __init__(self, y, image, list, speed, screen):
        super().__init__(y, image, list, speed, screen)
        self._posx = self._lane_list[2]
        self.select_lane()

    def change_lane(self, list):
        self._posx = list[2]

class Hole(Obstacles):
    def __init__(self, y, image, list, speed, screen):
        super().__init__(y, image, list, speed, screen)
        self._posx = self._lane_list[3]
        self.select_lane()
        self._scaled = pygame.transform.smoothscale(self._image, (65,65))

    def change_lane(self, list):
        self._posx = list[3]


class Levels():
    def __init__(self, screen, image):
        self._image = image
        self._sized = pygame.transform.smoothscale(self._image, (40,40))
        self._screen = screen

class Health(Levels):
    def __init__(self, screen, image):
        super().__init__(screen, image)
        self._amount = 3

    def show(self):
        if self._amount == 3:
            self._screen.blit(self._sized, (800, 100))
            self._screen.blit(self._sized, (860, 100))
            self._screen.blit(self._sized, (920, 100))
        elif self._amount == 2:
            self._screen.blit(self._sized, (800, 100))
            self._screen.blit(self._sized, (860, 100))
        elif self._amount == 1:
            self._screen.blit(self._sized, (800, 100))

    def decrease_health(self):
        self._amount -= 1 

    def lose_game(self):
        if self._amount == 0:
            return True

class Score(Levels):
    def __init__(self, screen, image):
        super().__init__(screen, image)
        self._value = 0

    def show(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        score = str(self._value)
        text = font.render(f":  {score}", True, (255, 255, 255))
        self._screen.blit(text, (880, 50))
        self._screen.blit(self._sized, (830, 45))

    def get_score(self):
        self._value += 1

    def return_value(self):
        return self._value

class Gas(Levels):
    def __init__(self, screen, image):
        super().__init__(screen, image)
        self._amount = 100
        self._playing_time = 30

    def show(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        fuel_left = str("%.1f" % self._amount)
        text = font.render(f": {fuel_left}", True, (255, 255, 255))
        self._screen.blit(text, (875, 730))
        self._screen.blit(self._sized, (825, 725))

    def get_fuel(self):
        self._amount = 100

    def lose_fuel(self):
        self._playing_time += clock.get_time()/1000 
        self._amount -= clock.get_time()/500*(self._playing_time//30)

    def lose_game(self):
        if self._amount <= 0:
            return True



playing = Game_Launcher(False)
clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if playing._bool:
                    pass
                else:
                    playing.create_objects()
                    playing.working()

            if event.key == pygame.K_a:
                if playing._remote_control == False:
                    playing.move_car_left()
                else:
                    playing.remote_control_move_left()

            if event.key == pygame.K_d:
                if playing._remote_control == False:
                    playing.move_car_right()
                else:
                    playing.remote_control_move_right()


    if playing._bool: 
        playing.shuffle() 
        playing.blit_window()
        playing.get_score()
        playing.get_fuel()
        playing.lose_fuel()
        playing.speed_up()
        playing.remote_control()
        playing.lose_game()

    if playing._bool == False:
        playing.starting_screen()
        
    pygame.display.update()
    pygame.time.wait(1)
    clock.tick()

 
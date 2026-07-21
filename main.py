import random #import the randomizer functions
from browser import timer #import timer functions
import math

car_colors = [Color.red,Color.orange,Color.yellow,Color.blue,Color.purple] #list of car colors
lanes = [0,50,100,150,200,250,300,350] #lane x values
starts = [get_height(),0] #start y values
minute = 0
second = 0
#above are the minute and second timer initialization values
cars = [] #list of the cars that will be spawned on screen
game_over = False

background = Rectangle(500,500)
background.set_position(0,0)
add(background)
#adds a black background

lane_settings = {} #initializing the dictionary that contains the settings for each lane

def randomize_lane_settings():
    global lane_settings
    possible_speeds = [200,300,400,500,600]
    possible_directions = [1,-1]
    lane_settings = {}
    for lane in lanes:
        speed = random.choice(possible_speeds)
        direction = random.choice(possible_directions)
        lane_settings[lane] = {"speed":speed,"direction":direction}

randomize_lane_settings()
#randomizing lane settings

def timers():
    global second
    global minute
    second += 1
    if second > 59:
        second = 0
        minute += 1
    txt.set_text(f"Time: {minute:02d}:{second:02d}")
    remove(txt)
    add(txt) #timer function


def add_road_lines():
    x = 45
    for i in range(len(lanes)-1):
        line = Line (x,0,x,500)
        line.set_color(Color.white)
        add(line)
        x += 50
    
add_road_lines()
#adding white road lines


player = Circle(15)
player.set_position(18,get_height()/2)
player.set_color(Color.green)
add(player)
#adds the player onto screen

def move_player(event):
    if game_over == True:
        return
    current_x = player.get_x()
    current_y = player.get_y()
    
    new_x = current_x
    new_y = current_y
    
    if event.key == "ArrowRight":
        new_x += 50
    elif event.key == "ArrowUp":
        new_y -= 20
    elif event.key == "ArrowDown":
        new_y += 20
    elif event.key == "ArrowLeft":
        new_x -= 50
        
    min_x = 0
    max_y = 470
    min_y = 0
    max_x = 400
    
    if min_x <= new_x <= max_x and min_y <= new_y <= max_y:
        player.set_position(new_x,new_y)
    
player_movement = add_key_down_handler(move_player)
    #key handler to move player piece


def add_cars(): 
    car = Rectangle(30,55)
    rand_lane = random.choice(lanes)
    settings = lane_settings[rand_lane]
    speed = settings["speed"]
    direction = settings["direction"]
    start_y = 0 if direction == 1 else get_height()
    
    safe_to_spawn = True
    for existing_car in cars:
        x = existing_car.get_x()
        y = existing_car.get_y()
        if x == rand_lane and abs(y-start_y) < 100:
            safe_to_spawn = False
            break
    if not safe_to_spawn:
        return
    
    car.set_color(random.choice(car_colors))
    car.set_position(rand_lane,start_y)
    add(car)
    cars.append(car)
    

    def move_car():
        car.move(0, 20 * direction)
        
    def del_car():
        if car in cars:
            cars.remove(car)
        remove(car)
            
        
    timer.set_interval(move_car,speed)
    timer.set_timeout(del_car,19000)
#adds a moving car of a random color, speed, and in a random lane to the game board

def check_collision():
    player_x = player.get_x() + 15
    player_y = player.get_y() + 15
    player_radius = 15
    
    for car in cars:
        car_x = car.get_x()
        car_y = car.get_y()
        car_width = 30
        car_height = 55
        
        player_left = player_x - player_radius
        player_right = player_x + player_radius
        player_top = player_y - player_radius
        player_bottom = player_y + player_radius
    
        car_left = car_x
        car_right = car_x + car_width
        car_top = car_y 
        car_bottom = car_y + car_height
    
        if (player_right > car_left and player_left < car_right and player_bottom > car_top and player_top < car_bottom):
            return True
    return False
    
def explosion():
    x = player.get_x()-15
    y = player.get_y()-25
    boom1 = Rectangle(40,50)
    boom1.set_color(Color.red)
    boom1.set_position(x,y)
    boom1.set_rotation(math.radians(45))
    add(boom1)
    boom2 = Rectangle(40,50)
    boom2.set_color(Color.red)
    boom2.set_position(x-5,y)
    boom2.set_rotation(math.radians(-45))
    add(boom2)
    boom3 = Rectangle(10,40)
    boom3.set_color(Color.orange)
    boom3.set_position(x+5,y+5)
    boom3.set_rotation(math.radians(25))
    add(boom3)
    boom4 = Rectangle(10,40)
    boom4.set_color(Color.orange)
    boom4.set_position(x+5,y+5)
    boom4.set_rotation(math.radians(-25))
    add(boom4)
    boom5 = Rectangle(10,40)
    boom5.set_color(Color.orange)
    boom5.set_position(x+5,y+5)
    boom5.set_rotation(math.radians(90))
    add(boom5)
    boom6 = Rectangle(5,50)
    boom6.set_color(Color.yellow)
    boom6.set_position(x+8,y)
    boom6.set_rotation(math.radians(0))
    add(boom6)
    boom7 = Rectangle(5,50)
    boom7.set_color(Color.yellow)
    boom7.set_position(x+8,y)
    boom7.set_rotation(math.radians(-45))
    add(boom7)
    boom8 = Rectangle(5,50)
    boom8.set_color(Color.yellow)
    boom8.set_position(x+8,y)
    boom8.set_rotation(math.radians(45))
    add(boom8)
    boom9 = Rectangle(5,50)
    boom9.set_color(Color.yellow)
    boom9.set_position(x+8,y)
    boom9.set_rotation(math.radians(90))
    add(boom9)
    
def game_loop():
    global game_over
    if check_collision():
        player.set_color(Color.red)
        game_over = True
        message = Text("GAME OVER!")
        message.set_position(120,100)
        message.set_color(Color.red)
        add(message)
        timer.clear_interval(game_timer)
        timer.clear_interval(time)
        explosion()
        return


timer.set_interval(add_cars, 1000) #cars added every second
time = timer.set_interval(timers,1000)#calls timer function to update the timer every second
game_timer = timer.set_interval(game_loop, 50)

txt = Text(f"Time: {minute:02d}:{second:02d}")
txt.set_position(125,50)
txt.set_color(Color.gray)
add(txt)
print("Click on the screen and use the arrow keys to move and survive as long as you can!")
#adding the timer on screen
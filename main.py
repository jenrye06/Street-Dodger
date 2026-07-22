import random #import the randomizer functions 
from browser import timer #import timer functions 
from browser import document #import document functions 
import math #import math functions 

canvas = document["game"] #get the canvas element from the HTML document
ctx = canvas.getContext("2d") #get the context of the canvas

lane_settings = {} #initializing the dictionary that contains the settings for each lane 
car_colors = ["red","orange","yellow","blue","purple"] #list of car colors 
lanes = [0,50,100,150,200,250,300,350] #lane x values
possible_speeds = [4,5,6,7,8] #possible speed values
high_score = 0; 
score = 0;
minute = 0 
second = 0 
#above: minute and second timer initialization values 
cars = [] #list of the cars that will be spawned on screen 
game_over = False 
paused = False #initializing the paused variable to false

def clear_canvas():
    ctx.clearRect(0, 0, canvas.width, canvas.height)


def Rectangle(x,y,width,height,color): #rectangle drawing function
    ctx.fillStyle = color 
    ctx.fillRect(x,y,width,height) 

def RotatedRectangle(x,y,width,height,color,angle): #rotated rectangle drawing function
    ctx.save() 
    ctx.translate(x + width / 2, y + height / 2) 
    ctx.rotate(angle) 
    ctx.fillStyle = color 
    ctx.fillRect(-width / 2, -height / 2, width, height)
    ctx.restore()

def Line(x1,y1,x2,y2,color): #line drawing function
    ctx.strokeStyle = color 
    ctx.beginPath() 
    ctx.moveTo(x1,y1) 
    ctx.lineTo(x2,y2) 
    ctx.stroke()

def Circle(x,y,radius,color): #circle drawing function
    ctx.fillStyle = color 
    ctx.beginPath() 
    ctx.arc(x,y,radius,0,2*math.pi) 
    ctx.fill()

def Text(text,x,y,color): #text drawing function
    ctx.fillStyle = color 
    ctx.font = "20px Arial" 
    ctx.fillText(text, x, y)

def draw_timer(): #draws the timer on the canvas
    timer_text = f"{minute:02d}:{second:02d}" 
    Text(timer_text, 10, 30, "white")

def draw_score(): #draws score on canvas
    global score
    score_text = "Score: " + score
    Text(score_text,10,20,"white")

def draw_game_over(): #draws the game over text on the canvas
    Text("GAME OVER", 150, 250, "red")

def draw_player(): #draws the player on the canvas
    Circle(player["x"], player["y"], player["radius"], player["color"])

def draw_cars(): #draws the cars on the canvas
    for car in cars: 
        Rectangle(car["x"], car["y"], 30, 55, car["color"])

def get_height():
    return canvas.height #returns canvas height

def timers(): 
    global second 
    global minute 
    second += 1 
    if second > 59: 
        second = 0 
        minute += 1 

def calculate_score():
    global score
    return score + 1

def move_player(event): 
    if game_over == True: 
        return 
    current_x = player["x"] 
    current_y = player["y"]     
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
        player["x"] = new_x 
        player["y"] = new_y 
    #key handler to move player piece (fix later)

def add_road_lines(): #adds the lines to the road
    x = 45 
    for i in range(len(lanes)-1): 
        line = Line (x,0,x,500,"white") 
        x += 50 

def randomize_lane_settings(): 
    global lane_settings 
    global possible_speeds 
    possible_directions = [1,-1] 
    lane_settings = {} 
    for lane in lanes: 
        speed = random.choice(possible_speeds) 
        direction = random.choice(possible_directions) 
        lane_settings[lane] = {"speed":speed,"direction":direction} 
        #randomizes the speed and direction of each lane and stores it in the lane_settings dictionary

def add_cars():  
    rand_lane = random.choice(lanes)
    settings = lane_settings[rand_lane] 
    speed = settings["speed"] 
    direction = settings["direction"] 
    start_y = 0 if direction == 1 else get_height() 
    safe_to_spawn = True 
    for existing_car in cars: 
        x = existing_car["x"] 
        y = existing_car["y"] 
        if x == rand_lane and abs(y-start_y) < 100: 
            safe_to_spawn = False 
            break 
    if not safe_to_spawn: 
        return 
    car = {"x": rand_lane, "y": start_y, "speed": speed, "direction": direction, "color": random.choice(car_colors),"angle": 0}
    cars.append(car)

def move_car(): 
    for car in cars:
        car["y"] += car["speed"] * car["direction"] #moves cars (fix later)

def del_car(): #function to delete cars off screen
    for car in cars[:]: # Iterate over a copy of the list
        if car["y"] < 0 or car["y"] > get_height():
            cars.remove(car)

def check_collision(): #function to check if the player has collided with a car
    player_x = player["x"] + 15 
    player_y = player["y"] + 15 
    player_radius = 15     
    for car in cars: 
        car_x = car["x"] 
        car_y = car["y"] 
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
    x = player["x"]-15 
    y = player["y"]-25 
    boom1 = RotatedRectangle(x,y,40,50,"red",math.radians(45))   
    boom2 = RotatedRectangle(x-5,y,40,50,"red",math.radians(-45)) 
    boom3 = RotatedRectangle(x+5,y+5,10,40,"orange",math.radians(45)) 
    boom4 = RotatedRectangle(x+5,y+5,10,40,"orange",math.radians(-45)) 
    boom5 = RotatedRectangle(x+5,y+5,10,40,"orange",math.radians(0)) 
    boom6 = RotatedRectangle(x+8,y,5,50,"yellow",math.radians(45)) 
    boom7 = RotatedRectangle(x+8,y,5,50,"yellow",math.radians(-45)) 
    boom8 = RotatedRectangle(x+8,y,5,50,"yellow",math.radians(0)) 
    boom9 = RotatedRectangle(x+8,y,5,50,"yellow",math.radians(90)) 

def game_loop(): #game loop function
    global game_over 
    clear_canvas()
    Rectangle(0,0,400,500,"black")
    add_road_lines()
    move_car()
    draw_player()
    draw_cars()
    draw_timer()
    del_car()
    if check_collision(): 
        player["color"] = "red"
        game_over = True 
        timer.clear_interval(game_timer) 
        timer.clear_interval(time) 
        explosion() 
        draw_game_over()
        return

starts = [get_height(),0] #start y values 
player = {"x": 18, "y": get_height()/2, "radius": 15, "color": "green"} #initializing the player piece with its starting x and y values, radius, and color 
document.bind("keydown", move_player) 


randomize_lane_settings() #randomizes the lane settings for the cars
game_timer = timer.set_interval(game_loop, 50) #refreshes game loop every 50 milliseconds
score = timer.set_interval(calculate_score,1000) #every second survived you get a point
timer.set_interval(add_cars, 1000) #calls the add_cars function every second
time = timer.set_interval(timers,1000)#calls timer function to update the timer every second 
 
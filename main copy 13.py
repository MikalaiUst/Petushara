import pygame
pygame.init()
import os
import json
from math import cos,sin,sqrt,pi
from time import time

start = time()
clock = pygame.time.Clock()

tile_size = 100
projectile_size = 20
coin_size = 50

window = pygame.display.set_mode((1200,800))
title = pygame.display.set_caption("LogIn Screen")
base_font = pygame.font.Font(None,56)
title_font = pygame.font.Font(None,120)
background = pygame.image.load("Textures/Backgrounds/LogIn.png")
background = pygame.transform.smoothscale(background, (1200, 800))
field_pic = pygame.image.load("Textures/Buttons/text_field.png")
yes_box = pygame.image.load("Textures/Buttons/green_tick.png")
no_box = pygame.image.load("Textures/Buttons/red_cross.png")
okay_box = pygame.image.load("Textures/Buttons/blue_tick.png")

icon = pygame.image.load("Textures/Backgrounds/icon.png")
pygame.display.set_icon(icon)

wall_sprite = pygame.image.load("Textures/Tiles/tiling_wall.png")
wall_sprite = pygame.transform.smoothscale(wall_sprite, (tile_size, tile_size))
projectile = pygame.image.load("Textures/Objects/standart_bullet.png")
projectile = pygame.transform.smoothscale(projectile, (projectile_size, projectile_size))
turret_top = pygame.image.load("Textures/Objects/Turrets/turret_top.png")
turret_top = pygame.transform.smoothscale(turret_top, (tile_size*1.1, tile_size/2*1.1))
turret_bottom = pygame.image.load("Textures/Objects/Turrets/turret_bottom.png")
turret_bottom = pygame.transform.smoothscale(turret_bottom, (tile_size, tile_size))
wall_sprite = pygame.image.load("Textures/Tiles/tiling_wall.png")
wall_sprite = pygame.transform.smoothscale(wall_sprite, (tile_size, tile_size))

coin = pygame.image.load("Textures/Objects/Coins/coin.png")
coin = pygame.transform.smoothscale(coin, (coin_size, coin_size))


class BaseWindow: # Base class used for all window screens in the program
    # Variable that stores which scene/window the program should switch to next
    transition_to = None
    #basic class constructor, each class will have its own needed  list of variables
    def __init__(self):
        pass
    #method in which all of the visual aspects will be written
    def board(self,surface):
        pass
    #any kind of events like mouse click or key press will be dealt with in this method




    def event_enter(self, event):
        pass

class Message: #Logic for the pop up messages
    def __init__(self,coords:pygame.Rect,button_param,text,is_choice,padding,font_size):
        #sizes of buttons are created in here. They must be the same to not confuse the user
        button_height = button_param[1]
        button_width = button_param[0]
        self.button_1_param = pygame.Rect(0,0,button_width,button_height)
        self.button_2_param = pygame.Rect(0,0,button_width,button_height)
        #the parametres for the textbox itself and
        self.text = text
        self.coords = coords
        self.is_choice = is_choice
        self.padding = padding
        self.font = pygame.font.Font(None,font_size)
        #these variables are support variables used to calculate symbol separation
        self.text_height = self.font.get_height()
        height = self.text_height
        words = text.split()
        text_message = ""
        text_width = 0
       
        for index in range(0,len(words)):
            #Here, the separation symbol is placed so the text fits into a predifined box
            word = words[index]
            if text_width + self.calc_width(word)+self.padding*2 < coords.width:
                #Checks if the added word will fit in line and adds a word to the list
                text_message+= word+" "
                text_width += self.calc_width(" " + word)
            else:
                text_message+="," +word
                text_width = self.calc_width(word)
                height += self.font.get_height()+self.padding

        if padding*2+text_width+button_width*2+40<coords.width:
            #button coordinates instantiation if there is enough space left for both of them
            self.button_1_param.y = height+self.coords.y
            self.button_1_param.x = self.padding*2+text_width+self.coords.x
            self.button_2_param.y = self.button_1_param.y
            self.button_2_param.x = self.coords.x+self.coords.width-self.padding-button_width
        else:                                                
            #button coordinates instantiation if there is not enough space
            self.button_1_param.y = height+self.padding+self.text_height+self.coords.y
            self.button_1_param.x = self.padding*3+self.coords.x
            self.button_2_param.y = self.button_1_param.y
            self.button_2_param.x = self.coords.x+self.coords.width-self.padding*3-button_width
       
        self.coords.height = height+self.text_height+self.button_1_param.height+self.padding*2
        self.text = text_message
        print(self.text)
    def calc_width(self, text):
        #method used to calculate the width of instantiated text
        return self.font.render(text,True,(100,100,100)).get_width()
   




    def board(self, surface):
        #textbox is created with borderlines
        pygame.draw.rect(surface, (255,255,255), self.coords)
        pygame.draw.rect(surface, (0,0,0), self.coords, 2)
        #text is splitted by the separation symbol into lines and drawn one under another
        #text is able to fit within the text box


        y_coordinate = self.coords.y+self.padding
        for line in self.text.rsplit(","):
            surface.blit(self.font.render(line,True,(100,100,100)),(self.coords.x+self.padding,y_coordinate))
            y_coordinate += self.text_height+self.padding
        #checks what type of box is created and what lines are shown (unifinished)
        if self.is_choice == True:
            surface.blit(pygame.transform.smoothscale(yes_box, (self.button_1_param.width, self.button_1_param.height)), (self.button_1_param.x,self.button_1_param.y))
            surface.blit(pygame.transform.smoothscale(no_box, (self.button_2_param.width, self.button_2_param.height)), (self.button_2_param.x,self.button_2_param.y))
        elif self.is_choice == False:
            surface.blit(pygame.transform.smoothscale(okay_box, (self.button_1_param.width, self.button_1_param.height)), (self.button_1_param.x,self.button_1_param.y))
           




    def event_enter(self, event):
        #method that checks what button is pressed and returns a corresponding result
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.is_choice:
                if self.button_1_param.collidepoint(pos):
                    print("Yes")
                    return "yes"
                elif self.button_2_param.collidepoint(pos):
                    print("No")
                    return "no"
            else:
                if self.button_1_param.collidepoint(pos):
                    print("Okay")
                    return "ok"
            return None
                   
class LogInWindow(BaseWindow):
    def __init__(self):
        self.user_response = None
        #messages that will be displayed in this window are declared here
        self.messages = {"incorrect_password_message":Message(pygame.Rect(300,300,800,200),(40,30),"The user with such username already exists. Password to this account is incorrect",True,10,45),
                         "login_proceed_message":Message(pygame.Rect(300,300,800,200),(40,30),"The user with such username already exists. Do you want to proceed with logging in you can access the account now",True,10,45),#
                         "non_existant_username_message":Message(pygame.Rect(300,300,800,200),(40,30),"The user with such username doesn't exist. Do you want to create new account?",True,10,45)}
        self.active_message = "login_proceed_message"
        #background is adjusted to this particular window
        background = pygame.image.load("Textures/Backgrounds/LogIn.png")
        self.background = pygame.transform.smoothscale(background, (1200, 800))
    def board(self,surface):
        #default
        surface.blit(self.background, (0, 0))
        title = title_font.render("Log In",True,(255,255,255))
        surface.blit(title, (450, 60))
        #text_fields from the list are added on the screen
        for t in textfield_list:
            t.board(window)
            #if there is a message activated by user, it is being displayed
        if self.active_message:
            print("one is active right now")
            self.messages[self.active_message].board(surface)
    def event_enter(self, event):
        #system checks if any buttons in the
        if self.active_message:
            result = self.messages[self.active_message].event_enter(event)
            if result in ("yes", "no", "ok"):
                print("User clicked:"+result+" on"+self.active_message+"")
                self.active_message = None  
            return  
        #events are inputed into the text fields area
        for t in textfield_list:
            t.event_enter(event)
        if event.type == pygame.KEYDOWN:
            #if return is pressed a series of checks is made before (unifinished)
            if event.key == pygame.K_RETURN:
                initial_user_data = {
                    "Password":password_field.user_text,
                    "Username":username_field.user_text
                }
                filename = "game_saves/"+initial_user_data["Username"]+".json"
                if not os.path.exists(filename):
                    self.active_message = "non_existant_username_message"
                    self.transition_to = 1
                    with open(filename, "w") as file:
                        json.dump(initial_user_data,file,indent = 4)
                        file.close()
                if os.path.exists(filename):
                    with open(filename, "r") as file:
                        user_data = json.load(file)
                        self.transition_to = 1

class TextArea:

    def __init__(self,field_type,coords:pygame.Rect,preview="",pixel_offset = 0):
        self.field_type = field_type #helps to determine if text won't be shown to the user
        self.preview = preview #what the user will see before clicking on the field
        self.user_text = ''
        self.coords = coords
        self.pixel_offset = pixel_offset
        self.active = False #If the field is selected
        self.highlight_colour = (255,255,255)




    def board(self,surface):
        surface.blit(pygame.transform.smoothscale(field_pic, (self.coords.width, self.coords.height)), (self.coords.x,self.coords.y))
        #if the textfield is active, it will be highlighted
        if self.active:
            pygame.draw.rect(surface,self.highlight_colour,self.coords,5)
        #if user hasnt entered anything yet and the field is unselected, it will have the name of field outputted
        if len(self.user_text)==0 and not self.active:
            text_surface = base_font.render(self.preview,True,(100,100,100))
        else:
            text_surface = base_font.render(self.user_text,True,(255,255,255))
        text_surface_width = text_surface.get_width()
        rect_w = self.coords.width
        #this section allows text to stay within the field as it is being entered
        if text_surface_width> rect_w:
            diff = text_surface_width - rect_w
            height = text_surface.get_height()
            rect = pygame.Rect(diff, 0, rect_w- self.pixel_offset*2, height)
            text_surface = text_surface.subsurface(rect)
        #certain offset is added to the text so it looks more plausible
        x_coord = self.coords.x+self.pixel_offset
        y_coord = self.coords.y + (self.coords.height - text_surface.get_height())/2
        surface.blit(text_surface, (x_coord,y_coord))




    def event_enter(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            #this section adds unicode characters to the message as user is typing them
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key != pygame.K_RETURN:
                self.user_text+=event.unicode
        #allows field to get selected and unselected
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect.collidepoint(self.coords,pygame.mouse.get_pos()):
            self.active = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False

class MainMenuWindow(BaseWindow):
    def __init__(self):
        #buttons are declared and stored in a list
        self.button_list = [
            TranstionButton("levels",pygame.Rect(400,225,400,150),2),
            TranstionButton("leaderboard",pygame.Rect(400,425,400,150),3),
            TranstionButton("save_files",pygame.Rect(400,600,425,150),4)
        ]
    def board(self,surface):
        surface.blit(background, (0, 0))
        #each button from the list is drawn on the screen
        for button in self.button_list:
            button.board(surface)
    def event_enter(self, event):
        #checks if any of the buttons has been pressed by the user
        for button in self.button_list:
            result = button.event_enter(event)
            if result:
                self.transition_to = result
                print(f"Transitioning to: {self.transition_to}")

class TranstionButton:
    def __init__(self,button_pic_name,coords:pygame.Rect, target):
        #button texture is loaded and scaled to fit the given coordinates
        self.button_pic = pygame.image.load("Textures/Buttons/"+ button_pic_name +".png")
        self.button_pic = pygame.transform.smoothscale(self.button_pic, (coords.width, coords.height))
        #coordinates are stored for click detection
        self.coords = coords
        self.target = target
        pass
    def board(self,surface:pygame.Surface):
        #button is drawn at the defined coordinates
        surface.blit(self.button_pic,(self.coords.x,self.coords.y))
       
    def event_enter(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect.collidepoint(self.coords,pygame.mouse.get_pos()):
            return self.target
        return None

class Levels:
    def __init__(self):
        pass
    def board(self,surface):
        pass
    def event_enter(self, event):
        pass

class Level(BaseWindow):
    def __init__(self, level_name):
        # file = open("levels/" + level_name + ".txt", "r")

        #player variables
        self.player_param = 150
        self.player_speed = 15
        self.direction = "left"
        self.sprite_dir = "right"
        self.character_img = pygame.image.load("Textures/user_icons/hero.png")
        self.character_img = pygame.transform.smoothscale(self.character_img, (self.player_param, self.player_param))
        self.coin_num = 0
        self.hp_num = 5
        

        self.offset_x = 0
        self.offset_y = 0
        self.surface_height = 800
        self.surface_width = 1200
        self.player_interface = Player_interface()

        #player stored as a rectangle
        self.player_rect = pygame.Rect(self.surface_width/2-self.player_param/2, self.surface_height/2-self.player_param/2, self.player_param, self.player_param)
        file = open("Textures/levels/" + level_name + ".txt", "r")


        wall_list = []
        self.world_turrets = []
        self.active_projectiles = []
        self.coins =[]
        row_num = 0
       
        for line in file.readlines():
            element_num = 0
            for element in line.strip().split(","):
                x_pos = element_num *tile_size
                y_pos = row_num *tile_size
                if element == "1":
                    wall_list.append(Wall(x_pos,y_pos,tile_size))

                    # print(time()-start,"wall added to the list")
                if element == "3":
                    self.world_turrets.append(Turret(x_pos,y_pos,"simple_turret",tile_size,50))
                if element =="2":
                    self.offset_x = x_pos*tile_size-self.surface_width/2
                    self.offset_y = y_pos*tile_size-self.surface_height/2
                if element == "4":
                    self.coins.append(Coins(x_pos,y_pos))
                if element == "5":
                    self.world_turrets.append(Turret(x_pos,y_pos,tile_size,500,45,self.active_projectiles))
                element_num += 1
            row_num += 1
        self.world_walls = wall_list
           
    def board(self,surface):
        
        current_time = time()
        surface.fill((0, 0, 0))
        
        surface.blit(self.character_img, (self.player_rect.x,self.player_rect.y))
        self.movement()
        for obj in self.world_walls:
            obj.tile_rect.x = obj.world_x - self.offset_x
            obj.tile_rect.y = obj.world_y - self.offset_y
            surface.blit(wall_sprite, obj.tile_rect)

        for turret in self.world_turrets:
            offset = pygame.Vector2(self.offset_x,self.offset_y)
            turret.rect.topleft = turret.pos - offset
            turret.compile_turret(surface,offset)
            if turret.check_collision(self.player_rect.x,self.player_rect.y,self.player_param,offset):
                turret.shoot()
        
        for proj in self.active_projectiles:
            proj.rect.topleft = proj.space_pos - pygame.Vector2(self.offset_x,self.offset_y)
            surface.blit(projectile, proj.rect)
            proj.space_pos += proj.velocity()
            if proj.check_col(self.player_rect):
                self.hp_num -=1
                self.active_projectiles.remove(proj)

        for cur_coin in self.coins:
            offset = pygame.Vector2(self.offset_x,self.offset_y)
            cur_coin.rect.topleft = cur_coin.pos - offset
            surface.blit(coin,cur_coin.rect)
            if cur_coin.check_col(self.player_rect):
                self.coin_num+=1
                self.coins.remove(cur_coin)
        self.player_interface.draw_interface(surface,self.hp_num,self.coin_num)
    def event_enter(self, event :pygame.event):
        pass #66666666666666666666777777777777777777777777777.44444444444444444411111111111111111111111.66666666666666666666111111111111111111.2222222222222222222222
    def movement(self):
        keys_list = pygame.key.get_pressed()
        if keys_list[pygame.K_w]:
            trial_y = self.offset_y - self.player_speed
            if not self.will_collide(self.offset_x,trial_y):
                self.offset_y = trial_y
                self.direction = "up"
        if keys_list[pygame.K_a]:
            trial_x = self.offset_x - self.player_speed
            if not self.will_collide(trial_x,self.offset_y):
                self.offset_x = trial_x
                self.direction = "left"
        if keys_list[pygame.K_s]:
            trial_y = self.offset_y + self.player_speed
            if not self.will_collide(self.offset_x,trial_y):
                self.offset_y = trial_y
                self.direction = "down"
        if keys_list[pygame.K_d]:
            trial_x = self.offset_x + self.player_speed
            if not self.will_collide(trial_x,self.offset_y):
                self.offset_x = trial_x
                self.direction = "right"
    def will_collide(self,test_offset_x,test_offset_y):
        for wall in self.world_walls:
            rect_check = pygame.Rect(wall.world_x-test_offset_x,wall.world_y-test_offset_y,wall.tile_rect.width,wall.tile_rect.height)
            if rect_check.colliderect(self.player_rect):
                print("collision detected")
                return True
        return False

class Wall:
    def __init__(self, x, y, tile_size):
        tile_size = tile_size
        self.world_x = x
        self.world_y = y
        self.tile_rect = pygame.Rect(self.world_x, self.world_y, tile_size,tile_size)
       
        # The tile_rect starts at the world position, but will be updated to screen position later
        self.tile_rect = pygame.Rect(self.world_x, self.world_y, tile_size, tile_size)

class Player_interface:
    def __init__(self):
        self.health_bar_width = 500
        self.coin_icon_size = 30
        self.coin_bar_width = 150
        self.icon_font = pygame.font.Font("Textures/Fonts/PressStart2P-Regular.ttf",25)

        heart_bar = pygame.image.load("Textures/Interface/heart_bar.png")
        self.heart_bar_img = pygame.transform.smoothscale(heart_bar, (self.health_bar_width, self.health_bar_width/5))
        heart_icon = pygame.image.load("Textures/Interface/heart.png")
        self.heart_icon = pygame.transform.smoothscale(heart_icon, (self.health_bar_width/5.9, self.health_bar_width/8.5))
        self.health_bar_pos = pygame.Vector2(20,30)
        self.health_bar_rect = pygame.Rect(self.health_bar_pos,(self.heart_bar_img.get_width(),self.heart_bar_img.get_height()))

        self.coin_icon = pygame.transform.smoothscale(coin, (self.coin_icon_size, self.coin_icon_size))
        self.coin_bar_pos = pygame.Vector2(900,30)
        coin_bar = heart_icon = pygame.image.load("Textures/Interface/coin_bar.png")
        self.coin_bar_icon = pygame.transform.smoothscale(coin_bar, (self.coin_bar_width,self.coin_bar_width/2))
    
    def draw_interface(self,surface,hp_num,coin_num):
        
        surface.blit(self.heart_bar_img,self.health_bar_rect)
        for heart in range(0,hp_num):
            heart_pos = self.health_bar_pos+pygame.Vector2(self.health_bar_width/17,self.health_bar_width/21.3)+pygame.Vector2(self.health_bar_width/5.6,0)*heart
            heart_rect = pygame.Rect(heart_pos,(self.heart_icon.get_width(),self.heart_icon.get_height()))
            surface.blit(self.heart_icon,heart_rect)
        surface.blit(self.coin_bar_icon,pygame.Rect(self.coin_bar_pos,(self.coin_bar_icon.get_width(),self.coin_bar_icon.get_height())))
        coin_icon_rect = pygame.Rect(self.coin_bar_pos,(self.coin_icon_size,self.coin_icon_size))
        coin_icon_rect.center = self.coin_bar_pos+pygame.Vector2(self.coin_bar_width/4,self.coin_bar_icon.get_height()/2)
        surface.blit(self.coin_icon,coin_icon_rect)

        coin_count_text = self.icon_font.render("x"+str(coin_num),True,(255,255,255))
        coin_count_rect = pygame.Rect(self.coin_bar_pos,(coin_count_text.get_width(),coin_count_text.get_height()))
        coin_count_rect.center = self.coin_bar_pos+pygame.Vector2(self.coin_bar_icon.get_width()*0.7,self.coin_bar_icon.get_height()/2)
        surface.blit(coin_count_text,coin_count_rect)
        
        

class Turret:
    def __init__(self, x, y, tile_sizer,ranger,angle,bullet_list):
        self.pos = pygame.Vector2(x,y)
        self.tile_size = tile_sizer
        self.angle = angle
        self.shoot_range = ranger
        self.state = "INACTIVE"
        self.bullet_list = bullet_list

        self.current_time = 0
        self.theta = 0
        self.shoot_delay = 0.2
        self.shoot_num = 30
        self.round_delay = 2
        self.round_delay_temp = self.round_delay
        
        self.shoot_point = pygame.Vector2(0,0)
        self.rect = pygame.Rect(x, y, tile_size,tile_size)
        
    def compile_turret(self, surface,offset):
        surface.blit(turret_bottom, self.rect)

        rotated_image = pygame.transform.rotate(turret_top, self.angle)

        new_rect = rotated_image.get_rect()
        
        # 2.3 Calculate Center: Find the center point of the turret on the screen
        turret_center_screen = self.rect.topleft + pygame.Vector2(self.tile_size/1.80,self.tile_size/20)
        barrel_offset = pygame.Vector2(self.tile_size/2, 0)
        # 2.4 Preserve the Center: Set the center of the new rect to the screen center
        new_rect.center = turret_center_screen
        self.shoot_point=pygame.Vector2(new_rect.centerx,new_rect.centery)+barrel_offset.rotate(-self.angle)+offset
        
        
        # 2.5 Blit (Draw): Draw the rotated image using the new rect
        surface.blit(rotated_image, new_rect)
        # pygame.draw.line(surface,(255,255,255),new_rect.center,self.shoot_point,3)

        self.theta +=5

    def check_collision(self,player_x,player_y,player_d,offset):
        player_x = player_x+player_d/2
        player_y = player_y + player_d/2
        circle_pos = self.pos+pygame.Vector2(tile_size,tile_size)/2-offset
        pos_dif = circle_pos - pygame.Vector2(player_x,player_y)
        pygame.draw.circle(window,(255,0,0),circle_pos,self.shoot_range,20)
        # pygame.draw.line(window,(200,200,200),pygame.Vector2(player_x,player_y),circle_pos,3)
        if pos_dif.length()<=player_d/2+self.shoot_range:
            # print("this player is entering the circle")
            if self.state == "INACTIVE":
                self.current_time = time()-self.round_delay
                print(self.current_time)
            self.state = "SHOOTING"
            return True
        else:
            self.state = "INACTIVE"
            self.round_delay_temp=self.round_delay
            return False
    def shoot(self):
        cycle_time = self.round_delay+self.shoot_delay*self.shoot_num
        time_var=time()-self.current_time

        if time_var<=cycle_time:
            if time_var>self.round_delay_temp:
                angle_rad = self.angle*pi/180
                self.bullet_list.append(Oscilating_Projectile(self.shoot_point,-angle_rad,1))
                print("SHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                self.round_delay_temp += self.shoot_delay
        else:
            self.current_time = time()
            self.round_delay_temp = self.round_delay
        print("Constant:",self.round_delay)
        print("Temp:",self.round_delay_temp)
    def target():
        pass

class Projectile:
    def __init__(self, center_pos, angle, speed):
        self.space_pos = center_pos-pygame.Vector2(0,projectile_size/2)
        self.angle = angle
        self.speed = speed
        self.theta = 0
        self.theta_increase = 1/10
        self.rect = pygame.Rect(0, 0, projectile_size, projectile_size)
        self.rect.center = self.space_pos
    def velocity(self):
        x = self.speed
        y = 0
        return pygame.Vector2(x,y).rotate_rad(self.angle)
    def check_col(self,player_rect):
        return self.rect.colliderect(player_rect)
        
class Oscilating_Projectile(Projectile):
    def velocity(self):
        x = self.speed
        y = sin(self.theta)*self.speed*5
        self.theta += self.theta_increase
        return pygame.Vector2(x,y).rotate_rad(self.angle)

class Rose_Projectile(Projectile):
    def velocity(self):
        r = self.speed*sin(self.theta*3)
        x = r*cos(self.theta)
        y = r*sin(self.theta)
        self.theta += self.theta_increase  
        return pygame.Vector2(x,y).rotate_rad(self.angle)
        
class Spiral_Projectile(Projectile):
    def velocity(self):
        r = self.theta*self.speed
        x = r*cos(self.theta)
        y = r*sin(self.theta)
        self.theta += pi*self.theta_increase
        return pygame.Vector2(x,y)

class Coins:
    def __init__(self, x, y):
        self.pos=pygame.Vector2(x,y)+pygame.Vector2(tile_size/2,tile_size/2)-pygame.Vector2(coin_size/2,coin_size/2)
        self.rect = pygame.Rect(self.pos, (coin_size, coin_size))
        self.value = 1
        
    def check_col(self,player_rect):
        return self.rect.colliderect(player_rect)




#textfield objects are created for username and password input
password_field = TextArea("Password",pygame.Rect(200,500,800,100),"Password",50)
username_field = TextArea("Username",pygame.Rect(200,300,800,100),"Username",50)
textfield_list = [password_field,username_field]


LogIn_Screen = LogInWindow()       #login screen with username/password fields and messages
MainMenu_Screen = MainMenuWindow() #main menu where user chooses what to do next
Level_1 = Level("level_1")              #placeholder for the first level of the game
Window_list = [LogIn_Screen,MainMenu_Screen,Level_1]

#this variable defines which scene is currently active (0 = LogIn, 1 = MainMenu, 2 = Level_1, etc.)
current_scene = 2

run = True
while run:
    scene = Window_list[current_scene]
    for event in pygame.event.get():
        if event.type == pygame.QUIT or scene.transition_to==100:
            run = False
        scene.event_enter(event)
    scene.board(window)
    pygame.display.update()
    #if the scene's paramtre tranistion_to is something, it transtions to other scene
    if scene.transition_to is not None:
        current_scene = scene.transition_to
        scene.transition_to = None
    clock.tick(60)
pygame.quit()
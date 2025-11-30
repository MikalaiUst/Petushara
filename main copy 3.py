import pygame

pygame.init()

import sys
import os
import json
from textfield import TextArea

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

class BaseWindow:
    def __init__(self):
        pass
    def board(self,surface):
        pass
    def event_enter(self, event):
        pass


class Message:
    def __init__(self,coords:pygame.Rect,button_param,text,is_choice,padding,font_size):

        button_height = button_param[1]
        button_width = button_param[0]
        self.button_1_param = pygame.Rect(0,0,button_width,button_height)
        self.button_2_param = pygame.Rect(0,0,button_width,button_height)
        self.text = text
        self.coords = coords
        self.is_choice = is_choice
        self.padding = padding
        self.font = pygame.font.Font(None,font_size)
        self.text_height = self.font.get_height()
        height = self.text_height

        words = text.split()
        text_message = ""
        text_width = 0
        
        for index in range(0,len(words)):
            word = words[index]
            # print(word)
            # print(text_width)
            # print(coords.width)
            # print("----------------------------------------------------")
            if text_width + self.calc_width(word)+self.padding*2 < coords.width:
                # print("yes, length of message:"+str(self.font.render(text_message + " "+word,True,(100,100,100)).get_width()))
                text_message+= word+" "
                text_width += self.calc_width(" " + word)
            else:
                text_message+="," +word
                # print("no, length of message:"+str(self.font.render(text_message + " "+word,True,(100,100,100)).get_width()))
                text_width = self.calc_width(word)
                height += self.font.get_height()+self.padding

        
        if padding*2+text_width+button_width*2+40<coords.width: #button instantiation if there is enough space
            self.button_1_param.y = height+self.coords.y
            self.button_1_param.x = self.padding*2+text_width+self.coords.x
            self.button_2_param.y = self.button_1_param.y
            self.button_2_param.x = self.coords.x+self.coords.width-self.padding-button_width
        else:                                                #button instantiation if there is enough space
            self.button_1_param.y = height+self.padding+self.text_height+self.coords.y
            self.button_1_param.x = self.padding*3+self.coords.x
            self.button_2_param.y = self.button_1_param.y
            self.button_2_param.x = self.coords.x+self.coords.width-self.padding*3-button_width
        

        self.coords.height = height+self.text_height+self.button_1_param.height+self.padding*2
        self.text = text_message
        # self.coords = pygame.Rect(coords.x,coords.y, )
        print(self.text)
    def calc_width(self, text):
        return self.font.render(text,True,(100,100,100)).get_width()
    def change_text(self,new_text):
        pass
    

    def board(self, surface):
        pygame.draw.rect(surface, (255,255,255), self.coords)
        pygame.draw.rect(surface, (0,0,0), self.coords, 2)
        y_coordinate = self.coords.y+self.padding
        for line in self.text.rsplit(","):
            surface.blit(self.font.render(line,True,(100,100,100)),(self.coords.x+self.padding,y_coordinate))
            y_coordinate += self.text_height+self.padding
        if self.is_choice == True:
            surface.blit(pygame.transform.smoothscale(yes_box, (self.button_1_param.width, self.button_1_param.height)), (self.button_1_param.x,self.button_1_param.y))
            surface.blit(pygame.transform.smoothscale(no_box, (self.button_2_param.width, self.button_2_param.height)), (self.button_2_param.x,self.button_2_param.y))
        elif self.is_choice == False:
            surface.blit(pygame.transform.smoothscale(okay_box, (self.button_1_param.width, self.button_1_param.height)), (self.button_1_param.x,self.button_1_param.y))
            
        


    def event_enter(self, event):
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
                    


incorrect_password_message = Message(pygame.Rect(300,300,800,200),(40,30),"The user with such username already exists. Password to this account is incorrect",True,10,45)
login_proceed_message = Message(pygame.Rect(300,300,800,200),(40,30),"The user with such username already exists. Do you want to proceed with logging in, you can access the account now",True,10,45)
non_exixtant_username_message = Message(pygame.Rect(300,300,800,200),(40,30),"The user with such username doesn't exist, do you want to create new account?",True,10,45)
class LogInWindow(BaseWindow):
    def __init__(self):
        self.user_response = None
        self.active_message = None
        pass
    def board(self,surface):
        surface.blit(background, (0, 0))
        title = title_font.render("Log In",True,(255,255,255))
        surface.blit(title, (450, 60))
        for t in textfield_list:
            t.board(window)
        if self.active_message:
            self.active_message.board(surface)
        
        message.board(surface)
    def event_enter(self, event):
        for t in textfield_list:
            t.event_enter(event)
        result = message.event_enter(event)
        print(result)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                initial_user_data = {
                    "Password":password_field.user_text,
                    "Username":username_field.user_text
                }
                filename = "game_saves/"+initial_user_data["Username"]+".json"
                if not os.path.exists(filename):
                    with open(filename, "w") as file:
                        json.dump(initial_user_data,file,indent = 4)
                        file.close()
                if os.path.exists(filename):
                    with open(filename, "r") as file:
                        user_data = json.load(file)

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
        if self.active:
            pygame.draw.rect(surface,self.highlight_colour,self.coords,5)

        if len(self.user_text)==0 and not self.active:
            text_surface = base_font.render(self.preview,True,(100,100,100))
        else:
            text_surface = base_font.render(self.user_text,True,(255,255,255))
        text_surface_width = text_surface.get_width()
        rect_w = self.coords.width
        if text_surface_width> rect_w:
            diff = text_surface_width - rect_w
            height = text_surface.get_height()
            rect = pygame.Rect(diff, 0, rect_w- self.pixel_offset*2, height)
            text_surface = text_surface.subsurface(rect)
        x_coord = self.coords.x+self.pixel_offset
        y_coord = self.coords.y + (self.coords.height - text_surface.get_height())/2
        surface.blit(text_surface, (x_coord,y_coord))

    def event_enter(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif event.key != pygame.K_RETURN:
                self.user_text+=event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect.collidepoint(self.coords,pygame.mouse.get_pos()):
            self.active = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False



password_field = TextArea("Password",pygame.Rect(200,500,800,100),"Password",50)
username_field = TextArea("Username",pygame.Rect(200,300,800,100),"Username",50)
textfield_list = [password_field,username_field]

LogIn_Screen = LogInWindow()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        LogIn_Screen.event_enter(event)
                        

    LogIn_Screen.board(window)
    
    pygame.display.update()
pygame.quit()

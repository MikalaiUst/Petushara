import pygame
import sys
import os
import json

pygame.init()

window = pygame.display.set_mode((1200,800))
title = pygame.display.set_caption("LogIn Screen")

base_font = pygame.font.Font(None,56)
title_font = pygame.font.Font(None,120)
background = pygame.image.load("Textures/Backgrounds/LogIn.png")
background = pygame.transform.smoothscale(background, (1200, 800))
field_pic = pygame.image.load("Textures/Buttons/text_field.png")

class BaseWindow:
    def __init__(self):
        pass
    def board(self,surface):
        pass
    def event_enter(self, event):
        pass

class LogInWindow(BaseWindow): #This class shows the first thing that the user sees
    def __init__(self):
        password_field = TextArea("Password",pygame.Rect(200,500,800,100),"Password",50)
        username_field = TextArea("Username",pygame.Rect(200,300,800,100),"Username",50)
        self.textfield_list = [password_field,username_field]
        pass
    def board(self,surface):
        surface.blit(background, (0, 0))
        title = title_font.render("Log In",True,(255,255,255))
        surface.blit(title, (450, 60))
        for t in self.textfield_list: #all pre-declared textfields are drawn
            t.board(window)
    def event_enter(self, event):
        for t in self.textfield_list:
            t.event_enter(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                initial_user_data = {
                    "Password":self.textfield_list[0].user_text,
                    "Username":self.textfield_list[1].user_text
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



LogIn_Screen = LogInWindow()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        for t in textfield_list:
            t.event_enter(event)
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
                        

    
    window.blit(background, (0, 0))
    title = title_font.render("Log In",True,(255,255,255))
    window.blit(title, (450, 60))
    for t in textfield_list:
        t.board(window)
    pygame.display.update()
pygame.quit()
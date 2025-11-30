import pygame

base_font = pygame.font.Font(None,56)
title_font = pygame.font.Font(None,120)
background = pygame.image.load("Textures/Backgrounds/LogIn.png")
background = pygame.transform.smoothscale(background, (1200, 800))
field_pic = pygame.image.load("Textures/Buttons/text_field.png")

class TextArea:
    def __init__(self,field_type,coords:pygame.Rect,preview=""):
        self.field_type = field_type #helps to determine if text won't be shown to the user
        self.preview = preview #what the user will see before clicking on the field
        self.user_text = ''
        self.coords = coords
        self.active = False #If the field is selected
        self.highlight_colour = (0,0,0)

    def board(self,surface):
        surface.blit(pygame.transform.smoothscale(field_pic, (self.coords.width, self.coords.height)), (self.coords.x,self.coords.y))
        if self.active:
            pygame.draw.rect(surface,self.highlight_colour,self.coords,5)

        if len(self.user_text)==0 and not self.active:
            text_surface = base_font.render(self.preview,True,(100,100,100))
        else:
            text_surface = base_font.render(self.user_text,True,(255,255,255))
        width = text_surface.get_width()

        x_coord = self.coords.x+50
        y_coord = self.coords.y + (self.coords.height - text_surface.get_height())/2
        surface.blit(text_surface, (x_coord,y_coord))

    def event_enter(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else:
                self.user_text+=event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect.collidepoint(self.coords,pygame.mouse.get_pos()):
            self.active = True
            self.highlight_colour = (255,255,0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.active = False
            self.highlight_colour = (0,0,0)
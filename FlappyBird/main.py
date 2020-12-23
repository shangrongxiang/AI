import pygame
import neat
import os
pygame.init()
win_width = 300
win_height = 400
'''
导入所需要的图片
impor imgs we are going to use next step！ pygame.image.load(os.path.join("img","bird1.png"))) img is a folder in this folder
'''
bird_imgs = [pygame.image.load(os.path.join("img","bird1.png")),pygame.image.load(os.path.join("img","bird2.png")),pygame.image.load(os.path.join("img","bird3.png"))]
pipe = pygame.image.load(os.path.join("img","pipe.png"))
bg = pygame.image.load(os.path.join("img","bg.png"))
base = pygame.image.load(os.path.join("img","base.png"))

'''
create a bird class 
x and y determine the postion of the bird
创建bird 类，x 和 y 决定了 bird的位置 y is also height
vel is down speed
vel是bird想下的速度
'''
class Bird:
    imgs = bird_imgs
    rot_vel = 20
    max_rotation = 25
    animation = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]
    
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    '''
d是指原始位置到移动后的（跳）上下移动的距离 
'''
    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5*self.tick_count**2
        if d >= 16:##当下降了16是，不在加速。
            d = 16

        if d < 0:##当 d在上升时，做减速。
            d -= 2 

        self.y += d
        
        if d < 0 or self.y < self.height+50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel

    def draw(self,win):
        self.img_count += 1
        if self.img_count <self.animation*2:
            self.img = self.imgs[0]
        elif self.img_count < self.animation*3:
            self.img = self.imgs[1]
        elif self.img_count < self.animation*4:
            self.img = self.imgs[2]
        elif self.img_count == self.animation*4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.animation*2

        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw(win,bird):
    win.blit(bg,(0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((win_width,win_height))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw(win,bird)
    pygame.quit()
    quit()

main()




bird = Bird(50,300)
while run:
    bird.move
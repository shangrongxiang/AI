import pygame
import neat
import os
import random
import time
pygame.font.init()
pygame.init()
win_width = 290
win_height = 500
gen = 0
'''
导入所需要的图片
impor imgs we are going to use next step！ pygame.image.load(os.path.join("img","bird1.png"))) img is a folder in this folder

'''
bird_imgs = [pygame.image.load(os.path.join("img","bird1.png")),pygame.image.load(os.path.join("img","bird2.png")),pygame.image.load(os.path.join("img","bird3.png"))]
pipe = pygame.image.load(os.path.join("img","pipe.png"))
bg = pygame.image.load(os.path.join("img","bg.png"))
base = pygame.image.load(os.path.join("img","base.png"))
stat_font = pygame.font.SysFont("None",30)
'''
create a bird class 
x and y determine the postion of the bird
创建bird 类，x 和 y 决定了 bird的位置 y is also height
vel is down speed
vel是bird想下的速度
'''
class Bird():
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
        self.vel = -3
        self.tick_count = 0
        self.height = self.y
    '''
d是指原始位置到移动后的（跳）上下移动的距离 
'''
    def move(self):
        self.tick_count += 1

        d = self.vel * (self.tick_count) + 0.5*self.tick_count**2
        if d >= 16:##当下降了16是，不在加速。
            d = (d/abs(d)) * 16

        if d < 0:##当 d在上升时，做减速。
            d -= 1 

        self.y = self.y +  d
        
        if d < 0 or self.y < self.height+50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel

    def draw(self,win):
        self.img_count += 1
        if self.img_count <= self.animation:
            self.img = self.imgs[0]

        if self.img_count <self.animation*2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation*3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation*4:
            self.img = self.imgs[1]
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
class Pipe():
    gap = 200
    vel = 3
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.button = 0
        self.pipe_top = pygame.transform.flip(pipe,False,True)
        self.pipe_button = pipe

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(150,300)
        self.top = self.height - self.pipe_top.get_height()
        self.button = self.height + self.gap
    
    def move(self):
        self.x -= self.vel
    
    def draw(self,win):
        win.blit(self.pipe_top,(self.x,self.top))
        win.blit(self.pipe_button,(self.x,self.button))

    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        button_mask = pygame.mask.from_surface(self.pipe_button)

        top_offset = (self.x-bird.x,self.top - round(bird.y))
        button_offset = (self.x-bird.x,self.button-round(bird.y))

        b_point = bird_mask.overlap(button_mask,button_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True
        return False

class Base():
    vel = 3
    width = base.get_width()
    img = base

    def __init__(self,y):
        self.y = y
        self.x1 = 0

        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 < self.width * -1:
            self.x1 = self.x2 + self.width

        if self.x2 < self.width * -1:
            self.x2 = self.x1 + self.width

    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))

    



def draw(win,birds,pipes,base,score,gen,numberofBirds):
    win.blit(bg,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    text = stat_font.render("Score: " + str(score),1,(255,255,255))
    win.blit(text,(win_width-10-text.get_width(),10))

    text1 = stat_font.render("Gen: " + str(gen),1,(255,255,255))
    win.blit(text1,(10,10))

    text2 = stat_font.render("Birds: " + str(numberofBirds),1,(255,255,255))
    win.blit(text2,(10,30))
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def main(genomes,config):
    
    global gen
    gen += 1
    score = 0
    nets = []
    ge = []
    birds = []
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(90,200))
        g.fitness = 0
        ge.append(g)


    base = Base(450)
    
    pipes = [Pipe(200)]
    win = pygame.display.set_mode((win_width,win_height))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        add_pipe = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        ##bird.move()
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipeind = 1
        else:
            run = False
            break
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.5

            output = nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].height),abs(bird.y-pipes[pipe_ind].button)))
            if output[0] > 0.3:
                bird.jump()
        rem = []
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 100
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
           
            if pipe.x + pipe.pipe_top.get_width() < 0:
                rem.append(pipe)
            
            
            pipe.move()
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness +=   score*1.2 + 3
            pipes.append(Pipe(300))
        for r in rem:
            
            pipes.remove(r)

        for x,bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 440 or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
        base.move()
        draw(win,birds,pipes,base,score,gen,len(birds))

    


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,
    neat.DefaultStagnation,config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    status = neat.StatisticsReporter()
    p.add_reporter(status)

    winner = p.run(main,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)

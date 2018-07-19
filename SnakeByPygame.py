
#程序头部
# coding = utf-8
import pygame                             #调用pygame库     
from pygame.locals import *               #调用pygame常量，如K_LEFT    
from sys import exit                      #exit()用来退出进程       
from random import randint,sample,choice  #调用随机函数    
import math                               #调用数学函数，建立模型  
import time                               #调用时间模块，用来延时
import os                                 #调用os模块，用于系统文件路径获取


#类定义
#---------------------------------------------------------------------------------------------------------------------------------------------

#定义草地类模板
class GrassMap(object):
   
    def __init__(self,color,living_space):          
        self.living_space = living_space
        self.color = color

    
    def generate(self,surface):
        grass_Rect = pygame.Rect(self.living_space)
        surface.fill(self.color,grass_Rect)

#----------------------------------------------------------------------------------------------------------------------------------------------

#定义食物类模板
class Food(object):

    #类实例化时传递参数 
    def __init__(self,color,size,living_space):
        self.color = color
        self.size  = size
        self.living_space = living_space      

    #在地图中随机生成食物
    def generate(self,snakebody):
       
        cell_width  = int(self.living_space[2]//self.size)
        cell_height = int(self.living_space[3]//self.size)
        cell_x = int(self.living_space[0]//self.size )
        cell_y = int(self.living_space[1]//self.size)

        x_area = range(cell_x ,cell_x + cell_width - 1)
        y_area = range(cell_y ,cell_y + cell_height - 1)
        xy_area = [(x,y) for x in x_area for y in y_area]

        snake_x = []
        snake_y = []
        for i in range(len(snakebody)):
            snake_x.append(snakebody[i][0]//self.size)
            snake_y.append(snakebody[i][1]//self.size)
        snake_xy = list(zip(snake_x,snake_y))
                
        (x,y) = choice([(x,y) for (x,y) in xy_area if (x,y) not in snake_xy ])
        #print('x:',[x for x in x_area if x not in snake_x ])
        #print('y:',[y for y in y_area if y not in snake_y ])
        self._food_pos = [(x,y)]
    

    #判定食物是否存在，若不存在则随机生成食物  
    def if_exist(self,exist,snakebody):
        if exist == 'be eaten':
            del self._food_pos[0]
            self.generate(snakebody)
            #print('rebuild food!')
            

    #画出食物   
    def draw(self,surface,*args):
        collide_flag = 0
        x = self._food_pos[0][0]*self.size
        y = self._food_pos[0][1]*self.size
        food_Rect = pygame.Rect(x,y,self.size,self.size)
        try:
            if food_Rect.collidelist(args[0]) != -1:
                #print(snake_Rect)
                #print(args[0])
                #print(snake_Rect.collidelist(args[0]))
                collide_flag = 1

        except IndexError:
            pass

        if collide_flag == 1:
            self.generate(args[1])
        else:pass
        
        pygame.draw.rect(surface,self.color,food_Rect)

#--------------------------------------------------------------------------------------------------------------------------------------------------

#定义贪吃蛇类模板
class Snake(object):

    #类实例化时传递参数   
    def __init__(self,color,length,size,living_space):                                      
        self.color  = color
        self.length = length
        self.size   = size
        self.living_space = living_space

    #贪吃蛇初始化   
    def generate(self):

        init_x              = self.living_space[0]
        init_y              = self.living_space[1] + self.living_space[3] - self.size

        self.snake_body  = [[x*self.size+init_x,init_y-60] for x in range(self.length)]
        #print('generate:',self.snake_body)

    #贪吃蛇移动
    def move(self,DIRECTION,foodbody):
        global SNAKE_BODY_STAY
        SNAKE_BODY_STAY = self.snake_body.copy()
        self.foodstate = 'not be eaten'
        #print('before mvoe:',self.snake_body)
        if  DIRECTION=='LEFT':
            self.snake_body.append([self.snake_body[len(self.snake_body)-1][0] - self.size,\
                                    self.snake_body[len(self.snake_body)-1][1]]) 
            if self.eatfood(foodbody):
                self.foodstate = 'be eaten'
            else:
                del self.snake_body[0]  

        elif DIRECTION=='RIGHT':
            self.snake_body.append([self.snake_body[len(self.snake_body)-1][0] + self.size,\
                                    self.snake_body[len(self.snake_body)-1][1]])
            if self.eatfood(foodbody):
                self.foodstate = 'be eaten'
            else:
                del self.snake_body[0]  

        elif DIRECTION=='UP':
            self.snake_body.append([self.snake_body[len(self.snake_body)-1][0],\
                                    self.snake_body[len(self.snake_body)-1][1] - self.size])                
            if self.eatfood(foodbody):
                self.foodstate = 'be eaten'
            else:
                del self.snake_body[0]  

        elif DIRECTION=='DOWN':
            self.snake_body.append([self.snake_body[len(self.snake_body)-1][0],\
                                    self.snake_body[len(self.snake_body)-1][1] + self.size])                
            if self.eatfood(foodbody):
                self.foodstate = 'be eaten'
            else:
                del self.snake_body[0]
        #print(self.snake_body)


    #贪吃蛇死亡判定
    def isdead(self):
        #条件1——贪吃蛇撞墙
        if (self.snake_body[len(self.snake_body)-1][0] == self.living_space[0] - self.size or \
            self.snake_body[len(self.snake_body)-1][0] == self.living_space[0] + self.living_space[2])\
        or (self.snake_body[len(self.snake_body)-1][1] == self.living_space[1] - self.size or \
            self.snake_body[len(self.snake_body)-1][1] == self.living_space[1] + self.living_space[3]):
            #print('die for me 1')
            return True
        #条件2——贪吃蛇“追尾”
        for bodynet in self.snake_body[:-1]:
            if bodynet == self.snake_body[len(self.snake_body)-1]:
                #print('bodynet:',bodynet)
                #print('snakebody:',self.snake_body)
                #print('die for me 2')
                return True
            
    #判定贪吃蛇是否吃到食物
    def eatfood(self,foodbody):
        global GETSCORE
        #print('foodbody:',foodbody)
        #print('snakebody:',self.snake_body)

        if foodbody[0][0]*self.size == self.snake_body[len(self.snake_body)-1][0] and \
            foodbody[0][1]*self.size == self.snake_body[len(self.snake_body)-1][1]:
            
            soundeat.play()
            GETSCORE = 1
            #print('eat!')
            return True
        else:
            return False
     

    #画出贪吃蛇
    def draw(self,surface,inner_color,Rlist,life):
        collide_flag = 0
        for bodynet in self.snake_body:
            snake_Rect = pygame.Rect(bodynet[0],bodynet[1],self.size,self.size)
            try:
                if snake_Rect.collidelist(Rlist) != -1:
                    #print(snake_Rect)
                    #print(args[0])
                    #print(snake_Rect.collidelist(args[0]))
                    collide_flag = 1

            except IndexError:
                pass

        if collide_flag == 1:
            #self.snake_body = SNAKE_BODY_STAY
            life -= 1
            if life == 0:
                
                sounddead.play()
                terminate(surface)
            else:
                self.snake_body = [[x*20+0.05*WINDOW_WIDTH,0.9*WINDOW_HEIGHT-20] for x in range(len(self.snake_body))]
                
        else:pass

        for bodynet in self.snake_body:
            if bodynet == self.snake_body[len(self.snake_body)-1]:
                self.color = inner_color
            else: self.color = (170,170,0)

            snake_Rect = pygame.Rect(bodynet[0],bodynet[1],self.size,self.size)         
            inner_Rect = pygame.Rect(bodynet[0]+4,bodynet[1]+4,self.size-8,self.size-8)

            pygame.draw.rect(surface,self.color,snake_Rect)
            pygame.draw.rect(surface,inner_color,inner_Rect)

        return life


#辅助函数
# ======================================================================================================================================================================

#游戏开始界面
def start():
    while True:
    #for _ in range(1):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                 main()           

        screen.fill((0,0,0))

        eggsurface     = pygame.image.load(SNAKE_START)

        font          = pygame.font.SysFont("Arial",30)
        startsurface  = font.render('Enjoy Yourself!',True,(155,48,255))
        startsurface1 = font.render('Press any key to start your game',True,(155,48,255))
        screen.blit(startsurface,(0.38*WINDOW_WIDTH,0.85*WINDOW_HEIGHT))
        screen.blit(startsurface1,(0.26*WINDOW_WIDTH,0.2*WINDOW_HEIGHT))  
        screen.blit(eggsurface,(WINDOW_WIDTH//2-100,WINDOW_HEIGHT//2-100))

        #drawfire(screen)
        #drawwater(screen)
        #drawice(screen)
        #drawsolid(screen)  
        pygame.display.update()

#游戏结束界面
def terminate(screen): 
        font         = pygame.font.SysFont("Arial",30)
        startsurface  = font.render('Please press the keyboard SPACE to restart',True,(135,206,250))
        gameover = pygame.image.load(GAMEOVER)
        gameover_scale = pygame.transform.scale(gameover,(400,100))
        screen.fill((0,0,0))
        screen.blit(startsurface,(0.21*WINDOW_WIDTH,0.7*WINDOW_HEIGHT))
        screen.blit(gameover_scale,(200,230))
        pygame.display.update()
        while True:
            for event in pygame.event.get():   
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:    
                    if event.key == K_SPACE:
                        main()

#随机地形常量生成函数
def terrain(n1,n2,s1,s2,r1,r2):
    number = randint(n1,n2)
    sampx = sample([x*s1 for x in range(1,r1)],number)
    sampy = sample([y*s2 for y in range(1,r2)],number)
    return [number,sampx,sampy]

#画出随机地形——火
def drawfire(screen,number,sampx,sampy):
    X = []
    Y = []
    fireRlist = []
    for k in range(number):
        FX = [0,15,20,25,40,25,15]
        FY = [10,25,0,25,10,40,40]
        var_x = sampx[k]
        var_y = sampy[k]
        for i in range(len(FX)):
            FX[i] += var_x
        X.append(FX)
        for j in range(len(FY)):
            FY[j] += var_y
        Y.append(FY)
    for i in range(number):
        pointlist = list(zip(X[i],Y[i]))
        pygame.draw.polygon(screen,(255,0,0),pointlist)
        fireR = pygame.Rect(X[i][0],Y[i][2],40,40)
        fireRlist.append(fireR)

    return fireRlist

#画出随机地形——水
def drawwater(screen,number,sampx,sampy):
    X = []
    Y = []
    waterRlist = [] 
    for k in range(number):
        FX = [0,100,0,100]
        FY = [0,0,40,40]
        var_x = sampx[k]
        var_y = sampy[k]
        for i in range(len(FX)):
            FX[i] += var_x
        X.append(FX)
        for j in range(len(FY)):
            FY[j] += var_y
        Y.append(FY)

    for i in range(number):
        pointlist = list(zip(X[i],Y[i]))
        pygame.draw.lines(screen,(0,0,255),False,pointlist)
        waterR = pygame.Rect(X[i][0],Y[i][0],100,40)
        waterRlist.append(waterR)

    return waterRlist

#画出随机移动地形——冰
def drawice(screen,number,sampx,sampy):
    iceRlist = []
    clock    = pygame.time.Clock()
    timepass = clock.tick(60)

    for i in range(number):    
        sampy[i] += 2
        if sampy[i]>600:
            sampy[i] = 0
    for i in range(number):
        x_pos = sampx[i]
        y_pos = sampy[i]
        pygame.draw.circle(screen,(135,206,255),(x_pos,y_pos),20)
        iceR = pygame.Rect(sampx[i]-20,sampy[i]-20,40,40)
        iceRlist.append(iceR)

    return iceRlist
        
#画出随机移动地形——土
def drawsolid(screen,number,sampx,sampy):    
    clock    = pygame.time.Clock()
    timepass = clock.tick(60)
    solidRlist = []
    for i in range(number):
        sampx[i] +=2
        if sampx[i]>800:
            sampx[i] = 0
    for i in range(number):
        SOLID_POS = (sampx[i],sampy[i],80,40)
        SOLID_RECT = pygame.Rect(SOLID_POS)
        pygame.draw.rect(screen,(205,201,165),SOLID_RECT)
        solidR = SOLID_RECT
        solidRlist.append(solidR)

    return solidRlist

#设置传送门（普通模式到噩梦模式）
def gateway(surface,area,score,goal,snakebody):
    global GATEWAY_FLAG
    size = 40
    if score >= goal//2:
        x  = area[0]
        y  = area[1]
        gateR    = pygame.Rect(x,y,size,size)
        headbody = snakebody[len(snakebody)-1]
        headR    = pygame.Rect(headbody[0],headbody[1],20,20)
        
        if headR.colliderect(gateR):
            pygame.draw.rect(surface,(0,0,0),gateR)
            GATEWAY_FLAG += 1
        else: pass
    else: pass
            

#普通模式
# ==============================================================================================================================================

def main():

    #传送门标志位
    global GATEWAY_FLAG

    #设定贪吃蛇移动速度    
    SNAKE_SPEED = 13

    #初始贪吃蛇移动方向
    DIRECTION     = 'RIGHT'

    #进入下一关需要的分数
    goal = 12

    #实例化草地
    grass = GrassMap(GRASS_COLOR,LIVING_SPACE)
    
    #实例化食物
    food  = Food(FOOD_COLOR,SIZE,LIVING_SPACE)

    #实例化贪吃蛇
    snake = Snake(SNAKE_COLOR,SNAKE_LENGTH,SIZE,LIVING_SPACE)

    #实例出控制帧数的对象clock
    clock = pygame.time.Clock()

    #初始化贪吃蛇
    snake.generate()

    #获取贪吃蛇坐标
    snakebody = snake.snake_body        

    #随机生成食物
    food.generate(snakebody)

    #获取背景音乐的路径
    BGMpath = os.getcwd() + '//' + 'BGM.ogg'
    #加载背景音乐
    pygame.mixer.music.load(BGMpath)
    #循环播放背景音乐
    pygame.mixer.music.play(-1)

    while True:
    #for _ in range(8):
        
        #print('while start')

        #进入传送门的过程限制移动
        if GATEWAY_FLAG == 1:
            pygame.event.set_blocked(KEYDOWN)

        #获取事件
        event = pygame.event.poll()       
        #print('get event')
        #print('direction',DIRECTION) 

        #判定事件
        if event.type == QUIT:
            pygame.quit()
            exit()
        #控制贪吃蛇移动方向     
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and DIRECTION != 'RIGHT':
                DIRECTION = 'LEFT'
            elif event.key == K_RIGHT and DIRECTION != 'LEFT':
                DIRECTION = 'RIGHT'
                #print(DIRECTION)
            elif event.key == K_UP and DIRECTION != 'DOWN':
                DIRECTION = 'UP'
            elif event.key == K_DOWN and DIRECTION != 'UP':
                DIRECTION = 'DOWN'
                #print(DIRECTION)

        #控制游戏暂停\继续
            elif event.key == K_SPACE:
                pause_flag = 0
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            exit()

                        if event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                
                                pause_flag = 1

                    if pause_flag == 1:
                        pygame.mixer.music.unpause()
                        break
                    pygame.mixer.music.pause()                            
            
            #加速贪吃蛇
            elif event.key == K_LSHIFT:
                SNAKE_SPEED *= 3
            #print('DIRECTION',DIRECTION)
        #从加速恢复
        elif event.type == KEYUP:
            if event.key == K_LSHIFT:
                SNAKE_SPEED /= 3

        #获取食物坐标           
        foodbody = food._food_pos
        #移动贪吃蛇
        snake.move(DIRECTION,foodbody)      

        #print('before:',food._food_pos,snake.snake_body[snake.head])
        #获取贪吃蛇坐标
        snakebody = snake.snake_body
        #获取食物状态
        exist     = snake.foodstate
        #判定是否随机生成食物
        food.if_exist(exist,snakebody)      
        #print('foodbody:',food._food_pos)
        #print('snakebodyhead:',snake.snake_body[snake.head])

        #判定贪吃蛇是否死亡  
        if snake.isdead():                               
            pygame.mixer.music.stop()
            #print('dead:',snakebody)
            #print('dead',DIRECTION)
            sounddead.play()            
            terminate(screen)
                
        else:
            pass         

        #游戏分数模型
        score = (len(snake.snake_body)-5)*3

        #判定是否进入下一关
        if score == goal:
            time.sleep(0.3)
            hardmode()
        else: pass

        #填充背景     
        screen.fill(BACK_GROUND_FILL)                 

        #显示传送门开启提示
        if score == goal//2:
            font         = pygame.font.SysFont("Arial",20)
            gatesurface = font.render('The Random Warp Gate has opened ', True,(190,190,190))
            screen.blit(gatesurface,(0.2*WINDOW_WIDTH,0.025*WINDOW_HEIGHT)) 
        
        #获取字体对象
        font         = pygame.font.SysFont("Arial",20)
        goalsurface  = font.render('Goal : %s' % goal,True,(0,220,0))
        scoresurface = font.render('Score: %s' % score,True,(0,0,220))

        tip1surface = font.render('Tip1: you can pause/unpause your game by press the keyboard SPACE' ,True,(190,190,190))
        tip2surface = font.render('Tip2: you can speed up/down your snake by do/undo the keyboard LEFT SHIFT' ,True,(190,190,190))

        #画出分数
        screen.blit(scoresurface,(0.8*WINDOW_WIDTH,0.05*WINDOW_HEIGHT))
        screen.blit(goalsurface,(0.8*WINDOW_WIDTH,0.01*WINDOW_HEIGHT))
        #画出提示
        screen.blit(tip1surface,(0.1*WINDOW_WIDTH,0.91*WINDOW_HEIGHT))
        screen.blit(tip2surface,(0.1*WINDOW_WIDTH,0.95*WINDOW_HEIGHT))

        #生成草地
        grass.generate(screen)                       

        #依据传送条件开启传送门
        gateway(screen,area,score,goal,snakebody)             

        #判定是否进行传送
        if GATEWAY_FLAG == 2:
            #恢复贪吃蛇移动锁定
            pygame.event.set_allowed(KEYDOWN)
            GATEWAY_FLAG = 0

            #进入噩梦模式
            nightmode()      
        else: pass

        #画出贪吃蛇
        snake.draw(screen,SNAKE_INNER_COLOR,[],1)         
        #画出食物
        food.draw(screen)
        #刷新
        pygame.display.update()                      
        #print('update')

        #维持传送门存在1s
        if GATEWAY_FLAG ==1:
            time.sleep(1)
        time_passed = clock.tick(SNAKE_SPEED)         

#困难模式    
# ==================================================================================================================================


def hardmode():
    #困难模式贪吃蛇身体颜色
    snakecolor = (200,200,0)

    #设全局变量辅助判定生命加一条件
    global GETSCORE
    GETSCORE = 0

    #初始贪吃蛇生命
    LIFE     = 1

    #加速键K_LSHIFT的速度加成值
    SPEED = 0

    #初始贪吃蛇移动方向
    DIRECTION     = 'RIGHT'

    #进入下一关需要的分数
    goal = 12

    #实例草地
    grass = GrassMap((0,190,0),LIVING_SPACE)

    #实例食物
    food  = Food((200,0,0),SIZE,LIVING_SPACE)

    #实例贪吃蛇
    snake = Snake(SNAKE_COLOR,SNAKE_LENGTH,SIZE,LIVING_SPACE)

    #实例出控制帧数的对象clock
    clock = pygame.time.Clock()

    #初始化贪吃蛇
    snake.generate()

    #获取贪吃蛇坐标
    snakebody = snake.snake_body        

    #随机生成食物
    food.generate(snakebody)

    #获取背景音乐路径
    BGMpath = os.getcwd() + '//' + 'BGM.ogg'
    #加载背景音乐
    pygame.mixer.music.load(BGMpath)
    #循环播放背景音乐
    pygame.mixer.music.play(-1)


    while True:
    #for _ in range(8):  
        #获取事件
        event = pygame.event.poll()       
        #判定事件
        if event.type == QUIT:
            pygame.quit()
            exit()
        #控制贪吃蛇移动   
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and DIRECTION != 'RIGHT':
                DIRECTION = 'LEFT'
            elif event.key == K_RIGHT and DIRECTION != 'LEFT':
                DIRECTION = 'RIGHT'
            elif event.key == K_UP and DIRECTION != 'DOWN':
                DIRECTION = 'UP'
            elif event.key == K_DOWN and DIRECTION != 'UP':
                DIRECTION = 'DOWN'

       #控制游戏暂停/继续         
            elif event.key == K_SPACE:
                pause_flag = 0
                while True:
                    for event in pygame.event.get():

                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                        if event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                
                                pause_flag = 1
                    if pause_flag == 1:
                        pygame.mixer.music.unpause()
                        break
                    pygame.mixer.music.pause()                           
            #加速贪吃蛇 
            elif event.key == K_LSHIFT:
                SPEED += 13
            # print('DIRECTION',DIRECTION)
        #从加速恢复
        elif event.type == KEYUP:
            if event.key == K_LSHIFT:
                SPEED -= 13
                    
        #获取食物坐标        
        foodbody = food._food_pos           
        #移动贪吃蛇并判断是否吃到食物
        snake.move(DIRECTION,foodbody)       
        #print('before:',food._food_pos,snake.snake_body[snake.head])

        #获取贪吃蛇坐标
        snakebody = snake.snake_body         
        #获取食物状态
        exist     = snake.foodstate         
        #判定是否随机生成食物
        food.if_exist(exist,snakebody)       
        #print('foodbody:',food._food_pos)
        #print('snakebodyhead:',snake.snake_body[snake.head])

        #判定贪吃蛇是否死亡    
        if snake.isdead():                  
            LIFE -= 1
            if LIFE == 0:
                pygame.mixer.music.stop()
                sounddead.play()               
                terminate(screen)
            elif LIFE > 0:
                snake.snake_body = [[x*20+0.05*WINDOW_WIDTH,0.9*WINDOW_HEIGHT-20] for x in range(len(snakebody))]
                DIRECTION = 'RIGHT'
                time.sleep(0.8)
        else:
            pass         

        #游戏分数模型
        score = (len(snake.snake_body)-5)*3

        #判定是否进入下一关
        if score == goal:
            time.sleep(0.3)
            nightmode()
        else: pass
            
        #贪吃蛇加速模型
        SNAKE_SPEED = 10 + math.log(score+1,math.e)*2

        #判定贪吃蛇是否满足加一条命的条件
        if GETSCORE == 1:
            if score != 0 and score % ((goal-3)//3) == 0:
                LIFE += 1
                
            GETSCORE = 0
        elif GETSCORE == 0: pass

        #填充背景
        screen.fill(BACK_GROUND_FILL)              

        #创建字体对象
        font         = pygame.font.SysFont("Arial",20)
       
        goalsurface = font.render('Goal : %s' % goal, True,(0,220,0))
        scoresurface = font.render('Score: %s' % score, True,(0,0,220))
       
        lifesurface   = font.render('Life: ', True,(220,0,0))

        #画出分数
        screen.blit(goalsurface,(0.8*WINDOW_WIDTH,0.01*WINDOW_HEIGHT))    
        screen.blit(scoresurface,(0.8*WINDOW_WIDTH,0.05*WINDOW_HEIGHT))

        #画出贪吃蛇生命指示
        screen.blit(lifesurface,(0.2*WINDOW_WIDTH-100,0.05*WINDOW_HEIGHT))

        #画出贪吃蛇的“血条”
        for i in range(LIFE):
            lifeR = pygame.Rect(0.2*WINDOW_WIDTH-50+25*i,0.05*WINDOW_HEIGHT,20,20)
            pygame.draw.rect(screen,snakecolor,lifeR)
            
        #画出草地
        grass.generate(screen)                    
        #画出谈处死
        LIFE = snake.draw(screen,snakecolor,[],LIFE)               
        #画出食物
        food.draw(screen)                            
        #print('update')
        #刷新
        pygame.display.update()                    
        #控制帧率
        time_passed = clock.tick(SNAKE_SPEED+SPEED)       


#噩梦模式
# ==================================================================================================================================

def nightmode():

    snakecolor      = (0,0,0)
    #SNAKE_BODY_STAY = []
    SPEED = 0
    LIFE = 1
    global GETSCORE
    GETSCORE = 0
    goal = 30

    #扩大地图为铺满整个窗体
    LIVING_SPACE = (0,0,WINDOW_WIDTH,WINDOW_HEIGHT)
    
    DIRECTION     = 'RIGHT'

    #随机地形常量——火
    rand1 = terrain(3,7,40,40,16,12)

    #随机地形常量——水
    rand2 = terrain(1,3,100,40,8,15)

    #随机地形常量——冰
    rand3 = terrain(3,9,40,40,20,10)

    #随机地形常量——土
    rand4 = terrain(2,8,80,40,10,15)

    #设置地形随机
    mode = randint(1,4)
    
    food  = Food((150,0,0),SIZE,LIVING_SPACE)

    snake = Snake(SNAKE_COLOR,SNAKE_LENGTH,SIZE,LIVING_SPACE)

    clock = pygame.time.Clock()

    snake.generate()

    snakebody = snake.snake_body        

    food.generate(snakebody)

    BGMpath = os.getcwd() + '//' + 'BGM.ogg'
    pygame.mixer.music.load(BGMpath)
    pygame.mixer.music.play(-1)


    while True:
    #for _ in range(8):

        event = pygame.event.poll()      

        if event.type == QUIT:
            pygame.quit()
            exit()
            
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and DIRECTION != 'RIGHT':
                DIRECTION = 'LEFT'
            elif event.key == K_RIGHT and DIRECTION != 'LEFT':
                DIRECTION = 'RIGHT'
            elif event.key == K_UP and DIRECTION != 'DOWN':
                DIRECTION = 'UP'
            elif event.key == K_DOWN and DIRECTION != 'UP':
                DIRECTION = 'DOWN'
                
            elif event.key == K_SPACE:
                pause_flag = 0
                while True:
                    for event in pygame.event.get():

                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                        if event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                
                                pause_flag = 1
                    if pause_flag == 1:
                        pygame.mixer.music.unpause()
                        break
                    pygame.mixer.music.pause()                           
            
            elif event.key == K_LSHIFT:
                SPEED += 13
            # print('DIRECTION',DIRECTION)
        elif event.type == KEYUP:
            if event.key == K_LSHIFT:
                SPEED -= 13
                                    
        foodbody = food._food_pos           
        snake.move(DIRECTION,foodbody)    
        #print('before:',food._food_pos,snake.snake_body[snake.head])
        snakebody = snake.snake_body      
        exist     = snake.foodstate      
        food.if_exist(exist,snakebody)      
        #print('foodbody:',food._food_pos)
        #print('snakebodyhead:',snake.snake_body[snake.head])

        #判定贪吃蛇是否死亡    
        if snake.isdead():                 
            LIFE -= 1
            if LIFE == 0:
                pygame.mixer.music.stop()
                sounddead.play()
                terminate(screen)
            elif LIFE > 0:
                snake.snake_body = [[x*20+0,WINDOW_HEIGHT-20] for x in range(len(snakebody))]
                DIRECTION = 'RIGHT'
                time.sleep(0.8)
        else:
            pass

        #游戏分数模型
        score = (len(snake.snake_body)-5)*3

        #贪吃蛇加速模型
        SNAKE_SPEED = 10 + math.log(score+1,math.e)*2

        #判定通过条件，进入通关界面
        if score == goal:
            time.sleep(0.8)
            while True:
                for event in pygame.event.get():   
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == KEYDOWN:     
                        if event.key == K_SPACE:
                            start()

                pygame.mixer.music.fadeout(6000)
                screen.fill((0,0,0))
                smilesurface = pygame.image.load(GETPASS)
                screen.blit(smilesurface,(200,100))

                font         = pygame.font.SysFont("Arial",30)
                tipsurface   = font.render('Press the Keyboard Space to restart!',True,(0,255,250))
                endsurface   = font.render('Congratulations,your stage clear!',True,(0,255,250))
                screen.blit(endsurface,(0.26*WINDOW_WIDTH,0.05*WINDOW_HEIGHT))
                screen.blit(tipsurface,(0.25*WINDOW_WIDTH,0.87*WINDOW_HEIGHT))
                pygame.display.update()                     
             
        #判定贪吃蛇是否满足加一条命的条件
        if GETSCORE == 1:
            if score != 0 and score % ((goal-3)//3) == 0:
                LIFE += 1
                
            GETSCORE = 0
        elif GETSCORE == 0: pass


        screen.fill((190,190,190))               

        font         = pygame.font.SysFont("Arial",20)
        goalsurface  = font.render('Goal : %s' % goal,True,(0,220,0))
        scoresurface = font.render('Score: %s' % score,True,(150,0,0))
        lifesurface  = font.render('Life: ', True,(220,0,0))
        screen.blit(scoresurface,(0.8*WINDOW_WIDTH,0.05*WINDOW_HEIGHT))
        screen.blit(goalsurface,(0.8*WINDOW_WIDTH,0.01*WINDOW_HEIGHT))
        screen.blit(lifesurface,(0.2*WINDOW_WIDTH-100,0.05*WINDOW_HEIGHT))

        #画出贪吃蛇的“血条”
        for i in range(LIFE):
            lifeR = pygame.Rect(0.2*WINDOW_WIDTH-50+25*i,0.05*WINDOW_HEIGHT,20,20)
            pygame.draw.rect(screen,snakecolor,lifeR)

        #用if...elif的结构画出随机地图
        if mode == 1:
            fireRlist = drawfire(screen,rand1[0],rand1[1],rand1[2])
            LIFE = snake.draw(screen,snakecolor,fireRlist,LIFE)      
            food.draw(screen,fireRlist,food._food_pos)               
        elif mode == 2:
            waterRlist = drawwater(screen,rand2[0],rand2[1],rand2[2])
            LIFE = snake.draw(screen,snakecolor,waterRlist,LIFE)
            food.draw(screen,waterRlist,food._food_pos)
        elif mode == 3:
            iceRlist = drawice(screen,rand3[0],rand3[1],rand3[2])
            LIFE = snake.draw(screen,snakecolor,iceRlist,LIFE)
            food.draw(screen,iceRlist,food._food_pos)
        elif mode ==4:
            solidRlist = drawsolid(screen,rand4[0],rand4[1],rand4[2])
            LIFE = snake.draw(screen,snakecolor,solidRlist,LIFE)
            food.draw(screen,solidRlist,food._food_pos)

        pygame.display.update()                           

        time_passed = clock.tick(SNAKE_SPEED+SPEED)        



#程序主体    
# ===============================================================================================================================================

#窗体宽度
WINDOW_WIDTH       = 800
#窗体高度
WINDOW_HEIGHT      = 600              

#窗体背景填充
BACK_GROUND_FILL   = (255,245,238)
#草地颜色
GRASS_COLOR        = (0,250,0)
#食物颜色
FOOD_COLOR         = (255,0,0)
#贪吃蛇颜色（底色）
SNAKE_COLOR        = (100,100,0)
#贪吃蛇主体颜色
SNAKE_INNER_COLOR  = (255,255,0)       

#生存空间
LIVING_SPACE       = (0.05*WINDOW_WIDTH,0.1*WINDOW_HEIGHT,0.9*WINDOW_WIDTH,0.8*WINDOW_HEIGHT)

#贪吃蛇和食物的“体型”
SIZE               = 20

#贪吃蛇的初始长度
SNAKE_LENGTH       = 5                

#游戏开始界面图片路径
SNAKE_START        = os.getcwd() + '\\' + 'cgg.jpg'
#游戏结束界面图片路径
GAMEOVER           = os.getcwd() + '\\' + 'gameover.jpg'
#游戏通关界面图片路径
GETPASS            = os.getcwd() + '\\' + 'Lqq.jpg'

#传送门标志位
GATEWAY_FLAG       = 0

#随机设置传送门出现位置
area               = (randint(3,40)*20,randint(3,30)*20)

#预加载pygame音频模块
pygame.mixer.pre_init(44100, 16, 2, 1024*4)

#初始化pygame 
pygame.init()

#创建窗体
screen =  pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,32)

#设置窗体标题 
pygame.display.set_caption("贪吃蛇大作战！")

#获取“死亡”音效路径
deadpath  = os.getcwd() + '//' + 'dead.wav'
#创建“死亡”音效对象
sounddead = pygame.mixer.Sound(deadpath)
#获取“吃食物”音效路径
eatpath   = os.getcwd() + '//' + 'eat.wav'
#创建“吃食物”音效对象
soundeat  = pygame.mixer.Sound(eatpath)

#开始游戏
start()                                           




























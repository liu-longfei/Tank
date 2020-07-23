# coding:utf-8
# Author: zdx and llf.   ps:zdx is the motivation,llf is a worker.
# Aim：Just to make zdx happy.Only for zdx happiness.
import pygame, time, random
from pygame.sprite import Sprite
from tkinter import *
from tkinter import messagebox

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 700
BG_COLOR = (0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)


class BaseItem(Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)


score = 0


class MainGame():
    window = None
    my_tank = None
    enemyTankList = []
    enemyTankCount = random.randint(10, 20)
    myBulletList = []
    enemyBulletList = []
    explodeList = []

    def __init__(self):
        pass

    def startGame(self):
        pygame.display.init()
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        background = pygame.image.load('./images/background.jpg')
        MainGame.my_tank = Tank(350, 250)
        self.createEnemyTank()

        pygame.display.set_caption('你瞅啥！！！打我啊！！！')
        while True:
            time.sleep(0.02)
            MainGame.window.blit(background, (0, 0))
            # MainGame.window.fill(BG_COLOR)
            self.getEvent()
            MainGame.window.blit(self.getTextSurface('敌方坦克剩余数量%d' % len(MainGame.enemyTankList)), (10, 10))
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            else:
                del MainGame.my_tank
                MainGame.my_tank = None
            self.blitEnemyTank()
            self.blitMyBullet()
            self.blitEnemyBullet()
            self.blitExplode()
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
            pygame.display.update()

    # 初始化地方坦克，并将敌方坦克添加到列表里

    def createEnemyTank(self):
        top = 100
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, 600)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            # enemy = EnemyTank(left, top)
            MainGame.enemyTankList.append(enemy)

    def blitExplode(self):
        for explode in MainGame.explodeList:
            if explode.live:
                explode.dispalyExplode()
            else:
                MainGame.explodeList.remove(explode)

    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            # 判断当前敌方坦克是否活着
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()
                enemyBullet = enemyTank.shot()
                if enemyBullet:
                    MainGame.enemyBulletList.append(enemyBullet)
            else:  # 不活着，从敌方坦克列表中移出
                MainGame.enemyTankList.remove(enemyTank)

    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            if myBullet.live:
                myBullet.displayBullet()
                myBullet.move()
                # 调用检测我方子弹是否与敌方坦克发生碰撞
                myBullet.myBullet_hit_enemyTank()
            else:
                MainGame.myBulletList.remove(myBullet)

    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            if enemyBullet.live:
                enemyBullet.displayBullet()
                enemyBullet.move()
                enemyBullet.enemyBullet_hit_myTank()

    def endGame(self):
        print('谢谢使用，欢迎再次使用')
        exit()

    def getTextSurface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('kaiti', 18)
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if MainGame.my_tank and MainGame.my_tank.live:
                    if event.key == pygame.K_LEFT:
                        MainGame.my_tank.direction = 'L'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下左键，坦克向左移动')
                    elif event.key == pygame.K_RIGHT:
                        MainGame.my_tank.direction = 'R'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下右键，坦克向右移动')
                    elif event.key == pygame.K_UP:
                        MainGame.my_tank.direction = 'U'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下右键，坦克向上移动')
                    elif event.key == pygame.K_DOWN:
                        MainGame.my_tank.direction = 'D'
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下右键，坦克向下移动')
                    elif event.key == pygame.K_SPACE:
                        print('发射子弹')
                        if len(MainGame.myBulletList) < 3:
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True


class Tank(BaseItem):
    def __init__(self, left, top):
        self.images = {
            'U': pygame.image.load('images/p1planeU.png'),
            'R': pygame.image.load('images/p1planeR.png'),
            'D': pygame.image.load('images/p1planeD.png'),
            'L': pygame.image.load('images/p1planeL.png'),
        }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = 5
        self.stop = True
        # 是否活着
        self.live = True

    def move(self):
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed

    def shot(self):
        return Bullet(self)

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class MyTank(Tank):
    def __init__(self):
        pass


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 调用父类的初始化方法
        super(EnemyTank, self).__init__(left, top)
        self.images = {
            'U': pygame.image.load('images/enemy1U.png'),
            'D': pygame.image.load('images/enemy1D.png'),
            'L': pygame.image.load('images/enemy1L.png'),
            'R': pygame.image.load('images/enemy1R.png'),
        }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.flag = True
        self.step = 60

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 60
        else:
            self.move()
            self.step -= 1

    def shot(self):
        num = random.randint(1, 100)
        if num < 10:
            return Bullet(self)


class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.image.load('images/enemymissile.png')
        self.direction = tank.direction
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        self.speed = 6
        self.live = True

    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False

    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)

    # 我方坦克与地方坦克的碰撞
    def myBullet_hit_enemyTank(self):
        # 循环遍历地方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                global score
                score += 100
                # 修改地方坦克和我方子弹的状态
                enemyTank.live = False
                self.live = False
                explode = Explode(enemyTank)
                MainGame.explodeList.append(explode)

    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                explode = Explode(MainGame.my_tank)
                MainGame.explodeList.append(explode)
                self.live = False
                MainGame.my_tank.live = False
                root = Tk()
                root.title('Game Over')
                root.geometry('500x350+500+260')
                btn01 = Button(root)
                btn01['text'] = '点击查看得分'
                btn01.pack()

                def grade(e):
                    messagebox.showinfo('得分',
                                        '你的得分是{}\n\nBUT\n\nif yourname == "zdx":\n   you are Very Good\nelse:\n    you are Vegetable \n   # include llf \n'.format(
                                            score))

                btn01.bind('<Button-1>', grade)
                global score
                print('你的得分是{}'.format(score))
                root.mainloop()
                exit()


class Wall():
    def __init__(self):
        pass

    def dispalyWall(self):
        pass


class Explode():
    def __init__(self, tank):
        self.rect = tank.rect
        self.images = [
            pygame.image.load('images/blast0.jpg'),
            pygame.image.load('images/blast1.jpg'),
            pygame.image.load('images/blast2.jpg'),
            pygame.image.load('images/blast3.jpg'),
            pygame.image.load('images/blast4.jpg'),
        ]
        self.step = 0
        self.image = self.images[self.step]
        self.live = True

    def dispalyExplode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            MainGame.window.blit(self.image, self.rect)
        else:
            self.live = False
            self.step = 0


class Music():
    def __init__(self):
        pass

    def play(self):
        pass


if __name__ == '__main__':
    MainGame().startGame()

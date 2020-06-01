from snake_elements import Settings, Snake, Crumbs, Button
import pygame,sys,time,logging
from pygame.sprite import Group

logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
#fix navigation; get rid of time...
#implement gamescore, highscore, new game and respective buttons
class Snagame():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snagame")
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.instruction=""
        self.crumbs=Group()
        self.snake=Group()
        self.last_instruction=""
        self.restart=True
        self.speed=0.1
        self.new_crumb=""
        self.score=0
        self.iteration=0
    def run(self):
        while True:
            #start game
            self.restart_game()
            #listener
            self.listen_for_commands()
            #movement
            self.moving(self.screen,self.settings,self.snake)
            #restart game
            self.restart_game()
            #endgame
            self.endgame()
            #update screen
            self.update_screen()
            clock=pygame.time.Clock()
            clock.tick(10)
            print(f"iteration:{self.iteration}---"+str(clock.get_fps()))
            self.iteration+=1
    def moving(self,screen,settings,snake):
        #new crumb
        if not self.crumbs:
            self.crumb_spawn()
            #avoid crumb spawn on the snake
            while pygame.sprite.groupcollide(self.snake,self.crumbs,False,True):
                self.crumb_spawn()
        #check for eaten crumb
        supper_time=pygame.sprite.groupcollide(self.crumbs,self.snake,True,False)
        #initialize
        slither_cell=""
        #avoid turning back
        if self.last_instruction=="up" and self.instruction=="down":
            self.instruction="up"
            #logging.debug("last_instruction=instruction:\n"'instruction:'+str(self.instruction)+"---last_instruction:"+str(self.last_instruction))
        elif self.last_instruction=="right" and self.instruction=="left":
            self.instruction="right"
        elif self.last_instruction=="down" and self.instruction=="up":
            self.instruction="down"
        elif self.last_instruction=="left" and self.instruction=="right":
            self.instruction="left"
        if self.instruction=="halt":
            #logging.debug('instruction:'+str(self.instruction)+"---last_instruction:"+str(self.last_instruction))
            pass
        #movement
        else:
            if self.instruction=="up":
                slither_cell=Snake(screen,settings,snake.sprites()[-1].rect.left,snake.sprites()[-1].rect.top-20)
                if slither_cell.rect.bottom==0:
                    self.restart=True
            elif self.instruction=="right":
                slither_cell=Snake(screen,settings,snake.sprites()[-1].rect.left+20,snake.sprites()[-1].rect.top)
                if slither_cell.rect.left==settings.screen_width:
                    self.restart=True
            elif self.instruction=="down":
                slither_cell=Snake(screen,settings,snake.sprites()[-1].rect.left,snake.sprites()[-1].rect.top+20)
                if slither_cell.rect.top==settings.screen_height:
                    self.restart=True
            elif self.instruction=="left":
                slither_cell=Snake(screen,settings,snake.sprites()[-1].rect.left-20,snake.sprites()[-1].rect.top)
                if slither_cell.rect.right==0:
                    self.restart=True
            if slither_cell!="":
                self.snake.add(slither_cell)
                if supper_time:
                    self.score+=1
                    logging.debug(str(self.score))
                else:
                    snake.sprites()[0].kill()
            #trigger over on autocollisions
            for cell in snake.sprites()[0:-2]:
                if cell.rect.collidepoint(slither_cell.rect.centerx,slither_cell.rect.centery):
                    self.restart=True
            #set comparison for next iteration
            self.last_instruction=self.instruction
    def listen_for_commands(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    self.instruction="up"
                elif event.key==pygame.K_RIGHT:
                    self.instruction="right"
                elif event.key==pygame.K_DOWN:
                    self.instruction="down"
                elif event.key==pygame.K_LEFT:
                    self.instruction="left"
                elif event.key==pygame.K_SPACE:
                    self.instruction="halt"
    def update_screen(self):
        score_button=Button(self.screen,str(self.score))
        score_button.msg_image_rect.center=(self.settings.screen_width-50,50)
        self.screen.fill(self.settings.bg_color)
        score_button.draw_button()
        self.new_crumb.draw_crumb()
        for cell in self.snake.sprites():
            cell.draw_snake()
        pygame.display.flip()
    def snake_head_spawn(self):
        snake_head=Snake(self.screen,self.settings,self.settings.startx,self.settings.starty)
        self.snake.add(snake_head)
    def crumb_spawn(self):
        self.new_crumb=Crumbs(self.screen,self.settings)
        self.crumbs.add(self.new_crumb)
    def restart_game(self):
        if self.restart==True:
            over_button=Button(self.screen,"Game Over, Sucka!-"+str(self.score))
            if self.score!=0:
                over_button.draw_button()
                pygame.display.flip()
                #logging.debug('over')
                time.sleep(2)
            self.restart=False
            self.instruction=""
            self.last_instruction=""
            #logging.debug('Start of False')
            for cell in self.snake.sprites():
                cell.kill()
            self.snake_head_spawn()
            for crumb in self.crumbs.sprites():
                crumb.kill()
            self.score=0
    def endgame(self):
        if len(self.snake.sprites())==int((self.settings.screen_width/self.settings.square_size)**2):
            self.screen.fill(self.settings.bg_color)
            pygame.display.flip()
            time.sleep(3)
            sys.exit()
game=Snagame()
game.run()
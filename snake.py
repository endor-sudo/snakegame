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
        self.new_crumb=""
        self.score=0
        self.clock = pygame.time.Clock()
        self.fps = self.settings.fps
        self.control_instruction=""
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
            #self.endgame()
            #update screen
            self.update_screen()
            print (f"tick={self.clock.tick(self.fps)}, fps={int(self.clock.get_fps())}")
            #self.clock.tick(self.fps)
    def moving(self,screen,settings,snake):
        #new crumb
        if not self.crumbs:
            self.crumb_spawn()
            #avoid crumb spawn on the snake
            while pygame.sprite.groupcollide(self.snake,self.crumbs,False,True):
                self.crumb_spawn()
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
        #check for pause
        if self.instruction=="halt":
            #logging.debug('instruction:'+str(self.instruction)+"---last_instruction:"+str(self.last_instruction))
            pass
        #movement
        else:
            self.control_instruction=self.instruction
            #turning only when supposed to
            if self.snake.sprites()[-1].rect.left%settings.square_size==0 and self.snake.sprites()[-1].rect.top%settings.square_size==0:
                #give the lead cell its direction        
                nextcell_direction=self.instruction
                #pass on directions from one cell to another
                for cell in reversed(self.snake.sprites()):
                    thiscell_direction=cell.direction
                    cell.direction=nextcell_direction
                    nextcell_direction=thiscell_direction
            else:
                self.instruction=self.last_instruction
            #for each cell make a movement according to directions
            for cell in self.snake.sprites():
                if cell.direction=="up":
                    cell.rect.top-=settings.speed
                    if self.snake.sprites()[-1].rect.bottom<0:
                        self.restart=True
                elif cell.direction=="right":
                    cell.rect.left+=settings.speed
                    if self.snake.sprites()[-1].rect.left==settings.screen_width:
                        self.restart=True
                elif cell.direction=="down":
                    cell.rect.top+=settings.speed
                    if self.snake.sprites()[-1].rect.top==settings.screen_height:
                        self.restart=True
                elif cell.direction=="left":
                    cell.rect.left-=settings.speed
                    if self.snake.sprites()[-1].rect.right==0:
                        self.restart=True
            #set comparison for next iteration
            self.last_instruction=self.instruction
            supper_time=False
            #check for eaten crumb
            if self.snake.sprites()[-1].rect.centerx==self.new_crumb.rect.centerx and self.snake.sprites()[-1].rect.centery==self.new_crumb.rect.centery:
                supper_time=True
            if supper_time:
                for crumb in self.crumbs:
                    crumb.kill()
                self.score+=1
                if self.snake.sprites()[0].direction=="up":
                    new_cell=Snake(screen, settings, self.snake.sprites()[0].rect.left, self.snake.sprites()[0].rect.top+settings.square_size,"up")
                elif self.snake.sprites()[0].direction=="down":
                    new_cell=Snake(screen, settings, self.snake.sprites()[0].rect.left, self.snake.sprites()[0].rect.top-settings.square_size,"down")
                elif self.snake.sprites()[0].direction=="left":
                    new_cell=Snake(screen, settings, self.snake.sprites()[0].rect.left+settings.square_size, self.snake.sprites()[0].rect.top,"left")
                elif self.snake.sprites()[0].direction=="right":
                    new_cell=Snake(screen, settings, self.snake.sprites()[0].rect.left-settings.square_size, self.snake.sprites()[0].rect.top,"right")
                mediumgroup=Group()
                mediumgroup.add(new_cell)
                for cell in self.snake.sprites():
                    mediumgroup.add(cell)
                self.snake=mediumgroup
                supper_time=False 
            #Autocollisions
            for cell in self.snake.sprites()[:-4]:
                if cell.rect.collidepoint(self.snake.sprites()[-1].rect.centerx, self.snake.sprites()[-1].rect.centery):
                    self.restart=True
            #to check whether it is ok to turn on the next iteration
            self.instruction=self.control_instruction
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
        snake_head=Snake(self.screen,self.settings,self.settings.startx,self.settings.starty, "halt")
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
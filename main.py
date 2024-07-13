import pygame
import random
import bisect

pygame.init()
pygame.mixer.init()


window_x=720
window_y=480

board_x=20
board_y=20


#CHANGE IT FOR YOUR RESOLUTION
block_resolution = 32

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fps = pygame.time.Clock()


pygame.display.set_caption('Isometric Snake')
game_window = pygame.display.set_mode((window_x, window_y))
game_window.fill(white)

snake_body_png = pygame.image.load("snake_body.png").convert_alpha()

board_png = pygame.image.load("board.png").convert_alpha()

fruit_png = pygame.image.load("fruit.png").convert_alpha()



class Snake:
    def __init__(self):
        #in the beginning snake have 3 parts and is going down
        self.direction = 'DOWN'
        self.next_direction = self.direction
        self.body = [[0,0],
              [0,0],
              [0,0],
              ]
        self.head_pos = [0,0]

    def change_direction(self, new_direction):
        #checking if snake wants to turn 180 degrees
        if new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        elif new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        elif new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def move(self):
        #moving on the 20x20 2D board
        if self.direction == 'UP':
            self.head_pos[1] -= 1
        elif self.direction == 'DOWN':
            self.head_pos[1] += 1
        elif self.direction == 'LEFT':
            self.head_pos[0] -= 1
        elif self.direction == 'RIGHT':
            self.head_pos[0] += 1

        self.body.insert(0, list(self.head_pos))

    def check_collision(self):
        #end of a board
        if (self.head_pos[0] < 0 or self.head_pos[1] < 0 or
                self.head_pos[0] > (board_x - 1) or self.head_pos[1] > (board_y - 1)):
            return True
        #collision with itself
        for pos in self.body[1:]:
            if self.head_pos == pos:
                return True
        return False

class Fruit:
    def __init__(self):
        self.position = [random.randrange(0, board_x - 1), random.randrange(0, board_y - 1)]

    def respawn(self, snake_body):
        new_fruit = True
        while new_fruit:
            self.position = [random.randrange(0, board_x - 1), random.randrange(0, board_y - 1)]
            new_fruit = False
            #checking if fruit wants to spawn inside snake
            for pos in snake_body:
                if self.position == pos:
                    new_fruit = True

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        #g_o = game_over
        self.g_o = False
        self.new_game = False
        self.pause = False

    def isometric_formula(self,pos):
        #adding this numbers make program to display board in the right spot
        x = pos[0] * block_resolution/2 - 244
        y = pos[1] * block_resolution/2 + 284
        new_pos = [0, 0]
        #basic isometric formula
        new_pos[0] = x + y
        new_pos[1] = -0.5 * x + 0.5 * y

        return new_pos
    def draw_board(self):
        for y in range(board_x):
            for x in range(board_y):
                #could be done with isometric_formula but it will need to use it twice
                game_window.blit(board_png, (window_x / 2 - block_resolution/2 + x * block_resolution/2 - y * block_resolution/2, window_y / 5 + x * 8 + y * 8 + block_resolution))

    def show_score(self):
        #gameplay
        if self.g_o == False:
            score_surface = pygame.font.SysFont('times new roman', 25).render('Score: ' + str(self.score), True, black)
            game_window.blit(score_surface, score_surface.get_rect())
        #game over screen
        else:
            score_surface = pygame.font.SysFont('times new roman', 50).render('Score: ' + str(self.score), True, black)
            score_rect = score_surface.get_rect()
            score_rect.center = (window_x / 2, window_y / 2)
            game_window.blit(score_surface, score_rect)

            restart_surface = pygame.font.SysFont('times new roman', 25).render('Press SPACE to restart', True, red)
            restart_rect = restart_surface.get_rect()
            restart_rect.center = (window_x/2, window_y/2 + 50)
            game_window.blit(restart_surface, restart_rect)

    def paused(self):
        game_window.fill(white)
        pause_surface = pygame.font.SysFont('times new roman', 50).render('Paused, press Esc', True, black)
        pause_rect = pause_surface.get_rect()
        pause_rect.center = (window_x / 2, window_y / 2)
        game_window.blit(pause_surface, pause_rect)
        pygame.display.update()

        return

    def update(self):
        #if game over then display and return
        if self.pause == True:
            self.paused()
            return
        if self.g_o == True:
            game_window.fill(white)
            self.show_score()
            pygame.display.update()
            return

        self.snake.move()

        if self.snake.check_collision():

            self.g_o = True
            self.show_score()
            pygame.display.update()
            pygame.mixer.music.load('End.mp3')
            pygame.mixer.music.play()
            return

        #making snake grow by not deleting last part
        if self.snake.head_pos == self.fruit.position:
            self.fruit.respawn(self.snake.body)
            self.score += 10
            pygame.mixer.music.load('Point.mp3')
            pygame.mixer.music.play()

        else:
            self.snake.body.pop()
        game_window.fill(white)

        self.draw_board()

        """
        algorith for checking where would fruit be in sorted list of snake 
        parts to display everything in right order
        """

        sort_key = lambda x: (-x[0], x[1])
        sorted_list = sorted(self.snake.body, key=sort_key)

        insert_index = bisect.bisect_left([sort_key(x) for x in sorted_list], sort_key(self.fruit.position))

        counter = 0
        for pos in sorted_list:
            if counter == insert_index:
                isometric_fruit_pos = self.isometric_formula(self.fruit.position)
                game_window.blit(fruit_png, (isometric_fruit_pos[0], isometric_fruit_pos[1]))
            isometric_pos = self.isometric_formula(pos)
            game_window.blit(snake_body_png, (isometric_pos[0], isometric_pos[1]))

            counter += 1

        #if fruit is meant to be displayed last
        if counter == insert_index:
            isometric_fruit_pos = self.isometric_formula(self.fruit.position)
            game_window.blit(fruit_png, (isometric_fruit_pos[0], isometric_fruit_pos[1]))

        self.show_score()

        pygame.display.update()

        fps.tick(5)

#int main()
if __name__ == '__main__':


    running = True
    while running:
        game = Game()

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.snake.next_direction = 'UP'
                    elif event.key == pygame.K_DOWN:
                        game.snake.next_direction = 'DOWN'
                    elif event.key == pygame.K_LEFT:
                        game.snake.next_direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT:
                        game.snake.next_direction = 'RIGHT'
                    if event.key == pygame.K_ESCAPE:
                        game.pause = not game.pause
                    if game.g_o == True:
                        if event.key == pygame.K_SPACE:
                            game.new_game = True

            game.snake.change_direction(game.snake.next_direction)
            game.update()
            if game.new_game:
                del game
                break

    pygame.quit()
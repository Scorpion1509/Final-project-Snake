import pygame
import random
from enum import Enum
from abc import ABC, abstractmethod


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class SnakeSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.body = [(100, 50), (90, 50), (80, 50)]
            cls._instance.direction = Direction.RIGHT
            cls._instance.grow = False
            cls._instance.score = 0
            cls._instance.game_over = False
            cls._instance.width = 600
            cls._instance.height = 400
        return cls._instance

    def update(self):
        self.move()
        self.check_collision()
        self.check_out_of_bounds()

    def move(self):
        head = self.body[0]
        x, y = head

        if self.direction == Direction.UP:
            new_head = (x, y - 10)
        elif self.direction == Direction.DOWN:
            new_head = (x, y + 10)
        elif self.direction == Direction.LEFT:
            new_head = (x - 10, y)
        elif self.direction == Direction.RIGHT:
            new_head = (x + 10, y)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def check_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head == segment:
                self.game_over = True

    def check_out_of_bounds(self):
        head = self.body[0]
        if head[0] < 0:
            head = (self.width - 10, head[1])
        elif head[0] >= self.width:
            head = (0, head[1])
        elif head[1] < 0:
            head = (head[0], self.height - 10)
        elif head[1] >= self.height:
            head = (head[0], 0)

        self.body[0] = head

    # Остальные методы класса SnakeSingleton


class Food(Observer):
    def __init__(self):
        self.position = (0, 0)
        self.width = 600
        self.height = 400
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, 59) * 10, random.randint(0, 39) * 10)

    def get_position(self):
        return self.position

    def update(self):
        pass

class GameObjectFactory(ABC):
    @abstractmethod
    def create_snake(self):
        pass

    @abstractmethod
    def create_food(self):
        pass

class ConcreteGameObjectFactory(GameObjectFactory):
    def create_snake(self):
        return SnakeSingleton()

    def create_food(self):
        return Food()

class CompositeGameObject:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update(self):
        for obj in self.objects:
            obj.update()

class Game:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.factory = ConcreteGameObjectFactory()
        self.game_objects = CompositeGameObject()
        self.snake = self.factory.create_snake()
        self.food = self.factory.create_food()
        self.game_objects.add_object(self.snake)
        self.game_objects.add_object(self.food)
        self.spawn_food()

    def spawn_food(self):
        self.food.randomize_position()
        while self.food.get_position() in self.snake.body:
            self.food.randomize_position()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self.snake.direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT:
                        self.snake.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.snake.direction = Direction.RIGHT

            self.screen.fill((0, 0, 0))
            self.game_objects.update()

            for segment in self.snake.body:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))

            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.get_position()[0], self.food.get_position()[1], 10, 10))

            if self.snake.body[0] == self.food.get_position():
                self.snake.grow = True
                self.spawn_food()

            if self.snake.game_over:
                font = pygame.font.Font(None, 36)
                text = font.render("Game Over", True, (255, 0, 0))
                text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()


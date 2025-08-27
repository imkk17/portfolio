import pygame
import sys
import random
import heapq
import time
import urllib.request
import io
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
MAZE_WIDTH = SCREEN_WIDTH // TILE_SIZE
MAZE_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Directions
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def load_image_from_url(url, size=(TILE_SIZE - 10, TILE_SIZE - 10)):
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        image = image.resize(size, Image.Resampling.LANCZOS)
        return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
    except Exception as e:
        print(f"Error loading image: {e}")
        return pygame.Surface(size)  # Fallback to empty surface

class Maze:
    def __init__(self):
        self.grid = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
        self.generate_maze()

    def generate_maze(self):
        stack = []
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = 0
        stack.append((start_x, start_y))

        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 < nx < MAZE_WIDTH - 1 and 0 < ny < MAZE_HEIGHT - 1 and self.grid[ny][nx] == 1:
                    neighbors.append((dx, dy))
            if neighbors:
                dx, dy = random.choice(neighbors)
                self.grid[y + dy][x + dx] = 0
                nx, ny = x + dx * 2, y + dy * 2
                self.grid[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        self.start = (1, 1)
        self.end = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
        self.grid[self.end[1]][self.end[0]] = 0

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1
        # Placeholder URL; replace with specific sprite for Lucky the Cat
        self.sprite = load_image_from_url(
            "https://www.spriters-resource.com/resources/sheets/149/152177.png?updated=1629746970",
            (TILE_SIZE - 10, TILE_SIZE - 10)
        )

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze.grid[new_y][new_x] == 0:
            self.x = new_x
            self.y = new_y

class Wolf:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.5
        self.path = []
        self.move_timer = 0
        # Placeholder URL; replace with specific sprite for Tanuki
        self.sprite = load_image_from_url(
            "https://www.spriters-resource.com/resources/sheets/149/152177.png?updated=1629746970",
            (TILE_SIZE - 10, TILE_SIZE - 10)
        )

    def find_path(self, maze, target_x, target_y):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        start = (self.x, self.y)
        goal = (target_x, target_y)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            for dx, dy in DIRECTIONS:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < MAZE_WIDTH and 0 <= neighbor[1] < MAZE_HEIGHT and maze.grid[neighbor[1]][neighbor[0]] == 0:
                    tentative_g = g_score[current] + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return []

    def update(self, maze, player, time_elapsed):
        if time_elapsed > 30:
            self.speed = 1.0
        if time_elapsed > 60:
            self.speed = 1.5
        self.move_timer += self.speed / FPS
        if self.move_timer >= 1:
            if not self.path:
                self.path = self.find_path(maze, player.x, player.y)
            if self.path:
                next_pos = self.path.pop(0)
                self.x, self.y = next_pos
            self.move_timer = 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Chase - Doodle Champion")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        # Placeholder URL; replace with specific sprite for exit (door)
        self.exit_sprite = load_image_from_url(
            "https://www.spriters-resource.com/resources/sheets/149/152177.png?updated=1629746970",
            (TILE_SIZE, TILE_SIZE)
        )
        self.reset()

    def reset(self):
        self.maze = Maze()
        self.player = Player(*self.maze.start)
        self.wolf = Wolf(MAZE_WIDTH - 2, 1)
        self.state = "menu"
        self.start_time = None
        self.score = 0

    def draw_maze(self):
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                color = BLACK if self.maze.grid[y][x] == 1 else WHITE
                pygame.draw.rect(self.screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_player(self):
        self.screen.blit(self.player.sprite, (self.player.x * TILE_SIZE + 5, self.player.y * TILE_SIZE + 5))

    def draw_wolf(self):
        self.screen.blit(self.wolf.sprite, (self.wolf.x * TILE_SIZE + 5, self.wolf.y * TILE_SIZE + 5))

    def draw_exit(self):
        self.screen.blit(self.exit_sprite, (self.maze.end[0] * TILE_SIZE, self.maze.end[1] * TILE_SIZE))

    def draw_text(self, text, pos, color=WHITE):
        text_surf = self.font.render(text, True, color)
        self.screen.blit(text_surf, pos)

    def menu(self):
        self.screen.fill(BLACK)
        self.draw_text("Maze Chase - Doodle Champion", (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 50))
        self.draw_text("Press SPACE to start", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    def game_over(self):
        self.screen.fill(BLACK)
        self.draw_text("Game Over!", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        self.draw_text(f"Score: {self.score}", (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        self.draw_text("Press R to restart", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

    def win(self):
        self.screen.fill(BLACK)
        self.draw_text("You Win!", (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
        self.draw_text(f"Score: {self.score}", (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        self.draw_text("Press R to restart", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        if event.key == pygame.K_SPACE:
                            self.state = "playing"
                            self.start_time = time.time()
                    elif self.state == "playing":
                        if event.key == pygame.K_UP:
                            self.player.move(0, -1, self.maze)
                        elif event.key == pygame.K_DOWN:
                            self.player.move(0, 1, self.maze)
                        elif event.key == pygame.K_LEFT:
                            self.player.move(-1, 0, self.maze)
                        elif event.key == pygame.K_RIGHT:
                            self.player.move(1, 0, self.maze)
                    elif self.state in ["game_over", "win"]:
                        if event.key == pygame.K_r:
                            self.reset()

            if self.state == "menu":
                self.menu()
            elif self.state == "playing":
                time_elapsed = time.time() - self.start_time
                self.score = int(time_elapsed)
                self.wolf.update(self.maze, self.player, time_elapsed)
                if (self.player.x, self.player.y) == (self.wolf.x, self.wolf.y):
                    self.state = "game_over"
                if (self.player.x, self.player.y) == self.maze.end:
                    self.state = "win"
                self.screen.fill(BLACK)
                self.draw_maze()
                self.draw_exit()
                self.draw_player()
                self.draw_wolf()
                self.draw_text(f"Score: {self.score}", (10, 10))
                pygame.display.flip()
            elif self.state == "game_over":
                self.game_over()
            elif self.state == "win":
                self.win()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
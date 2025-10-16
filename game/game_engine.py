import pygame
from .paddle import Paddle
from .ball import Ball, score_sound

# Game Engine
WHITE = (255, 255, 255)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            score_sound.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        if self.player_score == self.target_score or self.ai_score == self.target_score:
            winner = "Player Wins!" if self.player_score == self.target_score else "AI Wins!"

            screen.fill((0, 0, 0))
            win_text = self.font.render(winner, True, (255, 255, 255))
            prompt_text = self.font.render(
                "Press 3, 5, or 7 to play again | ESC to quit", True, (255, 255, 255)
            )

            screen.blit(
                win_text,
                (self.width // 2 - win_text.get_width() // 2, self.height // 2 - 50),
            )
            screen.blit(
                prompt_text,
                (self.width // 2 - prompt_text.get_width() // 2, self.height // 2 + 20),
            )

            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                        elif event.key in (pygame.K_3, pygame.K_5, pygame.K_7):
                            self.target_score = int(event.unicode)
                            self.reset_game()
                            waiting = False

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2


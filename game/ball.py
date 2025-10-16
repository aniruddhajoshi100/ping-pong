import pygame
import random

pygame.mixer.init()
paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
score_sound = pygame.mixer.Sound("assets/score.wav")


class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            wall_bounce_sound.play()

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.x = player_rect.right
            self.velocity_x *= -1
            paddle_hit_sound.play()
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.x = ai_rect.left - self.width
            self.velocity_x *= -1
            paddle_hit_sound.play()
        # Check collision with player paddle
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.x = player_rect.right  # move ball just outside paddle
            self.velocity_x *= -1
        # Check collision with AI paddle
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.x = ai_rect.left - self.width  # move ball just outside paddle
            self.velocity_x *= -1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


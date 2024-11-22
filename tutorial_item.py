import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# 화면 설정
screen_width = 1200 
screen_height = 700
TILE_SIZE = 50
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Heart of Truth")

# 플레이어 설정
player_pos = [4, 2]
player_images = {
    "up": pygame.image.load("image/up_resized.png"),
    "down": pygame.image.load("image/down_resized.png"),
    "left": pygame.image.load("image/left_resized.png"),
    "right": pygame.image.load("image/right_resized.png"),
}
current_image = player_images["up"]

# 타일 맵 정의 (0: 빈 칸, 1: 벽, 3: 파괴 가능한 벽, 4 : 몬스터, 5 : 아이템)
level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 파괴 가능한 벽 설정
obstacle_image = pygame.image.load("image/start.png") # obstacle.png
obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))
destructible_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 3]
destructible_items = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 5] # 아이템 위치를 찾아서 리스트 (x, y) 로 저장
break_count = 0
break_limit = 5

# 방향키 설정
MOVE_KEYS = {
    pygame.K_LEFT: (-1, 0, "left"),
    pygame.K_RIGHT: (1, 0, "right"),
    pygame.K_UP: (0, -1, "up"),
    pygame.K_DOWN: (0, 1, "down")
}

# 맵 그리기
def draw_map():
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, GRAY, rect)
            elif tile == 3 and [x, y] in destructible_walls:
                screen.blit(obstacle_image, rect.topleft)
                
            # 5번 아이템 - 아이템 위치에 아이템 이미지 띄우기
            elif tile == 5 and [x, y] in destructible_items:
                screen.blit(item_image, rect.topleft)

# 캐릭터 이동
def move_player(dx, dy, direction):
    global player_pos, current_image, break_count, item_get
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map):

        # 벽 충돌 처리
        if [new_x, new_y] in destructible_walls:
            if break_count < break_limit:  # 벽 부수기 제한 확인
                destructible_walls.remove([new_x, new_y])
                break_count += 1

        # 이동 위치가 아이템 위치라면 True로 바꾸고, 위치 제거
        elif [new_x, new_y] in destructible_items:
            destructible_items.remove([new_x, new_y])
            item_get = True

        elif level_map[new_y][new_x] != 1:
            player_pos = [new_x, new_y]
    current_image = player_images[direction]



# 아이템 이미지 로드
item_image = pygame.image.load("image/test_item.png")
item_image = pygame.transform.scale(item_image, (TILE_SIZE, TILE_SIZE))  # 타일 크기에 맞게 조정

# 아이템 획득 여부 (기본값: False)
item_get = False



# 게임 루프
running = True
while running:
    screen.fill(WHITE)
    draw_map()
    screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

    # 남은 횟수 출력
    font = pygame.font.SysFont(None, 36)
    count_text = font.render(f"block count: {break_limit - break_count} / Acquire item : {item_get}", True, (0, 0, 0))
    screen.blit(count_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                dx, dy, direction = MOVE_KEYS[event.key]
                move_player(dx, dy, direction)
                
    pygame.display.flip()
pygame.quit()

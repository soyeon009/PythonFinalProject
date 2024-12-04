import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TILE_SIZE = 50

def main():
    pygame.init()
    pygame.display.set_caption("Heart of Truth")
    screen = pygame.display.set_mode((1200, 700))
    clock = pygame.time.Clock()

    # 폰트 설정
    font = pygame.font.Font(None, 36)

    # 배경 이미지
    background_image = pygame.image.load("bg.png")
    background_image = pygame.transform.scale(background_image, (1200, 700))

    # 플레이어 설정
    player_pos = [4, 4]  # 플레이어 시작 위치
    player_images = {
        "up": pygame.image.load("1up.png"),
        "down": pygame.image.load("down.png"),
        "left": pygame.image.load("left.png"),
        "right": pygame.image.load("right.png"),
    }
    current_image = player_images["down"]

    # 타일 맵
    level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 2, 0, 0, 1, 0, 0, 5, 0, 0, 1, 0, 0, 5, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 6, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 7, 7, 7, 1, 1, 1, 0, 0, 0, 1, 1, 1, 3, 3, 3, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 4, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

    # 움직이는 벽(2)와 파괴 가능한 벽(3) 위치 추적
    movable_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 2]
    destructible_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 3]
    break_count = 0
    break_limit = 5

    #포탈(5) 위치 저장
    portal_positions = [[x,y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 5]

    #블록(6) 놓는 위치 저장
    target_positions = [[x,y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 6]

    #사라지는 벽(7) 위치 저장
    onoff_positions = [[x,y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 7]

    # 타일 이미지 설정
    wall_image = pygame.image.load("wall.png")
    wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))

    obstacle_image = pygame.image.load("removewall.png")
    obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))

    movable_wall_image = pygame.image.load("movewall.png")
    movable_wall_image = pygame.transform.scale(movable_wall_image, (TILE_SIZE, TILE_SIZE))

    goal_image = pygame.image.load("end.png")
    goal_image = pygame.transform.scale(goal_image, (TILE_SIZE, TILE_SIZE))

    portal_img = pygame.image.load("portal.png")
    portal_img = pygame.transform.scale(portal_img,(TILE_SIZE,TILE_SIZE))

    targets_img = pygame.image.load("target.png") #블록 놓는 곳
    targets_img = pygame.transform.scale(targets_img,(TILE_SIZE,TILE_SIZE))

    onoffwall_img = pygame.image.load("onoffWall.png")
    onoffwall_img = pygame.transform.scale(onoffwall_img,(TILE_SIZE,TILE_SIZE))

    # 방향키 설정
    MOVE_KEYS = {
        pygame.K_LEFT: (-1, 0, "left"),
        pygame.K_RIGHT: (1, 0, "right"),
        pygame.K_UP: (0, -1, "up"),
        pygame.K_DOWN: (0, 1, "down")
    }

    def draw_map():
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    screen.blit(wall_image, rect.topleft)
                elif tile == 3 and [x, y] in destructible_walls:
                    screen.blit(obstacle_image, rect.topleft)
                elif tile == 2 and [x, y] in movable_walls:
                    screen.blit(movable_wall_image, rect.topleft)
                elif tile == 4:
                    screen.blit(goal_image, rect.topleft)
                elif tile == 5:
                    screen.blit(portal_img, rect.topleft)
                elif [x,y] in target_positions:#(6 블럭 놓는 곳)
                    screen.blit(targets_img, rect.topleft)
                elif tile == 7:
                    screen.blit(onoffwall_img, rect.topleft)

    def move_player(dx, dy, direction):
        nonlocal player_pos, current_image, break_count
        new_x, new_y = player_pos[0] + dx, player_pos[1] + dy

        if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map):
            # 움직이는 벽 처리 (2)
            if [new_x, new_y] in movable_walls:
                move_x, move_y = new_x + dx, new_y + dy
                if 0 <= move_x < len(level_map[0]) and 0 <= move_y < len(level_map):
                    if level_map[move_y][move_x] == 0 or level_map[move_y][move_x] == 6:  # 밀려날 자리가 비어 있으면
                        movable_walls.remove([new_x, new_y])
                        movable_walls.append([move_x, move_y])
                        level_map[new_y][new_x] = 0
                        level_map[move_y][move_x] = 2
                    else:
                        return  # 밀 수 없는 경우 이동 불가
                else:
                    return  # 맵 경계 밖으로 이동 불가

            # 파괴 가능한 벽 처리 (3)
            elif [new_x, new_y] in destructible_walls:
                if break_count < break_limit:
                    destructible_walls.remove([new_x, new_y])
                    level_map[new_y][new_x] = 0
                    break_count += 1
                else:
                    return  # 벽 부수기 제한 초과

            # 도착지점 처리 (4)
            elif level_map[new_y][new_x] == 4:
                print("Goal Reached!")
                pygame.quit()
                sys.exit()
            
            # 일반 이동
            elif level_map[new_y][new_x] == 0 or level_map[new_y][new_x] == 5 or level_map[new_y][new_x] == 6:
                player_pos = [new_x, new_y]
                current_image = player_images[direction]
            #target_position에 움직이는 블록이 있다면 맵에 있는 7을 0으로 바꿈
            cnt = 0                
            for [target_x,target_y] in target_positions:
                if level_map[target_y][target_x] == 2:#2는 움직이는 벽 번호
                    cnt +=1
                if cnt == len(target_positions):
                    for [off_x,off_y] in onoff_positions:
                        level_map[off_y][off_x]=0
            
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    dx, dy, direction = MOVE_KEYS[event.key]
                    move_player(dx, dy, direction)
                if event.key == pygame.K_SPACE:
                    if player_pos in portal_positions:
                        portal_positions_copy = portal_positions.copy()  # 포탈 목록 복사
                        portal_positions_copy.remove(player_pos)  # 현재 위치의 포탈을 제외
                        if portal_positions_copy:
                            player_pos = portal_positions_copy[0]

        # 화면 업데이트
        screen.blit(background_image, (0, 0))  # 배경 이미지
        draw_map()
        screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

        # 남은 벽 부수기 횟수 출력
        count_text = font.render(f"Wall Breaks: {break_limit - break_count}", True, BLACK)
        screen.blit(count_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
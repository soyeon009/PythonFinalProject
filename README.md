## 파이썬 응용 - 기말 프로젝트 팀 <해냈조>
### tutorial_1(item).py
#### 튜토리얼 소스코드에 아이템 추가 및 획득 여부 구현
#### 탈출 코드 구현
#### 아이템 획득시에만 탈출 코드 구현
#### 탈출시 자동 맵 이동 구현
#### 리셋 버튼 이미지, reset_all 함수 구현

#### 맵의 아이템 8 추가 설정
```python
# 0: 움직일수있는 공간 1: 벽(이동x) 2:움직일수있는벽 3: 파괴가능한벽 4:몬스터 5:포탈 6:블록 놓는 위치 7: 사라지는 블럭 8 : 아이템 9 : 리셋 버튼
    level_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
```

#### 아이템 위치 리스트 변수 설정
```python
 # 아이템 위치를 찾아서 리스트 (x, y) 로 저장
    destructible_items = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 8]
```

#### 탈출 위치 리스트 변수 설정
```python
 # 탈출 위치를 찾아서 리스트 (x, y) 로 저장
    destructible_escape = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 4]
```

#### draw_map 함수에 아이템 위치에 이미지 생성
```python
# 8번 아이템 - 아이템 위치에 아이템 이미지 띄우기
            elif tile == 8 and [x, y] in destructible_items:
                screen.blit(item_image, rect.topleft)
```

#### move_player 함수에 item_get 변수 비전역변수로 가져오기 & 아이템 획득 유무 판별
```python
# 이동 위치가 아이템 위치라면 True로 바꾸고, 위치 0으로 변경, 플레이어 위치 새로 이동
            elif [new_x, new_y] in destructible_items:
                destructible_items.remove([new_x, new_y])
                item_get = True
                level_map[new_y][new_x] = 0
                player_pos = [new_x, new_y]
```

#### move_player 함수에 탈출 지점에서 아이템 획득 여부 판별 맵 자동 이동
```python
# 탈출 위치 처리 (4)
            # 아이템 획득 여부 판별과 플레이어 위치(탈출 위치)에 따른 맵 자동 이동
            elif level_map[new_y][new_x] == 4 and item_get == True:
                destructible_escape.remove([new_x, new_y])
                level_map[new_y][new_x] = 0
                player_pos = [new_x, new_y]
                os.system('python story1.py')
                pygame.quit()
                sys.exit()
```

#### reset_all 함수 구현
```python
def reset_all() :
        nonlocal death_count, player_pos, current_image, destructible_walls, movable_walls, level_map, break_count
        
        # 데스 카운트 추가
        death_count += 1

        # 플레이어 위치 초기화
        player_pos = initial_player_pos[:]
        current_image = player_images["down"]

        # 벽 부수기 횟수 초기화
        break_count = 0

        # 맵 초기화
        level_map = [row[:] for row in initial_level_map]

        # 파괴 가능한 벽 초기화
        destructible_walls = initial_destructible_walls[:]

        # 움직이는 벽 초기화
        movable_walls = initial_movable_walls[:]
```

#### 아이템, 리셋버튼 이미지 로드 및 획득 여부 기본값
```python
# 아이템 이미지 로드
item_image = pygame.image.load("image/test_item.png")
item_image = pygame.transform.scale(item_image, (TILE_SIZE, TILE_SIZE))  # 타일 크기에 맞게 조정

# 아이템 획득 여부 (기본값: False)
item_get = False

# 리셋 버튼 이미지 로드
    reset_btn = pygame.image.load("reset_btn.png")
    reset_btn = pygame.transform.scale(reset_btn, (TILE_SIZE, TILE_SIZE))  # 타일 크기에 맞게 조정
```

####  아이템 획득 여부 출력
```python
# 남은 벽 부수기 횟수와 데스 카운트, 아이템 획득 유무 출력
        info_text = font.render(f"Wall Breaks: {break_limit - break_count} | Death: {death_count}  | Acquire item : {item_get}", True, BLACK))
```

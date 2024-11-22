## 파이썬 응용 - 기말 프로젝트 팀 <해냈조>
### 튜토리얼 소스코드에 아이템 추가 및 획득 여부 구현

```python
destructible_items = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 5] # 아이템 위치를 찾아서 리스트 (x, y) 로 저장
```

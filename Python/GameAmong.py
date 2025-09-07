import pgzrun
import heapq
import time

TITLE = "Tìm đường đi trong mê cung"

TILE_SIZE = 50
WIDTH = TILE_SIZE * 20
HEIGHT = TILE_SIZE * 10

tiles = ['empty', 'wall', 'goal', 'spikes', 'key']
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 4, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

player = Actor('among_us', anchor=(0, 0), pos=(1 * TILE_SIZE, 1 * TILE_SIZE))
key_collected = False
path = []  # Đường đi từ A*
target_position = None  # Vị trí chìa khóa cần thu thập
came_from = {}  # Thêm biến để lưu đường đi
game_won = False
show_win_button = True

# Tạo một biến để kiểm tra xem trò chơi đã bắt đầu chưa
game_started = False

# Tạo hình ảnh nút "Start"
start_button = Actor('start_button', pos=(WIDTH // 2, HEIGHT // 2))

win_button = Actor('win_button', pos=(WIDTH // 2, HEIGHT // 2))

# Hàm tính khoảng cách Manhattan giữa hai điểm
def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Hàm tìm đường bằng thuật toán A*
def a_star(start, goal):
    open_list = []
    closed_set = set()

    heapq.heappush(open_list, (0, start))
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        closed_set.add(current)

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            x, y = current[0] + dx, current[1] + dy
            neighbor = (x, y)

            if neighbor in closed_set or maze[y][x] == 1:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in [item[1] for item in open_list]:
                heapq.heappush(open_list, (tentative_g_score + manhattan_distance(neighbor, goal), neighbor))
            elif tentative_g_score >= g_score.get(neighbor, 0):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score

    return None

# Hàm di chuyển nhân vật với độ trễ
def move_player():
    global key_collected, path, target_position, came_from, game_started, game_won
    if game_started:
        row = int(player.y / TILE_SIZE)
        column = int(player.x / TILE_SIZE)

        if not key_collected:
            if target_position is None:
                # Tìm chìa khóa gần nhất và tính đường đi đến nó
                key_position = find_nearest_key((column, row))
                if key_position:
                    target_position = key_position
                    came_from = {}
                    path = a_star((column, row), key_position)
                else:
                    pass

            if target_position and path:
                next_x, next_y = path.pop(0)
                x = next_x * TILE_SIZE
                y = next_y * TILE_SIZE
                player.x, player.y = x, y

                if (next_x, next_y) == target_position:
                    maze[next_y][next_x] = 0  # Xóa chìa khóa
                    target_position = None
                    key_collected = True
                    game_won = True

# Hàm với độ trễ để làm chậm việc di chuyển
def slow_move_player():
    move_player()
    time.sleep(0.1)  # Thêm độ trễ 0.1 giây vào mỗi lần di chuyển

# Hàm kiểm tra sự kiện nhấp chuột để bắt đầu trò chơi
def on_mouse_down(pos):
    global game_started, show_win_button
    if not game_started and start_button.collidepoint(pos):
        game_started = True
    elif game_won and show_win_button and win_button.collidepoint(pos):  # Kiểm tra show_win_button khi người chơi ấn vào nút "Win Game"
        show_win_button = False

def find_nearest_key(player_pos):
    keys = [(x, y) for y in range(len(maze)) for x in range(len(maze[0])) if maze[y][x] == 4]
    if not keys:
        return None
    nearest_key = min(keys, key=lambda key_pos: manhattan_distance(key_pos, player_pos))
    return nearest_key

def draw():
    screen.clear()
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))
    player.draw()

    # Hiển thị nút "Start" nếu trò chơi chưa bắt đầu
    if not game_started:
        start_button.draw()
    if game_won and show_win_button:  # Kiểm tra show_win_button trước khi vẽ nút "Win Game"
        win_button.draw()
    

def update():
    slow_move_player()
pgzrun.go()

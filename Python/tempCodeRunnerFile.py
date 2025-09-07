def on_mouse_down(pos):
    global game_started, show_win_button
    if not game_started and start_button.collidepoint(pos):
        game_started = True
    elif game_won and show_win_button and win_button.collidepoint(pos):  # Kiểm tra show_win_button khi người chơi ấn vào nút "Win Game"
        show_win_button = False
def print_board(board):
    """Display board in a 3x3 grid with position numbers for empty cells."""
    print("\n")
    for i in range(0, 9, 3):
        a = board[i] if board[i] != ' ' else str(i + 1)
        b = board[i+1] if board[i+1] != ' ' else str(i + 2)
        c = board[i+2] if board[i+2] != ' ' else str(i + 3)
        print(f" {a} | {b} | {c} ")
        if i < 6:
            print("---+---+---")
    print("\n")


# --- GAME RULES ---
node_count = 0
LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def winner(board):
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None


def moves(board):
    return [i for i, v in enumerate(board) if v == ' ']


def terminal(board):
    return winner(board) is not None or not moves(board)


def utility(board, me='O', opp='X'):
    w = winner(board)
    if w == me:
        return 1
    elif w == opp:
        return -1
    else:
        return 0


def minimax(board, player, me='O', opp='X'):
    global node_count
    node_count += 1
    if terminal(board):
        return utility(board, me, opp), None

    best_val = -2 if player == me else 2
    best_move = None

    for m in moves(board):
        b2 = board[:]
        b2[m] = player
        next_player = opp if player == me else me
        val, _ = minimax(b2, next_player, me, opp)

        if player == me and val > best_val:
            best_val, best_move = val, m
        elif player == opp and val < best_val:
            best_val, best_move = val, m

    return best_val, best_move


def alphabeta(board, player, alpha=-2, beta=2, me='O', opp='X'):
    global node_count
    node_count += 1
    if terminal(board):
        return utility(board, me, opp), None

    if player == me:
        best = (-2, None)  # MAX
        for m in moves(board):
            b2 = board[:]; b2[m] = player
            val, _ = alphabeta(b2, opp, alpha, beta, me, opp)
            if val > best[0]:
                best = (val, m)
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return best
    else:
        best = (2, None)   # MIN
        for m in moves(board):
            b2 = board[:]; b2[m] = player
            val, _ = alphabeta(b2, me, alpha, beta, me, opp)
            if val < best[0]:
                best = (val, m)
            beta = min(beta, val)
            if alpha >= beta:
                break
        return best


def play_game():
    board = [' ' for _ in range(9)]
    human = 'X'
    ai = 'O'

    print("Welcome to Tic-Tac-Toe (You are X, AI is O)")
    print_board(board)
    first = input("Do you want to go first? (y/n): ").strip().lower().startswith('y')
    current = human if first else ai

    while not terminal(board):
        if current == human:
            try:
                pos = int(input("Enter your move (1-9): ")) - 1
            except ValueError:
                print("Please enter a number 1-9.")
                continue
            if pos not in moves(board):
                print("Invalid move. Try again.")
                continue
            board[pos] = human
        else:
            print("AI is thinking...")
            global node_count
            node_count = 0
            _, m = alphabeta(board, player=ai, alpha=-2, beta=2, me=ai, opp=human)
            board[m] = ai
            print(f"AI chose position {m+1}")
            print(f"Nodes searched: {node_count}")

        print_board(board)
        current = ai if current == human else human

    w = winner(board)
    if w == human:
        print("🎉 You win!")
    elif w == ai:
        print("🤖 AI wins!")
    else:
        print("😐 It's a draw!")


if __name__ == "__main__":
    play_game()

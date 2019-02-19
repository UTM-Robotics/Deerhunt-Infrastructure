from threading import Lock

class Leaderboard:
    def __init__(self):
        self.max_len = 10
        self.lock = [Lock(),
                     Lock(),
                     Lock(),
                     Lock(),
                     Lock(),
                     Lock(),
                     Lock(),
                     Lock(),
                     Lock(),
                     Lock()]
        self.board = []

    def acquire(self, position):
        if position >= len(self.board):
            return None

        self.lock[position].acquire()
        return self.board[position]

    def release(self, position):
        self.lock[position].release()

    def replace(self, position, id):
        if position >= len(self.board):
            self.board.append(id)
            return
        
        self.board.insert(position, id)
        self.board.pop()

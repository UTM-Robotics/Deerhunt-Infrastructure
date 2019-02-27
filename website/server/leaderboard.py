from threading import Lock
from datetime import datetime

class Leaderboard:
    def __init__(self, collection):
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
        self.collection = collection

    def acquire(self, position):
        if position >= len(self.board):
            return None

        self.lock[position].acquire()
        return self.board[position]

    def release(self, position):
        self.lock[position].release()

    def save(self, match_id):
        self.collection.insert_one({'leaderboard': self.board, 
                                    'time': datetime.utcnow(),
                                    'takeover_match': match_id
                                    })

    def replace(self, position, id):
        if position >= len(self.board):
            self.board.append(id)
            return
        
        self.board.insert(position, id)
        self.board.pop()

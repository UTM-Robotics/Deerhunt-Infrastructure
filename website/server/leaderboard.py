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

        self.queue_lock = Lock()
        self.queue_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def acquire(self, position):
        if position >= len(self.board):
            return None

        self.queue_lock.acquire()
        self.queue_count[position] += 1
        self.queue_lock.release()

        self.lock[position].acquire()
        return self.board[position]

    def release(self, position):
        self.queue_count[position] -= 1
        self.lock[position].release()

    def is_locked(self, position):
        return self.lock[position].locked()

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

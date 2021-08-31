class EventsModel:
    def __init__(self, name):
        self.name = name
        self.game = None
        self.starttime = None
        self.endtime = None
        self.created_timestamp = None

    def set_name(self, name) -> None:
        self.name = name
    
    def get_name(self) -> str:
        return self.name

    def set_game(self, game) -> None:
        self.game = game

    def get_game(self):
        return self.game

    def set_starttime(self, starttime):
        self.starttime = starttime
    
    def get_starttime(self):
        return self.starttime

    def set_endtime(self, endtime):
        self.endtime = endtime

    def get_endtime(self):
        return self.endtime
 
    def set_created_timestamp(self, time) -> None:
        self.created_timestamp = time

    def get_created_timestamp(self) -> str:
        return self.created_timestamp

    def covert_to_dict(self) -> dict:
        return {'name': self.get_name(),
                'game': self.get_game(),
                'starttime': self.get_starttime(),
                'endtime': self.get_endtime(),
                'created_timestamp': self.get_created_timestamp()
                }
                
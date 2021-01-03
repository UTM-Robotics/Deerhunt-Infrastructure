import random
import math
import time
import threading

class TournamentController(threading.Thread):

    DEFENDER_IN_BATTLE = 1
    CHALLENGER_IN_BATTLE = 2
    

    def __init__(self, client, database, challenger=None):
        threading.Thread.__init__(self)
        self.client = client
        self.database = database
        self.is_running_tournament = False
        self.challenger = challenger

    def __enter__(self):
        self.session = self.client.start_session()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.end_session()
        self.session = None
        if exc_type is not None:
            return False
        return True

    def run(self):
        '''
        This runs when thread object calls .start()
        '''
        schedule.every().seconds.do(self.run_single_elimintation)
        while True:
                schedule.run_pending()
                time.sleep(1)

    def run_single_elimintation(self):
        pass

    def init_challenge(self, defender):
        session = self.session
        chal_user_file = self.database.users.find_one({"username": self.challenger}, session=self.session)
        chall_team = self.database.teams.find_one({"name": chal_user_file["team"]}, session=self.session)
        def_team = self.database.teams.find_one({"name": defender }, session=self.session)
        if def_team['is_fighting'] or chall_team['is_fighting']:
            return False
        return True
        
    
    def run_battle(self, position):
        leader = board.acquire(position)
        leader_path = f'{submissions_folder}/{leader}'

        if leader is None:
            board.replace(position, submit_folder)
            board.save('default')
            return 'Victory by default'

        uid = uuid.uuid4().hex
        build_path = f'{build_folder}/{uid}'

        shutil.copytree(template_folder, f'{build_path}/')
        copy_dir_contents(leader_path, f'{build_path}/p1')
        copy_dir_contents(submit_path, f'{build_path}/p2')
        shutil.copytree(server_folder, f'{build_path}/server')

        img = dock.images.build(path=build_path, tag=uid, rm=True, network_mode=None)
        container = dock.containers.run(uid, detach=True, auto_remove=True, network_mode=None,
                                        cpu_count=1, mem_limit='512m')

        lines = []
        maps = []
        errors = []

        for line in container.logs(stream=True):
            l = line.decode().strip()
            if 'ERROR:' == l[0:6]:
                errors.append(l[6:])
            elif 'MAP:' == l[0:4]:
                maps.append(l[4:])
            else:
                lines.append(l)

        lines = lines[3:]

        if 'Winner: p2' == lines[-1]:
            board.replace(position, submit_folder)
            board.save(uid)

        board.release(position)

        game_id = database.logs.insert_one({'lines': lines,
                                            'maps': maps,
                                            'errors': errors,
                                            'build_id': uid,
                                            'defender': leader,
                                            'challenger': submit_folder,
                                            'submitter': session['username']}).inserted_id

        return jsonify(game_id=str(game_id), message=lines[-1])
        


    @staticmethod
    def battle(player1: str, player2: str):
        '''
        Returns 0 if player1 wins.
        Returns 1 if player2 wins. 
        '''
        print(player1)
        print(player2)
        return random.randint(0,10) % 2


    def testjob(self):
        print("HI")

    @staticmethod
    def start_scheduler(client, database, time_seconds: int):
        def run_threaded(job_func):
            job_thread = threading.Thread(target=job_func)
            job_thread.start()
        with TournamentController(client, database, ) as tourney:
            schedule.every(time_seconds).seconds.do(tourney.testjob)
            while True:
                schedule.run_pending()
                time.sleep(1)
        

    
    
    
    
    # def run(self):
    #     '''
    #     Runs tournament battles until there is one top winner.
    #     '''
    #     res = []
    #     if len(self.init_teams_dict) > 1:
    #         self.init_teams_dict = TournamentLevel.shuffle(self.init_teams_dict)
    #         res = TournamentLevel.runTournament(self.init_teams_dict)
    #     return res


    # @staticmethod
    # def shuffle(submissions: list):
    #     '''
    #     This wrapper shuffles and rearranges list of dictionaries to be in the form [ 'teamname1', 'teamname2' ]
    #     Each dictionary represents a single team and their submission path.
    #     '''
    #     retList = submissions
    #     # for i in submissions:
    #     #     # This for loop makes a list of dictionaries. [{'team name': '/deerhunt/submission path'}, ... ,{}]
    #     #     temp = dict()
    #     #     temp[i] = submissions[i]
    #     #     retList.append(temp)
    #     print("original: ", submissions)
    #     random.shuffle(retList)
    #     print("list after shuffle ", retList)
    #     return list(retList)
    
    # @staticmethod
    # def create_empty_list(n: int):
    #     x = []
    #     for _ in range(n):
    #         x.append(list())
    #     return x

    # @staticmethod
    # def runTournament(rootList: list):
    #     '''
    #     Runs entire tournament simulation.
    #     Returns a single list
    #     [[], [], []]
    #     '''
    #     count = 0
    #     starting_teams = list()
    #     starting_teams.append(rootList) # [ ['alex2', 'kyrel', ...,'']]
    #     total_teams = len(rootList)
    #     rounds = math.floor(math.log(total_teams, 2))
    #     for _ in range(rounds):
    #         # temp.append(list())
    #         temp = TournamentLevel.create_empty_list(len(starting_teams)+1)
    #         print(starting_teams)

    #         num_brackets = len(starting_teams)
    #         for k in range(num_brackets):

    #             num_teams = len(starting_teams[k])
    #             if num_teams % 2 != 0:
    #                 num_teams -= 1
    #                 name = starting_teams[k][num_teams]
    #                 temp[k].append(name)
    #                 starting_teams[k].remove(name)

    #             for i in range(num_teams // 2):
    #                 player1 = starting_teams[k][i] #player1 is set to string "alex2" someteamname
    #                 player2 = starting_teams[k][num_teams - 1 - i]
    #                 result = TournamentLevel.battle(player1, player2) # STILL NEEDS TO BE WRITTEN
    #                 count +=1
    #                 if result == 0:
    #                     temp[k].append(player1)
    #                     temp[k+1].append(player2)
    #                 elif result == 1:
    #                     temp[k].append(player2)
    #                     temp[k+1].append(player1)
    #         starting_teams = temp

    #     temp = [[]]
    #     for i in range(len(starting_teams)):
    #         if i != 0:
    #             temp.append(starting_teams[i])
    #     print(starting_teams)
    #     num_brackets = len(starting_teams)
    #     num_teams = len(starting_teams[0])
    #     if num_teams % 2 != 0:
    #         num_teams -= 1
    #         name = starting_teams[k][num_teams]
    #         temp[k].append(name)
    #         starting_teams[k].remove(name)
    #     for i in range(num_teams // 2):
    #         player1 = starting_teams[0][i] #player1 is set to string "alex2" someteamname
    #         player2 = starting_teams[0][num_teams - 1 - i]
    #         result = TournamentLevel.battle(player1, player2) # STILL NEEDS TO BE WRITTEN
    #         count +=1
    #         if result == 0:
    #             temp[0].append(player1)
    #             temp[1].append(player2)
    #         elif result == 1:
    #             temp[0].append(player2)
    #             temp[1].append(player1)
    #     starting_teams = temp
    #     print("count: "+str(count))
    #     return starting_teams

        # for bracket in range(num_of_brackets):
        #     num_of_teams = len(rootList[bracket])
        #     for teams in range(num_of_teams // 2):
        #         player1 = rootList[bracket][teams]
        #         player2 = rootList[bracket][-1*(teams+1)]
        #         result = TournamentLevel.battle(player1, player2) # STILL NEEDS TO BE WRITTEN
        #         if result == 0:
        #             retList[bracket].append(player1)
        #             retList[bracket+1].append(player2)
        #         elif result == 1:
        #             retList[bracket].append(player2)
        #             retList[bracket].append(player1)
        #     if num_of_teams % 2 != 0:
        #         retList[bracket].append(rootList[bracket][num_of_teams // 2]) # Might have to update num of wins per team.
        # return retList

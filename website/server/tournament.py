import random

class TournamentLevel:

    def __init__(self, submissions: dict):
        self.init_teams_dict = submissions


    def run(self):
        '''
        Runs tournament battles until there is one top winner.
        '''
        res = []
        if len(self.init_teams_dict) > 1:
            self.init_teams_dict = TournamentLevel.shuffle(self.init_teams_dict)
            res = TournamentLevel.runTournament(self.init_teams_dict)
        return res


    @staticmethod
    def shuffle(submissions):
        '''
        This wrapper shuffles and rearranges list of dictionaries to be in the form [ ({}, {}), ({}, {}) ]
        Each dictionary represents a single team and their submission path.
        '''
        retList = list()
        for i in submissions:
            temp = dict()
            temp[i] = submissions[i]
            retList.append(temp)
        print("original: ", retList)
        random.shuffle(retList)
        print("list after shuffle ", retList)
        return list(retList)

    @staticmethod
    def runTournament(rootList: list):
        '''
        Runs entire tournament simulation.
        Returns a single list
        '''
        num_of_brackets = len(rootList)
        retList = list()
        for k in range(num_of_brackets):
            retList.append(list())
        retList.append(list())

        for bracket in range(num_of_brackets):
            num_of_teams = len(rootList[bracket])
            for teams in range(num_of_teams // 2):
                player1 = rootList[bracket][teams]
                player2 = rootList[bracket][-1*(teams+1)]
                result = battle(player1, player2) # STILL NEEDS TO BE WRITTEN
                if result == 0:
                    retList[bracket].append(player1)
                    retList[bracket+1].append(player2)
                elif result == 1:
                    retList[bracket].append(player2)
                    retList[bracket].append(player1)
            if num_of_teams % 2 != 0:
                retList[bracket].append(rootList[bracket][num_of_teams // 2]) # Might have to update num of wins per team.
        return retList

    @staticmethod
    def battle(player1: dict, player2: dict):
        '''
        Returns 0 if player1 wins.
        Returns 1 if player2 wins. 
        '''
        print(player1)
        print(player2)
        return random.randint(0,10) % 2

        # leader = board.acquire(position)
        # leader_path = f'{submissions_folder}/{leader}'

        # if leader is None:
        #     board.replace(position, submit_folder)
        #     board.save('default')
        #     return 'Victory by default'

        # uid = uuid.uuid4().hex
        # build_path = f'{build_folder}/{uid}'

        # shutil.copytree(template_folder, f'{build_path}/')
        # copy_dir_contents(leader_path, f'{build_path}/p1')
        # copy_dir_contents(submit_path, f'{build_path}/p2')
        # shutil.copytree(server_folder, f'{build_path}/server')

        # img = dock.images.build(path=build_path, tag=uid, rm=True, network_mode=None)
        # container = dock.containers.run(uid, detach=True, auto_remove=True, network_mode=None,
        #                                 cpu_count=1, mem_limit='512m')

        # lines = []
        # maps = []
        # errors = []

        # for line in container.logs(stream=True):
        #     l = line.decode().strip()
        #     if 'ERROR:' == l[0:6]:
        #         errors.append(l[6:])
        #     elif 'MAP:' == l[0:4]:
        #         maps.append(l[4:])
        #     else:
        #         lines.append(l)

        # lines = lines[3:]

        # if 'Winner: p2' == lines[-1]:
        #     board.replace(position, submit_folder)
        #     board.save(uid)

        # board.release(position)

        # game_id = database.logs.insert_one({'lines': lines,
        #                                     'maps': maps,
        #                                     'errors': errors,
        #                                     'build_id': uid,
        #                                     'defender': leader,
        #                                     'challenger': submit_folder,
        #                                     'submitter': session['username']}).inserted_id

        # return jsonify(game_id=str(game_id), message=lines[-1])
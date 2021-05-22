'''Controls all game related'''

import uuid
import docker


class GameController:
    ''' Performs all Teams-related logic with Database.'''
    dock = None

    @staticmethod
    def run_game(container_path):
        ''' Runs a game match in a docker container and generates the game state output.
            The container should be tagged on creation, and will be run using the tag.
        '''
        # Ensures docker object is initialized.
        if not GameController.dock:
            GameController.dock = docker.from_env()

        container_tag = uuid.uuid4().hex
        # Generate Docker image.
        GameController.dock.images.build(
            path=container_path, tag=container_tag, rm=True, network_mode=None)
        # Runs Docker Container using the generated image.
        container = GameController.dock.containers.run(container_tag, detach=True,\
             auto_remove=True, network_mode=None, cpu_count=1, mem_limit='512m')

        lines = []
        maps = []
        errors = []
        # Decode output from server per turn.
        for line in container.logs(stream=True):
            decoded_line = line.decode().strip()
            if decoded_line[0:6] == 'ERROR:':
                errors.append(decoded_line[6:])
            elif decoded_line[0:4] == 'MAP:':
                maps.append(decoded_line[4:])
            else:
                lines.append(decoded_line)
        # Remove first three boilerplate lines.
        lines = lines[3:]

        match_result = {'lines': lines,
                        'maps': maps,
                        'errors': errors,
                        'build_id': container_tag
                        }
        if lines[-1] == 'Winner: p2':
            winner = 2
        elif lines[-1] == 'Winner: p1':
            winner = 2
        elif "Waiting for client 2..." in lines:
            winner = 1
        else: 
            winner = 2
        return (match_result, winner)

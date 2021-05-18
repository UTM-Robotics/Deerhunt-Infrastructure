* AI Competition Framework
  This is the website and game that was built by me for NeoDeerhunt.
  NeoDeerhunt was an overnight competition where teams of three
  competed to build the best bot for the given game. A public leaderboard
  was displayed and participants could challenge people on the leaderboard
  to take their position and knock everybody below them down.
  

  The game was loosely inspired by starcraft. It has the following features:
  - Turn based
  - Horizontally symmetrical 2D grid maps
    - Contains walls and resources
  - Two types of units per player
    - Worker units
      - Can mine resources
    - Fighter units
      - Can attack other units
      - Can spend resources to duplicate
        

  The website was written in =flask= with =react.js= on the front end. It
  uses =mongodb= for storage and code submissions are run inside of a =docker=
  container. When a submission is made a new docker container is built and
  run. The replay and results of the match are extracted through docker logs.
  
  The itself game was written in =python= and uses a simple server (to control the game state)
  and two simple clients (one for each player). The client was designed to
  be easy for people to understand and implement. Classes that manage the connection to
  the server and provide useful utilities are provided so the player can
  focus on implementing their strategy for the game.

  
  The =README= s in each components folder provide more technical information
  on how to set up and run this for yourself.
  

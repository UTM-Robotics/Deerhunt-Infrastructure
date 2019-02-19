import React from 'react';
import GameBoard from './GameBoard';

class Replay extends React.Component {

    constructor() {
        super();
        this.state = {
            gameId: "",
            moves: [
            [
                ["x", "x", "x", "x"],
                ["x", "", "m", "x"],
                ["x", "m", "", "x"],
                ["x", "x", "x", "x"]
            ],
            [
                ["x", "x", "x", "x"],
                ["x", "m", "", "x"],
                ["x", "m", "", "x"],
                ["x", "x", "x", "x"]
            ],
            [
                ["x", "x", "x", "x"],
                ["x", "m", "", "x"],
                ["x", "", "m", "x"],
                ["x", "x", "x", "x"]
            ],
            [
                ["x", "x", "x", "x"],
                ["x", "m", "m", "x"],
                ["x", "", "", "x"],
                ["x", "x", "x", "x"]
            ]
            
            ]
        }
    }

    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.findGame();
        }
    }

    findGame() {
        console.log(this.state.gameId);
    }

    handleGameIdChange(e) {
        this.setState({
            gameId: e.target.value
        });
    }

    render() {
        console.log(this.state.moves);
        return (
            <div>
                <h1>Game Replay</h1>
                <input type="text" placeholder="Game Id" onChange={this.handleGameIdChange.bind(this)} />
                <div className="auth-button" onClick={this.findGame.bind(this)}>enter</div>
                <GameBoard
                    moves = {this.state.moves}
                />
            </div>
        );
    }
}

export default Replay;

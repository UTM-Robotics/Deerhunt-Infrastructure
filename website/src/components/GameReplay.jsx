import React from 'react';
import GameBoard from './GameBoard';
import $ from 'jquery';


class Replay extends React.Component {

    constructor() {
        super();
        this.state = {
            gameId: "",
            moves: "",
            currentMove: [],
            display: false,
            loggedIn: false
        }
    }

    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.findGame();
        }
    }

    findGame() {
        this.setState({
            display: true,
            moves: [
                [
                    ["x", "x", "x", "x"],
                    ["x", " ", "m", "x"],
                    ["x", "m", " ", "x"],
                    ["x", "x", "x", "x"]
                ],
                [
                    ["x", "x", "x", "x"],
                    ["x", "m", " ", "x"],
                    ["x", "m", " ", "x"],
                    ["x", "x", "x", "x"]
                ],
                [
                    ["x", "x", "x", "x"],
                    ["x", "m", " ", "x"],
                    ["x", " ", "m", "x"],
                    ["x", "x", "x", "x"]
                ],
                [
                    ["x", "x", "x", "x"],
                    ["x", "m", "m", "x"],
                    ["x", " ", " ", "x"],
                    ["x", "x", "x", "x"]
                ]
            ]
        });

    }


    componentDidMount() {
        this.isLoggedIn();
    }

    isLoggedIn() {
        $.ajax({
            url: '/api/isloggedin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true: false;
                if (parsed) {
                    this.setState({
                        loggedIn: parsed
                    });
                }
                else {
                    window.location.replace("/");
                }
            }
        });
    }

    getBoard() {
        return (
            <GameBoard moves = {this.state.moves} display={this.state.display} />
        );
    }

    changeMove(move) {
        this.setState({
            currentMove: move
        });
    }

    handleGameIdChange(e) {
        this.setState({
            gameId: e.target.value
        });
    }

    render() {
        var move = this.state.currentMove;
        return (
            this.state.loggedIn && <div>
                <h1>Game Replay</h1>
                <input type="text" placeholder="Game Id" onChange={this.handleGameIdChange.bind(this)} />
                <button className="auth-button" onClick={this.findGame.bind(this)}>enter</button>
                {this.getBoard()}
            </div>
        );
    }
}

export default Replay;

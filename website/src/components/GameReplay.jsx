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

    addError(type: string) {
        $('.error-message').remove();
        var message = "";
        if (type === 'id') {
            message = "Please enter a game id";
        }
        else {
            message = "The game id is incorrect/invalid"
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.auth-button').after(errorMessage);
    }


    findGame() {
        if (this.state.gameId == "") {
            this.addError("id");
            return;
        }
        
        const requestData = JSON.stringify({
            "game_id": this.state.gameId
        });
        
        $.ajax({
            url: '/api/getmatch',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                this.setState({
                    display: true,
                    moves: responseData.map(x => JSON.parse(x))
                });
            },
            error: () => {
                this.addError("");
                return;
            }
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

    handleGameIdChange(e) {
        this.setState({
            gameId: e.target.value
        });
    }

    render() {
        var move = this.state.currentMove;
        return (
            this.state.loggedIn && <div className="replay-container">
                <h1>Game Replay</h1>
                <input type="text" placeholder="Game Id" onChange={this.handleGameIdChange.bind(this)} />
                <button className="replay-button" onClick={this.findGame.bind(this)}>enter</button>
                {this.getBoard()}
            </div>
        );
    }
}

export default Replay;

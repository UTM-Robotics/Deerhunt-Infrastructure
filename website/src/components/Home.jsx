import React from 'react';
import $ from 'jquery';
import ChallengeButton from './ChallengeButton';
import ScrimmageButton from './ScrimmageButton';

class Home extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            canCompete: true,
            rank: -1,
            leaderboard: [],
            displayLeaderboard: false
        };
        this.competeError = this.competeError.bind(this);
        this.reloadAllData = this.reloadAllData.bind(this);
    }

    componentDidMount() {
        this.displayLeaderboard();
        this.getLeaderboard();
        this.getRank();
        this.getCanCompete();
        this.isLoggedIn();
    }

    reloadAllData() {
        this.getLeaderboard();
        this.getRank();
        this.getCanCompete();
    }

    getCanCompete() {
        /* $.ajax({
             url: '/api/canchallenge',
             type: 'GET',
             success: (responseData) => {
                 this.setState({
                     canCompete: responseData
                 });
             }
         });*/
    }

    getRank() {
        $.ajax({
            url: '/api/rank',
            type: 'GET',
            success: (responseData) => {
                this.setState({
                    rank: responseData["rank"]
                });
            }
        });
    }

    competeError(type) {
        var message = "";
        if (type === 'cup') {
            message = "Cannot Scrimmage against this player."
        }
        else if (type === 'nep') {
            message = "Please submit before requesting scrimmage";
        }
        this.setState({ errorMessage: message })
    }
    getLeaderboard() {
        $.ajax({
            url: '/api/leaderboard',
            type: 'GET',
            success: (responseData) => {
                this.setState({
                    leaderboard: responseData
                });
            }
        });
    }

    displayLeaderboard() {
        $.ajax({
            url: '/api/leaderboardtoggle',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true : false;
                this.setState({
                    displayLeaderboard: parsed
                });
            }
        });
    }


    isLoggedIn() {
        $.ajax({
            url: '/api/isloggedin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true : false;
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

    render() {
        return (
            this.state.loggedIn && <div className="home-container">
                {(this.state.displayLeaderboard && this.state.leaderboard.length > 0) && <h1>Leaderboard</h1>}
                {(!this.state.displayLeaderboard || this.state.leaderboard.length === 0) && <h1>Leaderboard Hidden</h1>}
                <p>{this.state.errorMessage}</p>
                {this.state.leaderboard.length > 0 && this.state.displayLeaderboard && <table align="center">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Team</th>
                            <th>Challenge</th>
                            <th>Scrimmage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.leaderboard.map((item, key) => (
                            <tr key={key}>
                                <td className="num">{key + 1}</td>
                                <td className="item">{item.name}</td>
                                <td className="item">{(this.state.rank != -1 &&
                                    key < this.state.rank && this.state.canCompete) &&
                                    <ChallengeButton team={item.name} />}</td>
                                <td className="item">{(key != this.state.rank && this.state.canCompete) &&
                                 <ScrimmageButton team={item.name} errorCallback={this.competeError} />}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>}
            </div>
        );
    }
}

export default Home;

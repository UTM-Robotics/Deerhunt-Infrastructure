import React from 'react';
import $ from 'jquery';
import ChallengeButton from './ChallengeButton';
import ScrimmageButton from './ScrimmageButton';

class Home extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            displayLeaderboard: false,
            canCompete: true,
            rank: -1,
            leaderboard: [],
            queue: []

        };
        this.addCompeteError = this.addCompeteError.bind(this);
        this.reloadAllData = this.reloadAllData.bind(this);
        this.addSuccessMessage = this.addSuccessMessage.bind(this);

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

    getQueue(){
        $.ajax({
             url: '/api/queue',
             type: 'GET',
             success: (responseData) => {
                 this.setState({
                     queue: responseData
                 });
             }
         });
     }

    getCanCompete(){
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
    gethasSubmitted() {
         $.ajax({
             url: '/api/canchallenge',
             type: 'GET',
             success: (responseData) => {
                 this.setState({
                     canCompete: responseData
                 });
             }
         });
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

    addCompeteError(type) {
        var message = "";
        if (type === 'fail_scrimmage') {
            message = "Cannot scrimmage against this player. Are you in queue?"
        }
        else if (type === 'fail_challenge') {
            message = "Cannot challenge this player. Are you in queue?"
        }
        this.setState({ errorMessage: message });
    }

    addSuccessMessage(type) {
        this.setState({
            errorMessage: "",
            successMessage: "Success, we are computing your match! Please wait, you may be queued."
        });
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
                <p className='error-message'>{this.state.errorMessage}</p>
                <p className='success-message'>{this.state.successMessage}</p>

                <p>Competing is throttled at once every 5 minutes. Be sure when you click that button!</p>
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
                                <td className="item">
                                    {((this.state.rank === -1 ||
                                        key < this.state.rank) && this.state.canCompete) &&
                                        <ChallengeButton
                                            rank={key}
                                            errorCallback={this.addCompeteError}
                                            successCallback={this.addSuccessMessage}
                                            reloadCallback={this.reloadAllData}
                                        />
                                    }
                                </td>
                                <td className="item">
                                    {(key != this.state.rank && this.state.canCompete) &&
                                        <ScrimmageButton
                                            rank={key}
                                            errorCallback={this.addCompeteError}
                                            successCallback={this.addSuccessMessage}
                                            reloadCallback={this.reloadAllData}
                                        />
                                    }
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>}
            </div>
        );
    }
}

export default Home;

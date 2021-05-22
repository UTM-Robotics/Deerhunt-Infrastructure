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
        this.onScrimmageError = this.onScrimmageError(this);
        this.reloadAllData = this.reloadAllData.bind(this);
        this.addSuccessMessage = this.addSuccessMessage.bind(this);
        this.addLoadingState = this.addLoadingState.bind(this);
        this.scrimmageCallback =this.scrimmageCallback.bind(this);
    }

    componentDidMount() {
        this.displayLeaderboard();
        this.getLeaderboard();
        this.getRank();
        this.getCanCompete();
        this.isLoggedIn();
    }

    addLoadingState() {
        this.setState({
            errorMessage: "",
            successMessage: "Your match is computing or in queue. If your game computes, it will appear in Team History."
        });
    }
    reloadAllData() {
        this.getLeaderboard();
        this.getRank();
        this.getCanCompete();
    }

    getQueue() {
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

    getHasSubmitted() {
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

    onScrimmageError(){
        console.log("OnScrimmageError");
        this.addCompeteError('fail_scrimmage');
    }

    addCompeteError(type) {
        var message = "";
        if (type === 'fail_scrimmage') {
            message = "Cannot scrimmage against this player. you may have scrimmaged\
             in the last minute. Please wait for cooldown"
        }
        else if (type === 'fail_challenge') {
            message = "Cannot challenge this player. Are you in queue? Otherwise,\
             you may have challenged in the last 5 minutes. Please wait for cooldown"
        }
        this.setState({
            errorMessage: message,
            successMessage: ""
        });
    }

    scrimmageCallback(rank){
        const requestData = JSON.stringify({
            "target_rank": rank,
        });
        this.addLoadingState();

        $.ajax({
            url: '/api/scrimmage',
            type: 'POST',
            data: requestData,
            async: true,
            timeout: 90000,
            contentType: 'application/json',
            success: (responseData) => {
                this.reloadAllData();
                this.addSuccessMessage("");
                console.log("We did a thing, response received.");
            },
            statusCode:{
                400:this.onScrimmageError
            }
        });
    }

    addSuccessMessage(message) {
        this.setState({
            errorMessage: "",
            successMessage: "Success, we are computing your match! Check your team for the results."
        });
        return;
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

                <p>Challenging is throttled at once every 5 minutes, scrimmaging once every minute. Be sure when you click that button!</p>
                <p>Please note that a battle takes anywhere from 5-15 seconds to run so the page may look like it
                is loading during that time. In addition if other people are challenging you will be queued and
                it will take longer for your challenge to go through.
                    </p>
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
                                            loadingCallback={this.addLoadingState}
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
                                            scrimmageCallback={this.scrimmageCallback}
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

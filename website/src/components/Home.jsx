import React from 'react';
import $ from 'jquery';

class Home extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            leaderboard: [],
            displayLeaderboard: false
        };
    }

    componentDidMount() {
        this.displayLeaderboard();
        this.getLeaderboard();
        this.isLoggedIn();
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
                var parsed = responseData == "True" ? true: false;
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

    render() {
        return (
            this.state.loggedIn && <div className="home-container">
                {(this.state.displayLeaderboard && this.state.leaderboard.length > 0) && <h1>Leaderboard</h1>}
                {(!this.state.displayLeaderboard || this.state.leaderboard.length === 0) && <h1>Leaderboard Hidden</h1>}
                {this.state.leaderboard.length > 0 && this.state.displayLeaderboard && <table align="center">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Team</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.leaderboard.map((item, key) => (
                            <tr key={key}>
                                <td className="num">{key + 1}</td>
                                <td className="item">{item.name}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>}
            </div>
        );
    }
}

export default Home;

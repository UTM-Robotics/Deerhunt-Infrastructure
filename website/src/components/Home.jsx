import React from 'react';
import $ from 'jquery';

class Home extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            leaderboard: []
        };
    }

    componentDidMount() {
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
                <h1>Leaderboard</h1>
                <table align="center">
                    <tbody>
                        {this.state.leaderboard.length > 0 && this.state.leaderboard.map((item, key) => (
                            <tr key={key}><td className="num">{key + 1}</td><td className="item">{item}</td></tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Home;

import React from 'react';
import $ from 'jquery';

class Home extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: true,
            leaderboard: []
        };
    }

    componentDidMount() {
        //this.isLoggedIn();
        this.getLeaderboard();
    }

    getLeaderboard() {
        console.log("inside");
        $.ajax({
            url: '/api/leaderboard',
            type: 'GET',
            success: (responseData) => {
                console.log(responseData);
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
                
                </div>
        );
    }
}

export default Home;

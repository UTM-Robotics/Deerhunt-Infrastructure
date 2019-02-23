import React from 'react';
import $ from 'jquery';

class LeaderboardStatus extends React.Component {
    constructor() {
        super();
        this.state = {
            status: ""
        }
    }

    componentDidMount() {
        this.getStatus();
    }

    getStatus() {
        $.ajax({
            url: '/api/leaderboardtoggle',
            type: 'GET',
            success: (responseData) => {
                this.setState({
                    status: responseData
                });
            }
        });
    }

    toggleStatus() {
        $.ajax({
            url: '/api/leaderboardtoggle',
            type: 'POST',
            success: () => {
                location.reload();
            }
        });
    }

    render() {
        return (
            <div className="status">
                <h1>Leaderboard Status</h1>
                <p>Status: {this.state.status}</p>
                <div className="toggle-button" onClick={this.toggleStatus.bind(this)}>Toggle</div>
            </div>
        );
    }
}

export default LeaderboardStatus;

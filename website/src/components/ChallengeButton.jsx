import React from 'react';
import $ from 'jquery';

class ChallengeButton extends React.Component {
    constructor() {
        super();
    }

    challenge() {
        const requestData = JSON.stringify({
            "target_team": this.props.team,
        });

        $.ajax({
            url: '/api/challenge',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                this.props.reloadCallback();

            },
            error: (err) => {
                console.log(err);
                this.props.errorCallback("fail_accept");
            }
        });
    }
    render() {
        return (
            <div className="leaderboard-button" onClick={this.challenge.bind(this)}>Challenge</div>
        );
    }
}

export default ChallengeButton;
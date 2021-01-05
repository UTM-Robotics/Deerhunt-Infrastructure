import React from 'react';
import $ from 'jquery';

class ChallengeButton extends React.Component {
    constructor() {
        super();
    }

    challenge() {
        const requestData = JSON.stringify({
            "target_rank": this.props.rank,
        });
        this.props.loadingCallback();
        $.ajax({
            url: '/api/challenge',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                this.props.reloadCallback();
                this.props.successCallback("");
            },
            error: (err) => {
                console.log(err);
                this.props.errorCallback("fail_challenge");
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
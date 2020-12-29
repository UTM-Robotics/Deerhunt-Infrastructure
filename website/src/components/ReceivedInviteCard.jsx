import React from 'react';
import $ from 'jquery';

class ReceivedInviteCard extends React.Component {
    constructor() {
        super();
        this.state = {
            "team": "",
            "team_display": ""
        }
    }

    acceptInvite() {
        const requestData = JSON.stringify({
            "team": this.state.team,
        });

        $.ajax({
            url: '/api/acceptinvite',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                alert('Success');
            },
            error: (err) => {
                console.log(err);
                alert('Error');
            }
        });
    }
    render() {
        return (
            <div className="invite-card">
                <h2>Team name: {this.state.team_display}</h2>
                <div className="invite-button" onClick={this.acceptInvite.bind(this)}>Accept Invite</div>
            </div>
        );
    }
}

export default ReceivedInviteCard;

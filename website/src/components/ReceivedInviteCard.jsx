import React from 'react';
import $ from 'jquery';

class ReceivedInviteCard extends React.Component {
    constructor() {
        super();
        this.state = {
            "team": "",
            "team_display": "",
            "reloadCallback": ()=>{},
            "errorCallback": (string)=>{}
        }
    }

    acceptInvite() {
        const requestData = JSON.stringify({
            "team": this.props.team,
        });

        $.ajax({
            url: '/api/acceptinvite',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                reloadCallback();

            },
            error: (err) => {
                console.log(err);
                errorCallback("fail_accept");
            }
        });
    }
    render() {
        return (
            <div className="invite-card">
                <h2>Team name: {this.props.team_display}</h2>
                <div className="invite-button" onClick={this.acceptInvite.bind(this)}>Accept Invite</div>
            </div>
        );
    }
}

export default ReceivedInviteCard;

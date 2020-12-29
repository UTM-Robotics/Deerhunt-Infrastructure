import React from 'react';
import $ from 'jquery';

class SentInviteCard extends React.Component {
    constructor() {
        super();
        this.state = {
            "username": "",
        }
    }
    render() {
        return (
            <div className="invite-card">
                <h2>username: {this.state.username}</h2>
            </div>
        );
    }
}

export default SentInviteCard;

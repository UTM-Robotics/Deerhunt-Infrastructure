import React from 'react';
import $ from 'jquery';

class SentInviteCard extends React.Component {
    constructor() {
        super();
        this.state = {
        }
    }
    render() {
        return (
            <div className="invite-card">
                <h5>Invite sent to: {this.props.username}</h5>
            </div>
        );
    }
}

export default SentInviteCard;

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
                <h4>Invite sent to: {this.props.username}</h4>
            </div>
        );
    }
}

export default SentInviteCard;

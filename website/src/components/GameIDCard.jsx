import React from 'react';
import $ from 'jquery';

class GameIDCard extends React.Component {
    constructor() {
        super();
    }
    render() {
        console.log(this.props.gameID);
        return (
            <div className="invite-card">
                <h4>GameID: {this.props.gameID}</h4>
            </div>
        );
    }
}

export default GameIDCard;

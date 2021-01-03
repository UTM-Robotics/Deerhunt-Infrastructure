import React from 'react';
import $ from 'jquery';

class GameIDCard extends React.Component {
    constructor() {
        super();
    }
    render() {
        console.log(this.props.gameID);
        return (
            <div className="gameid-card">
                <p>GameID: {this.props.gameID}</p>
            </div>
        );
    }
}

export default GameIDCard;

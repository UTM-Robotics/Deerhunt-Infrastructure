import React from 'react';
import $ from 'jquery';
class ScrimmageButton extends React.Component {
    constructor() {
        super();
    }

    scrimmage() {
        this.props.scrimmageCallback(this.props.rank);
    }
    render() {
        return (
            <div className="leaderboard-button" onClick={this.scrimmage.bind(this)}>Scrimmage</div>
        );
    }
}

export default ScrimmageButton;
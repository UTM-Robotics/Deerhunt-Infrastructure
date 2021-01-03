import React from 'react';
import $ from 'jquery';
class ScrimmageButton extends React.Component {
    constructor() {
        super();
    }

    scrimmage() {
        const requestData = JSON.stringify({
            "target_rank": this.props.rank,
        });
        this.props.loadingCallback();
        $.ajax({
            url: '/api/scrimmage',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                this.props.reloadCallback();
                this.props.successCallback();
            },
            error: (err) => {
                console.log(err);
                this.props.errorCallback("fail_scrimmage");
            },
            timeout: 60000// sets timeout to 60 seconds,
        });
    }
    render() {
        return (
            <div className="leaderboard-button" onClick={this.scrimmage.bind(this)}>Scrimmage</div>
        );
    }
}

export default ScrimmageButton;
import React from 'react';
import $ from 'jquery';

class ServerReset extends React.Component {
    constructor() {
        super();
    }

    componentDidMount() {
    }

    reloadStatus() {
        $.ajax({
            url: '/api/initglobalstate',
            type: 'POST',
            success: () => {
                this.props.reloadParent();
            }
        });
    }

    render() {
        return (
            <div className="status">
                <h1>Reset Server Status</h1>
                <div className="toggle-button" onClick={this.reloadStatus.bind(this)}>
                    Reset Server State
                </div>
            </div>
        );
    }
}

export default ServerReset;

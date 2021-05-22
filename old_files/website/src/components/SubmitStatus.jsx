import React from 'react';
import $ from 'jquery';

class SubmitStatus extends React.Component {
    constructor() {
        super();
        this.state = {
            status: ""
        }
    }

    componentDidMount() {
        this.getStatus();
    }

    getStatus() {
        $.ajax({
            url: '/api/submittoggle',
            type: 'GET',
            success: (responseData) => {
                this.setState({
                    status: responseData
                });
            }
        });
    }

    toggleStatus() {
        $.ajax({
            url: '/api/submittoggle',
            type: 'POST',
            success: () => {
                location.reload();
            }
        });
    }

    render() {
        return (
            <div className="status">
                <h1>Submit Status</h1>
                <p>Status: {this.state.status}</p>
                <div className="toggle-button" onClick={this.toggleStatus.bind(this)}>Toggle</div>
            </div>
        );
    }
}

export default SubmitStatus;

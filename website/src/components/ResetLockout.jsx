import React from 'react';
import $ from 'jquery';

class ResetLockout extends React.Component {
    constructor() {
        super();
        this.state = {
            "user": ""
        }
    }

    resetlockout() {
        if (this.state.user == "") {
            this.addLoginError('user');
            return;
        }
        const requestData = JSON.stringify({
            "username": this.state.user
        });

        $.ajax({
            url: '/api/resetlockout',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: (responseData) => {
                alert('Success');
            },
            error: (err) => {
                console.log(err);
                alert('Error');
            }
        });
    }
    
    handleUserChange(e) {
        this.setState({
            user: e.target.value
        });
    }

    render() {
        return (
            <div className="status">
                <h1>Reset Lockout</h1>
                <form>
                    <input type="text" placeholder="username" onChange={this.handleUserChange.bind(this)} 
                           style={{marginBottom: '10px'}} />
                    <div className="toggle-button" onClick={this.resetlockout.bind(this)}>clear</div>
                </form>
            </div>
        );
    }
}

export default ResetLockout;

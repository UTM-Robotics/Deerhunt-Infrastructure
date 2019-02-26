import React from 'react';
import $ from 'jquery';

class Profile extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            username: "",
            currentPassword: "",
            newPassword: "",
            confirmPassword: ""
        };
    }

    componentDidMount() {
        this.isLoggedIn();
    }

    isLoggedIn() {
        $.ajax({
            url: '/api/isloggedin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true: false;
                if (parsed) {
                    this.setState({
                        loggedIn: parsed
                    });
                }
                else {
                    window.location.replace("/");
                }
            }
        });
    }

    handleCurrentPasswordChange(e) {
        this.setState({
            currentPassword: e.target.value
        });
    }

    handleNewPasswordChange(e) {
        this.setState({
            newPassword: e.target.value
        });
    }

    handleConfirmPasswordChange(e) {
        this.setState({
            confirmPassword: e.target.value
        });
    }

    change() {
        console.log("change password");
    }

    render() {
        return (
             this.state.loggedIn && <div className="profile-container">
              <h1>Profile</h1>
                <form className="change-form" id="change-form">
                    <input type="password" placeholder="current password" onChange={this.handleCurrentPasswordChange.bind(this)} />
                    <input type="password" placeholder="new password" onChange={this.handleNewPasswordChange.bind(this)} />
                    <input type="password" placeholder="confirm new password" onChange={this.handleConfirmPasswordChange.bind(this)} />
                    <div className="register-button" onClick={this.change.bind(this)}>update</div>
                </form>
            </div>
        );
    }
}

export default Profile;

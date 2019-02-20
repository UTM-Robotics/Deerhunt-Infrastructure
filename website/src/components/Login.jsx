import React from 'react';

class Login extends React.Component {
    constructor() {
        super();
        this.state = {
            email: "",
            password: "",
            username: ""
        }
    }

    componentWillMount() {
        document.addEventListener("keypress", this.handleEnterKeyPress.bind(this));
    }

    addError(type: string) {
        var message = "";
        if (type === 'email1') {
            message = "Please enter a email";
        }
        else if (type === 'email2') {
            message = "Please enter a valid email";
        }
        else if (type === 'password1') {
            message = "Please enter a password";
        }
        else if (type === 'login') {
            message = "The username or password is incorrect/invalid";
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.auth-button').after(errorMessage);
    }

    handleEnterKeyPress(e: any) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.login();
        }
    }

    handleEmailChange(e: any) {
        this.setState({
            email: e.target.value
        });
    }

    handlePasswordChange(e: any) {
        this.setState({
            password: e.target.value
        });
    }
    
    render() {
        return (
            <div className="auth-form-container">
                <form className="login-form" id="login-form">
                    <input type="text" placeholder="email" onChange={this.handleEmailChange.bind(this)} />
                    <input type="password" placeholder="password" onChange={this.handlePasswordChange.bind(this)} />
                    <div className="auth-button">login</div>
                </form>
            </div>

        );
    }
}

export default Login;

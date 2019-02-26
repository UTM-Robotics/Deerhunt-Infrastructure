import React from 'react';
import { Link } from 'react-router-dom';
import $ from 'jquery';

class AppWrapper extends React.Component {
    constructor() {
        super();
        this.state = {
            loggedIn: false
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
                this.setState({
                    loggedIn: responseData == "True" ? true: false
                });
            }
        });
    }
    
    render() {
        return (
            <div className='app-container'>
                {this.state.loggedIn && <div className="nav-container">
                    <Link className="nav-link" to={'/home'}>Home</Link>
                    <Link className="nav-link" to={'/replay'}>Game Replay</Link>
                    <Link className="nav-link" to={'/submit'}>Submit</Link>
                    <Link className="nav-link" to={'/profile'}>Profile</Link>
                </div>}
                <div className="content-container">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default AppWrapper;

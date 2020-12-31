import React from 'react';
import { Link } from 'react-router-dom';
import $ from 'jquery';
import deerhuntLogo from './../assets/images/deerhuntLogo.png';

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
                    loggedIn: responseData == "True" ? true : false
                });
            }
        });
    }

    render() {
        return (
            <div className='app-container'>
                <div className='app-header-container'>
                    <h1>Battlecode: Deerhunt</h1>
                </div>
                {this.state.loggedIn && <div className="nav-container">
                    <Link className="nav-link" to={'/home'}>Home</Link>
                    <Link className="nav-link" to={'/replay'}>Game Replay</Link>
                    <Link className="nav-link" to={'/submit'}>Submit</Link>
                    <Link className="nav-link" to={'/profile'}>Profile</Link>
                    <Link className="nav-link" to={'/teams'}>Teams</Link>
                </div>}
                <div className="content-container">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default AppWrapper;

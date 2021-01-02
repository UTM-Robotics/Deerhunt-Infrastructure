import React from 'react';
import { Link } from 'react-router-dom';
import $ from 'jquery';
import mcssLogo from './../assets/images/mcsslogo.png';
import utmRoboticsLogo from './../assets/images/UTMRoboticslogo.png';

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
                    <img src={mcssLogo} alt="MCSS Logo" className="headerLogo"/>
                    <h1 className="shine">Battlecode: Deerhunt</h1>
                    <img src={utmRoboticsLogo} alt="UTM Robotics Logo" className="headerLogo"/>
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

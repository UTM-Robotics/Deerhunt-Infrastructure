import React from 'react';
import { Link } from 'react-router-dom';

class AppWrapper extends React.Component {
    constructor() {
        super();
        this.state = {
            loggedIn: false
        };
    }
    
    render() {
        return (
            <div className='app-container'>
                {this.state.loggedIn && <div className="nav-container">
                    <Link className="nav-link" to={'/home'}>Home</Link>
                    <Link className="nav-link" to={'/profile'}>Profile</Link>
                    <Link className="nav-link" to={'/replay'}>Game Replay</Link>
                    <Link className="nav-link" to={'/submit'}>Submit</Link>
                </div>}
                <div className="content-container">
                    {this.props.children}
                </div>
            </div>
        );
    }
}

export default AppWrapper;

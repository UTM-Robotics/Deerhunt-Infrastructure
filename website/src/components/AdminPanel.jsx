import React from 'react';
import $ from 'jquery';
import Register from './Register';
import LeaderboardStatus from './LeaderboardStatus';
import SubmitStatus from './SubmitStatus';


class AdminPanel extends React.Component {
    constructor() {
        super();
    }

    render() {
        return (
            <div>
                <Register />
                <div className="status-container">
                    <LeaderboardStatus />
                    <SubmitStatus />
                </div>
            </div>
        );
    }
}
export default AdminPanel;

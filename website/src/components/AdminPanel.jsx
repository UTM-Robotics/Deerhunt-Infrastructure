import React from 'react';
import $ from 'jquery';
import Register from './Register';
import LeaderboardStatus from './LeaderboardStatus';
import SubmitStatus from './SubmitStatus';
import ResetLockout from './ResetLockout';


class AdminPanel extends React.Component {
    constructor() {
        super();
        this.state = {
            "isadmin": false
        }
    }

    componentDidMount() {
        this.isAdmin()
    }

    isAdmin() {
        $.ajax({
            url: '/api/isadmin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true : false;
                if (parsed) {
                    this.setState({
                        "isadmin": true
                    });
                }
                else {
                    window.location.replace("/");
                }
            }
        });
    }

    render() {
        return (
            this.state.isadmin && <div>
                <div className="status-container">
                    <LeaderboardStatus />
                    <SubmitStatus />
                    <ResetLockout />
                </div>
            </div>
        );
    }
}
export default AdminPanel;

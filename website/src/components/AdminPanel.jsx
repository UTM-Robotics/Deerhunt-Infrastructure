import React from 'react';
import $ from 'jquery';
import LeaderboardStatus from './LeaderboardStatus';
import SubmitStatus from './SubmitStatus';
import ResetLockout from './ResetLockout';
import ServerReset from './ServerReset';


class AdminPanel extends React.Component {
    constructor() {
        super();
        this.state = {
            "isadmin": false
        }
        this.reload = this.reload.bind(this);
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

    reload(){
        this.setState({});
    }

    render() {
        return (
            this.state.isadmin && <div>
                <div className="status-container">
                    <ServerReset reloadParent={this.reload}/>
                    <LeaderboardStatus />
                    <SubmitStatus />
                    <ResetLockout />
                </div>
            </div>
        );
    }
}
export default AdminPanel;

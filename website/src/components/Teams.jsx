import React from 'react';
import $ from 'jquery';
import InviteCard from "./ReceivedInviteCard";
class Teams extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            team: "",
            newTeamName: "",
            invites: [],
            sentInvites: [],
            canInvite: false,
        };
    }

    componentDidMount() {
        document.addEventListener("keypress", this.handleEnterKeyPress.bind(this));
        this.isLoggedIn();
        this.loadTeam();
        this.loadInvites();
        this.loadIn
    }
    loadInvites() {
        $.ajax({
            url: '/api/userinvites',
            type: 'GET',
            success: (responseData) => {
                var parsed = JSON.parse(responseData);
                if (parsed) {
                    this.setState({
                        invites: parsed
                    });
                }
                else{
                    
                }
            }
        });
    }

    loadInvites() {
        $.ajax({
            url: '/api/isloggedin',
            type: 'GET',
            success: (responseData) => {
                var parsed = JSON.parse(responseData);
                if (parsed) {
                    this.setState({
                        invites: parsed
                    });
                }
                else{
                    
                }
            }
        });
    }

    isLoggedIn() {
        $.ajax({
            url: '/api/isloggedin',
            type: 'GET',
            success: (responseData) => {
                var parsed = responseData == "True" ? true : false;
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
    } 1

    handleEnterKeyPress(e) {
        if (e.charCode == 13 || e.keyCode == 13) {
            this.change();
        }
    }

    handleCreateTeamNameChange(e) {
        this.setState({
            createTeamName: e.target.value
        });
    }

    addError(type: string) {
        $('.error-message').remove();
        $('.success-message').remove();
        var message = "";
        if (type === 'cup') {
            message = "Please enter your current password"
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.register-button').after(errorMessage);
    }

    createTeam() {
        if (this.state.team != "") {
            this.addError('');
            return;
        }

        $.ajax({
            url: '/api/createTeam',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: () => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message">Created Team!</p>';
                $('.register-button').after(successMessage);
                this.state
            },
            error: () => {
                this.addError('');
                return;
            }
        });
    }

    render() {
        if (this.state.team != "") {
            cardsArray = this.state.invites.map(
                invite => (<InviteCard
                    team_name={invite}
                />)
            );

            return (
                <div className="no-team-container">
                    <h1>Join or Create a Team</h1>
                    <form className="team-input">
                        <input placeholder="New Team Name" onChange={this.handleCreateTeamNameChange.bind(this)} />
                        <div className="create-team-button" onClick={this.createTeam.bind(this)}>Create Team</div>
                    </form>
                    <h2>Invites Received</h2>
                    {cardsArray}
                </div>);
        }
        cardsArray = this.state.invites.map(
            invite => (<InviteCard
                team_name={invite}
            />)
        );
        return (
            <div className="on-team-container">
                <h1>Team name: {this.state.team}</h1>
                <form className="invite-input">

                    <input placeholder="User to Invite" onChange={this.handleInviteUserChange.bind(this)} />
                    <div className="send-invite-button" onClick={this.sendInvite.bind(this)}>Send Invite</div>
                </form>
                {cardsArray}
            </div>);
    }
}

export default Teams;

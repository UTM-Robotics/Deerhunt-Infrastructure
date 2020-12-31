import React from 'react';
import $ from 'jquery';
import ReceivedInviteCard from "./ReceivedInviteCard";
import SentInviteCard from "./SentInviteCard";

class Teams extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            team: "",
            team_display: "",
            newTeamName: "",
            usersInvited: [],
            canInvite: false,
            invites: {},
            invitedUser: "",
        };
    }

    componentDidMount() {
        this.isLoggedIn();
        this.reloadAllData();
    }

    reloadAllData() {
        this.loadTeam();
        this.loadReceivedInvites();
    }

    loadTeam() {
        $.ajax({
            url: '/api/getteam',
            type: 'GET',
            dataType: 'JSON',
            success: (responseData) => {
                console.log("Team Received:", responseData);
                if (responseData) {
                    this.setState({
                        team: responseData['name'] || "",
                        team_display: responseData['display_name'] || "",
                        usersInvited: responseData['invites'] || [],
                    });
                }
            }
        });
    }

    loadReceivedInvites() {
        $.ajax({
            url: '/api/userinvites',
            type: 'GET',
            dataType: 'JSON',
            success: (responseData) => {
                console.log(responseData);
                if (responseData) {
                    this.setState({
                        invites: responseData
                    });
                }
                else {

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
    }

    handleCreateTeamNameChange(e) {
        
        console.log("Updating newTeamName: ", e.target.value);
        this.setState({
            newTeamName: e.target.value
        });
    }

    addCreateTeamError(type) {
        $('.error-message').remove();
        $('.success-message').remove();
        var message = "";
        if (type === 'inval') {
            message = "Team name must have between 4 and 16 non-whitespace characters."
        }
        else if (type === 'exists') {
            message = "This team already exists, please choose another name.";
        }
        else if (type === 'fail_accept') {
            message = "Could not accept invite, team is empty or full.(Names cannot be reused)";
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.create-team-button').after(errorMessage);
    }

    createTeam() {
        if (this.state.newTeamName === "" || this.state.newTeamName.length < 4 || this.state.newTeamName.length > 16) {
            this.addCreateTeamError('inval');
            return;
        }
        console.log("Creating Team: ", this.state.newTeamName);
        const requestData = JSON.stringify({
            "team": this.state.newTeamName,
        });
        $.ajax({
            url: '/api/createteam',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: () => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message">Created Team!</p>';
                $('.create-team-button').after(successMessage);
                this.reloadAllData();
            },
            error: () => {
                this.addCreateTeamError('exists');
                return;
            }
        });
    }
    leaveTeam() {
        $.ajax({
            url: '/api/leaveteam',
            type: 'POST',
            contentType: 'application/json',
            success: () => {
                this.reloadAllData();
            }
        });
    }
    addInviteError(type) {
        $('.error-message').remove();
        $('.success-message').remove();
        var message = "";
        if (type === 'no_user') {
            message = "Please enter the email of the user to invite.";
        }
        else if (type === 'invalid_user') {
            message = "Invalid user, please ensure the email is valid and the user is registered.";
        }
        var errorMessage = '<p class="error-message">' + message + '</p>';
        $('.send-invite-button').after(errorMessage);
    }
    handleInviteUserChange(e) {
        this.setState({
            invitedUser: e.target.value
        });
    }

    sendInvite() {
        console.log("Sending invite");
        if (this.state.invitedUser === "") {
            this.addInviteError("no_user");
            return;
        }
        const requestData = JSON.stringify({
            "recipient": this.state.invitedUser,
        });
        console.log(requestData);
        $.ajax({
            url: '/api/sendinvite',
            type: 'POST',
            data: requestData,
            contentType: 'application/json',
            success: () => {
                $('.error-message').remove();
                $('.success-message').remove();
                var successMessage = '<p class="success-message">Invite Sent!</p>';
                $('.send-invite-button').after(successMessage);
                this.reloadAllData();
            },
            error: () => {
                console.log("Error!");
                this.addInviteError('invalid_user');
                return;
            }
        });
    }

    render() {
        console.log("Team: ", this.state.team);
        var invites = this.state.invites;

        if (this.state.team === "") {
            console.log("Invites: ", this.state.invites);
            var inviteCards = [];
            if (invites) {
                inviteCards = Object.entries(this.state.invites).map(
                    ([team_name, display_name]) => (<ReceivedInviteCard
                        team={team_name}
                        reloadCallback={this.reloadAllData}
                        errorCallback={this.addCreateTeamError}
                        team_display={display_name}
                    />)
                );
            }
            return (
                <div className="no-team-container">
                    <h1>Join or Create a Team</h1>
                    <form className="team-input">
                        <input placeholder="New Team Name" onChange={this.handleCreateTeamNameChange.bind(this)} />
                        <div className="create-team-button" onClick={this.createTeam.bind(this)}>Create Team</div>
                    </form>
                    <h2>Invites Received</h2>
                    {inviteCards}
                </div>);
        }
        var cardsArray = this.state.usersInvited.map(
            invitedUser => (<SentInviteCard
                username={invitedUser}
            />)
        );
        if (cardsArray.length == 0) {
            cardsArray = (<p> No users invited!</p>);
        }
        return (
            <div className="on-team-container">
                <h1>Team name: {this.state.team_display}</h1>
                <form className="invite-input">
                    <div className="leave-team-button" onClick={this.leaveTeam.bind(this)}>Leave Team</div>
                    <input placeholder="User to Invite" onChange={this.handleInviteUserChange.bind(this)} />
                    <div className="send-invite-button" onClick={this.sendInvite.bind(this)}>Send Invite</div>
                </form>
                {cardsArray}
            </div>);
    }
}

export default Teams;

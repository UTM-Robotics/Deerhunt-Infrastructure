import React from 'react';
import $ from 'jquery';
import ReceivedInviteCard from "./ReceivedInviteCard";
import SentInviteCard from "./SentInviteCard";
import GameIDCard from "./GameIDCard";
class Teams extends React.Component {

    constructor() {
        super();
        this.state = {
            loggedIn: false,
            team: "",
            teammates: [],
            team_display: "",
            newTeamName: "",
            usersInvited: [],
            canInvite: false,
            invites: {},
            invitedUser: "",
            team_games: [],
        };
        this.reloadAllData = this.reloadAllData.bind(this);
    }

    componentDidMount() {
        this.isLoggedIn();
        this.reloadAllData();
    }

    reloadAllData() {
        this.loadTeam();
        this.loadReceivedInvites();
        this.loadTeamGames();
    }

    loadTeam() {
        $.ajax({
            url: '/api/getteam',
            type: 'GET',
            dataType: 'JSON',
            success: (responseData) => {
                if (responseData) {
                    this.setState({
                        team: responseData['name'] || "",
                        teammates: responseData['users'] || [],
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
                if (responseData) {
                    this.setState({
                        invites: responseData
                    });
                }
            }
        });
    }
    loadTeamGames() {
        $.ajax({
            url: '/api/teamgames',
            type: 'GET',
            dataType: 'JSON',
            success: (responseData) => {
                if (responseData) {
                    this.setState({
                        team_games: responseData
                    });
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
        if (this.state.invitedUser === "") {
            this.addInviteError("no_user");
            return;
        }
        const requestData = JSON.stringify({
            "recipient": this.state.invitedUser,
        });
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
                this.setState({
                    invitedUser:""
                });
                this.reloadAllData();
            },
            error: () => {
                console.log("Error!");
                this.addInviteError('invalid_user');
                return;
            }
        });
    }
    getGameCard(id){
        return (<GameIDCard gameID={id}/>);
    }
    render() {
        var invites = this.state.invites;
        if (this.state.team === "") {
            var inviteCards = [];
            if (invites) {
                inviteCards = Object.entries(invites).map(
                    ([team_name, display_name]) => (<ReceivedInviteCard
                        team={team_name}
                        reloadCallback={this.reloadAllData}
                        errorCallback={this.addCreateTeamError}
                        team_display={display_name}
                    />)
                );
            }
            if (inviteCards.length == 0) {
                inviteCards = (<p> No invites Received!</p>);
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
        var usersArray = this.state.teammates.map(
            teammate_name => (<p>{teammate_name}</p>)
        );
        var cardsArray = this.state.usersInvited.map(
            invitedUser => (<SentInviteCard
                username={invitedUser}
            />)
        );
        if (cardsArray.length == 0) {
            cardsArray = (<p> No users invited!</p>);
        }
        var gameCards = this.state.team_games.map(item=>this.getGameCard(item));

        if (this.state.team_games.length == 0){
            gameCards = (<p> No games logged!</p>);
        }

        console.log(this.state.team_games);
        return (
            <div className="on-team-container">
                <h1>Team name: {this.state.team_display}</h1>
                {usersArray}
                <form className="invite-input">
                    <div className="leave-team-button" onClick={this.leaveTeam.bind(this)}>Leave Team</div>
                    <input placeholder="User to Invite" onChange={this.handleInviteUserChange.bind(this)} />
                    <div className="send-invite-button" onClick={this.sendInvite.bind(this)}>Send Invite</div>
                </form>
                {cardsArray}
                <h3>History (Recent First)</h3>
                {gameCards}
            </div>);
    }
}

export default Teams;

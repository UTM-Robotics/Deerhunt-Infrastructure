import React from 'react';

class GameBoard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            moves: this.props.moves
        };
    }

    componentWillReceiveProps (nextProps) {
        console.log(nextProps.moves);
        this.setState({
            moves: nextProps.moves
        });
    }
    
    render() {
        return (
            <div className="board">
              <h1>Game Board</h1>
              {this.state.moves.map((item, key) => (
                <h1>{item}</h1>
              ))}
            </div>
        );
    }
}

export default GameBoard;

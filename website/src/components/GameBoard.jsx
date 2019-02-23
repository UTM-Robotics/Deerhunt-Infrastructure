import React from 'react';
import melee from './../assets/images/m.gif';
import wall from './../assets/images/x.gif';
import resource from './../assets/images/r.gif';
import worker from './../assets/images/w.gif';
import blank from './../assets/images/empty.gif';

class GameBoard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            move: null,
            moves: null,
            iter: -1
        };

        this.image = {
            "m": melee,
            "r": resource,
            "w": worker,
            "x": wall,
            " ": blank
        }
            
    }
    componentDidUpdate(prevProps) {
        if (this.props.moves != prevProps.moves) {
                this.setState({
                    moves: this.props.moves,
                    iter: 0
                });
        }
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ iter: this.state.iter + 1 }), 1000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    resetIter() {
        this.setState({
            iter: 0
        });
    }

    render() {
        var display = false;
        if (this.state.iter >= 0 && this.state.moves != null && this.state.iter < this.state.moves.length) {
            var move = this.state.moves[this.state.iter];
            display = true;
        }
        return (
            this.props.display && <div className="board">
                <h1>Game Board</h1>
                <h1>{this.state.time}</h1>
                <table>
                <tbody>
                {display && move.map((row,ukey) => (
                    <tr key={ukey}>
                      {row.map((item, key) => (
                          <td key={key}><img className="boardImage" src={this.image[item.toLowerCase()]}/></td>
                        ))}
                    </tr>
                ))}
            </tbody>
                </table>
                <button onClick={this.resetIter.bind(this)}>start again</button>
            </div>
        );
    }
}

export default GameBoard;

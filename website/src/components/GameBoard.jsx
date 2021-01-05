import React from 'react';
import melee from './../assets/images/m.gif';
import melee2 from './../assets/images/M.gif';
import worker from './../assets/images/w.gif';
import worker2 from './../assets/images/W.gif';
import wall from './../assets/images/x.gif';
import resource from './../assets/images/r.gif';
import blank from './../assets/images/empty.gif';
import stun from './../assets/images/s.gif';
class GameBoard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            move: null,
            iter: -1
        };

        this.image = {
            "m": melee,
            "M": melee2,
            "w": worker,
            "W": worker2,
            "R": resource,
            "X": wall,
            " ": blank,
            "S": stun,
        }
            
    }
    componentDidUpdate(prevProps) {
        if (this.props.moves != prevProps.moves) {
                this.setState({
                    iter: 0,
                });
        }
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ iter: this.state.iter + 1 }), 500);
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
        var valid_iter = this.state.iter >= 0 && this.props.moves != "" && this.state.iter < this.props.moves.length;
        var resources_exist = this.props.p1_resources != "" && this.props.p2_resources != "";
        var lengths_math = this.props.moves.length == this.props.p1_resources.length && 
                           this.props.p1_resources.length == this.props.p2_resources.length;

        if (valid_iter && resources_exist && lengths_math) {
            var move = this.props.moves[this.state.iter];
            var p1 = this.props.p1_resources[this.state.iter];
            var p2 = this.props.p2_resources[this.state.iter];
            display = true;
        }
        return (
            this.props.display && <div className="board">
                <h1>Game Board</h1>
                <h3>{this.state.time}</h3>
                <h3>P1(Defender): {p1} - P2(Challenger): {p2}</h3>
                <h3>Turn Count: {this.state.iter + 1}</h3>
                <table>
                <tbody id="table-body">
                {display && move.map((row,ukey) => (
                    <tr key={ukey}>
                      {row.map((item, key) => (
                          <td key={key}><img className="boardImage" src={this.image[item]}/></td>
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

import React, { Component } from "react";
import { Text } from "@chakra-ui/react";

class CountDownTimer extends Component {
  state = {
    days: 0,
    hours: "00",
    minutes: "00",
    timeUp: false,
  };
  componentDidMount() {
    setInterval(() => {
      let eventDate = +new Date(this.props.date);
      let difference = eventDate - +new Date();
      if (difference < 1) {
        this.setState({ timeUp: true });
      } else {
        let days = Math.floor(difference / (1000 * 60 * 60 * 24));
        let hours = Math.floor((difference / (1000 * 60 * 60)) % 24);
        let minutes = Math.floor((difference / (1000 * 60)) % 60);
        this.setState({
          hours: hours > 9 ? hours : `0${hours}`,
          minutes: minutes > 9 ? minutes : `0${minutes}`,
          days,
        });
      }
    }, 1000);
  }
  render() {
    const { days, hours, minutes, timeUp } = this.state;
    const dayString = days > 1 ? "days" : "day";
    return timeUp ? (
      <Text
        textTransform={"uppercase"}
        fontWeight={800}
        fontSize={"sm"}
        letterSpacing={1.1}
        color={"gray.700"}
      >
        Happening now!
      </Text>
    ) : (
      <Text
        textTransform={"uppercase"}
        fontWeight={800}
        fontSize={"sm"}
        letterSpacing={1.1}
        color={"gray.700"}
      >{`${days} ${dayString} ${hours} hours ${minutes}  minutes`}</Text>
    );
  }
}
export default CountDownTimer;

import React, { Component } from 'react';
import {Row, Input, Button, Col, CardPanel} from 'react-materialize';

export default class MirrorTextWithHighlighting extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentText: null
        }
    }

    render() {
        return (
            <h2>{this.state.currentText || this.props.showText}</h2>
        )
    }
}
import React, { Component } from 'react';
import {Row, Input, Button, Col, CardPanel} from 'react-materialize';

export default class MirrorTextWithHighlighting extends Component {
    render() {
        return (
            <h2>{this.props.showText}</h2>
        )
    }
}
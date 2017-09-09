import React, { Component } from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/styles';


export default class MirrorTextWithHighlighting extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentText: null
        }
    }

    render() {
        return (
            <SyntaxHighlighter language="javascript" style={docco}>{this.state.currentText || this.props.showText}</SyntaxHighlighter>
        )
    }
}
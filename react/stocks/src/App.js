import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import {Row, Input, Button} from 'react-materialize';
import MirrorTextWithHighlighting from './components/MirrorTextWithHighlighting'

class App extends Component {

  constructor() {
    super();
    this.state = {
      currentText: "Awaiting text..."
    }
  }

  render() {
    return (
      <div className="App">
        <div className="container">
        <div style = {{"textAlign": "center", "marginTop": "100px"}}>
            <h1>Algorithm</h1>
            <h3>Algorithm trading for the masses.</h3>
            <p>1. Enter a sentence in any natural language, preferably English.</p>
            <p>2. Watch how well your algorithm scores compared to others.</p>
            <p>3. If it performs well, send your algorithm to a partnered online broker in one click for real money trading via "_some_button_name_" button</p>
        </div>
        <div id="entry">
          <Row>
            <Input onChange={this.updateAlgoText.bind(this)} s = {12} placeholder="If MSFT drops $10 from yesterday's close, buy 10 shares of MSFT" style={{"color": "white"}}/>
            <Button waves="light" onClick={this.updateCode}>Translate to Code</Button>
          </Row>
          <MirrorTextWithHighlighting showText = {this.state.currentText}/>
        </div>
    </div>
      </div>
    );
  }

  updateCode() {
    console.log("Code has been updated.");
    // Where the network request will go.
  }

  updateAlgoText(obj, value) {
    console.log("Changing Algo Text");
    this.setState({currentText: value})
  }
}

export default App;

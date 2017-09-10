import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import {Row, Input, Button} from 'react-materialize';
import MirrorTextWithHighlighting from './components/MirrorTextWithHighlighting';
import SyntaxHighlighter from 'react-syntax-highlighter';
import dateFormat from 'dateformat';
import request from 'superagent';

class App extends Component {

  constructor() {
    super();
    this.state = {
      currentText: "Awaiting text...",
      fromDate: "",
      toDate: ""
    }
  }

  render() {
    return (
      <div className="App">
        <div className="container">
            <div className="header" style={{"width": "50%", "text-align": "left", "marginTop": "100px"}}>
                <h1>AlgoTrader</h1>
                <h3>Algorithm trading for the masses.</h3>
            </div>
            <div className="instructions" style={{"width": "40%", "text-align": "left", "marginTop": "100px"}}>
                <p>1. Enter a sentence in any natural language, preferably English.</p>
                <p>2. Watch how well your algorithm scores compared to others.</p>
                <p>3. Make money.</p>
            </div>
        <div id="entry">
          <Row>
            <Input onChange={this.updateAlgoText.bind(this)} s = {12} placeholder="If MSFT drops $10 from yesterday's close, buy 10 shares of MSFT" style={{"textAlign": "center", "color": "#060d14", "fontSize":"18px"}}/>
          </Row>
            <Row>
              <Input s = {6} placeholder="From date" name="on" type="date" onChange={this.setFromDate.bind(this)}/>
              <Input s = {6} placeholder="To date" name="on" type="date" onChange={this.setToDate.bind(this)}/>
            </Row>
        </div>
        <Button waves="light" onClick={this.updateCode.bind(this)}>Translate to Code</Button>
        <MirrorTextWithHighlighting showText = {this.state.currentText}/>
        <Row>
          <img src="portfolio_value.png"/>
        </Row>
       
          <Button> <a href="algorithm.py" download> Download algorithm! </a></Button>
        </div>
      </div>
    );
  }

  setFromDate(e, v) {
    this.setState({fromDate: v});
  }

  setToDate(e, v) {
    this.setState({toDate: v});
  }

  updateCode(e) {
    e.preventDefault();
    e.stopPropagation();
    e.nativeEvent.stopImmediatePropagation();
    const fromDate = this.state.fromDate;
    const toDate = this.state.toDate;
    const fixedFromDate = dateFormat(fromDate, "yyyy/mm/dd").split("/").join("-");
    const fixedToDate = dateFormat(toDate, "yyyy/mm/dd").split("/").join("-");
    console.log("Updating code: " + JSON.stringify(this.state) + " and " + fixedFromDate);
    const objFit = {currentText: this.state.currentText, fromDate: fixedFromDate, fixedToDate: fixedToDate}; // yyyy/mm/dd
    console.log('thing to send: ' + JSON.stringify(objFit));
    fetch("http://a306cf12.ngrok.io/api/text", {
      method: 'POST',
      body: 'text=' + this.state.currentText + '&start=' + fixedFromDate + '&end=' + fixedToDate,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then((response) => {
      console.log(JSON.stringify(response));
    })
  }

  updateAlgoText(obj, value) {
    this.setState({currentText: value});
    // this.updateCode();
  }

  // highlightCurrentText() {
  //   var tokenizeQuery = this.state.currentText.split(" ");
  //   var actionsAndConditions = this.state.actionsAndConditions;
  //   for (var i = 0; i < tokenizeQuery.length; i++) {
  //     var word = tokenizeQuery[i]; // Get a word
  //     for (var j = 0; j < actionsAndConditions.length; j++) {
  //       // Check against all other possibilities.
  //       if (word === actionsAndConditions[j].value) {
  //         if (actionsAndConditions[j].type === 'ticker') tokenizeQuery[i] = '<TICKER>';
  //         if (actionsAndConditions[j].type === 'amount') tokenizeQuery[i] = '<AMOUNT>';
  //         if (actionsAndConditions[j].type === 'amount_unit') tokenizeQuery[i] = '<amount_unit>';
  //         if (actionsAndConditions[j].type === 'position') tokenizeQuery[i] = '<position>';
  //         if (actionsAndConditions[j].type === 'type') tokenizeQuery[i] = '<type>';
  //         if (actionsAndConditions[j].type === 'price') tokenizeQuery[i] = '<price>';
  //         if (actionsAndConditions[j].type === 'threshold') tokenizeQuery[i] = '<threshold>';
  //         if (actionsAndConditions[j].type === 'threshold_type') tokenizeQuery[i] = '<threshold_type>';
  //       }
  //     }
  //   }

  //   return tokenizeQuery.join(" ");
  //   // Split into words.
  //   // var tokenizeInput = this.state.currentText.split(" ");

  //   // // TODO: Make this better.
  //   // for (var i = 0; i < tokenizeInput.length; i++) {
  //   //   // Go through all possible elements.
  //   //   if (tokenizeInput[i].toLowerCase() === 'if') {
  //   //     // tokenizeInput[i] = "LMAO SHIT"
  //   //   }
  //   // }

  //   // return tokenizeInput.join(" ");
  // }
}

export default App;

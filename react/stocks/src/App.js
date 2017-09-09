import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import {Row, Input, Button} from 'react-materialize';
import MirrorTextWithHighlighting from './components/MirrorTextWithHighlighting';
// import request from 'superagent';

class App extends Component {

  constructor() {
    super();
    this.state = {
      currentText: "Awaiting text...",
      actionsAndConditions: [] // array of Strings
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
            <p>3. Get money.</p>
        </div>
        <div id="entry">
          <Row>
            <Input onChange={this.updateAlgoText.bind(this)} s = {12} placeholder="If MSFT drops $10 from yesterday's close, buy 10 shares of MSFT" style={{"color": "white"}}/>
            <Button waves="light" onClick={this.updateCode.bind(this)}>Translate to Code</Button>
          </Row>
          <MirrorTextWithHighlighting showText = {this.state.currentText}/>
        </div>
    </div>
      </div>
    );
  }

  updateCode() {
    console.log("Updating code.");
  }

  // updateCode() {
  //   console.log("Code has been updated.");
  //   // Where the network request will go.
  //   request.get('http://127.0.0.1:5000/api?text=' + this.state.currentText) // if MSFT drops 20% from yesterday, buy 10 shares of AAPL.
  //          .end((err, res) => {
  //            try {
  //              console.log('yeh: ');
  //            if (err) console.log(err);
  //            console.log('response recieved: ' + JSON.stringify(res));
  //            const base = JSON.parse(res.text);
  //            const action = base.action;
  //            const condition = base.condition;
  //           //  console.log("action: " + JSON.stringify(condition));
  //           // Add ticker from ACTION
  //           this.state.actionsAndConditions.push({type: 'ticker', value: action.ticker});
  //           // Add amount from ACTION
  //           this.state.actionsAndConditions.push({type: 'amount', value: action.amount});
  //           // Add amount_unit from ACTION
  //           this.state.actionsAndConditions.push({type: 'amount_unit', value: action.amount_unit});
  //           // Add position from ACTION
  //           this.state.actionsAndConditions.push({type: 'position', value: action.position});

  //           // // Add action from ACTION
  //           // this.state.actionsAndConditions.push({type: 'action', value: action.action});

  //           // Add type from CONDITION
  //           this.state.actionsAndConditions.push({type: 'type', value: condition.type})
  //           // Add ticker from CONDITION
  //           this.state.actionsAndConditions.push({type: 'ticker', value: condition.payload.stocks[0].ticker});
  //           // Add price from CONDITION
  //           this.state.actionsAndConditions.push({type: 'price', value: condition.payload.stocks[1].field})
  //           // Add threshold for CONDITION
  //           this.state.actionsAndConditions.push({type: 'threshold', value: condition.threshold});
  //           // Add threshold_type for CONDITION
  //           this.state.actionsAndConditions.push({type: 'threshold_type', value: condition.threshold_type})

  //           // // Add amount from CONDITION
  //           // this.state.actionsAndConditions.push({type: 'amount', value: condition.amount});
  //           // // Add verb from CONDITION
  //           // this.state.actionsAndConditions.push({type: 'verb', value: condition.verb});
  //           // // Add time from CONDITION
  //           // this.state.actionsAndConditions.push({type: 'time', value: condition.time});
  //           // // Add isPercentage from CONDITION
  //           // this.state.actionsAndConditions.push({type: 'isPercentage', value: condition.isPercentage});

  //           this.setState({currentText: this.highlightCurrentText()});
  //            } catch (e) {}
  //          })
  // }

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

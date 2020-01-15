import React from "react";
import "./App.css";

const BASE_URL = 'http://192.168.1.5:8099';

const Button = props => (
  <div className="Button" onClick={props.onClick}>
    <div className="keyText">{props.text}</div>
    {props.subText && <div>{props.subText}</div>}
  </div>
);


function App() {
  const [value, setValue] = React.useState('');
  const addNumber = num => () => {
    setValue(val => `${val}${num}`);
  };
  const submit = () => {
    fetch(`${BASE_URL}/cmd/${value}`, {method: 'POST'});
    setValue('');
  };
  
  return (
    <div className="App">
      <div className="display">{value}</div>
      <div className="Keypad">
        <Button onClick={addNumber(1)} text={1} />
        <Button onClick={addNumber(2)} text={2} subText="ABC" />
        <Button onClick={addNumber(3)} text={3} subText="DEF" />
        <Button onClick={addNumber(4)} text={4} subText="GHI" />
        <Button onClick={addNumber(5)} text={5} subText="JKL" />
        <Button onClick={addNumber(6)} text={6} subText="MNO" />
        <Button onClick={addNumber(7)} text={7} subText="PQRS" />
        <Button onClick={addNumber(8)} text={8} subText="TUV" />
        <Button onClick={addNumber(9)} text={9} subText="WXYZ" />
        <Button onClick={() => {setValue('')}} text={"C"} />
        <Button onClick={addNumber(0)} text={0} />
        <Button onClick={submit} text={"↵"} />
      </div>
      <pre className="legend">TODO: describe commands</pre>
    </div>
  );
}

export default App;

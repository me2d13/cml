import React from "react";
import { BASE_URL, PAGES } from "../config";

const Button = props => (
  <div className="Button" onClick={props.onClick}>
    <div className="keyText">{props.text}</div>
    {props.subText && <div>{props.subText}</div>}
  </div>
);

const lpad = number => (number <= 999 ? `   ${number}`.slice(-3) : number);

const Commands = ({ commands }) => {
  return (
    <pre className="legend">
      {commands.map(
        ({ number, description }) => `${lpad(number)} .. ${description}\n`
      )}
    </pre>
  );
};

function Keypad({ setPage }) {
  const [value, setValue] = React.useState("");
  const [commands, setCommands] = React.useState([]);
  const addNumber = num => () => {
    setValue(val => `${val}${num}`);
  };
  const submit = () => {
    if (value === "73887") {
      //SETUP
      setPage(PAGES.setup);
    } else {
      fetch(`${BASE_URL}/commands/${value}`, { method: "POST" });
      setValue("");
    }
  };

  React.useEffect(() => {
    fetch(`${BASE_URL}/commands`, { method: "GET" })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
      })
      .then(fetched => setCommands(fetched));
  }, []);

  return (
    <div>
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
        <Button
          onClick={() => {
            setValue("");
          }}
          text={"C"}
        />
        <Button onClick={addNumber(0)} text={0} />
        <Button onClick={submit} text={"↵"} />
      </div>
      {commands && <Commands commands={commands} />}
    </div>
  );
}

export default Keypad;

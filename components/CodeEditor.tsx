import React, { Component } from "react";
import { Controlled as CodeMirror } from "react-codemirror2";

let modeLoaded = false;
if (typeof window !== "undefined" && typeof window.navigator !== "undefined") {
  require("codemirror/mode/python/python");
  modeLoaded = true;
}

const CodeEditor = (props) => {
  const options = {
    theme: "duotone-light",
    lineNumbers: true,
  };
  if (modeLoaded) {
    options["mode"] = "python";
  }

  return (
    <div>
      <CodeMirror {...props} options={options} />
    </div>
  );
};

export default CodeEditor;

import React from "react";
import { Controlled as CodeMirror } from "react-codemirror2";

let modeLoaded = false;
if (typeof window !== "undefined" && typeof window.navigator !== "undefined") {
  require("codemirror/mode/python/python");
  modeLoaded = true;
}

const CodeEditor = (props) => {
  const options = {
    tabSize: 2,
    theme: "elegant",
    lineNumbers: true,
  };
  if (modeLoaded) {
    options["mode"] = "python";
  }

  return (
    <div style={{ marginBottom: "2em" }}>
      <CodeMirror {...props} options={options} />
    </div>
  );
};

export default CodeEditor;

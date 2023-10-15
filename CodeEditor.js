// src/components/CodeEditor.js
import React, { useState } from 'react';

const CodeEditor = ({ onCodeChange }) => {
  const [code, setCode] = useState('');

  const handleChange = (event) => {
    const newCode = event.target.value;
    setCode(newCode);
    onCodeChange(newCode);
  };

  return (
    <textarea value={code} onChange={handleChange} />
  );
};

export default CodeEditor;

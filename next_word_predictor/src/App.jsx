import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [predictionMode, setPredictionMode] = useState('next');
  const textareaRef = useRef(null);

  const updatePredictions = async (currentText) => {
    if (currentText.trim().length === 0) {
      setPredictions([]);
      return;
    }

    const isNextWordMode = currentText.endsWith(' ');
    const mode = isNextWordMode ? 'next' : 'current';
    setPredictionMode(mode); 

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // 2. Then, it sends that mode in the JSON body to the backend.
        body: JSON.stringify({
          context: currentText.trim(),
          mode: mode, // <-- The mode is sent right here
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setPredictions(data.predictions || []);

    } catch (error) {
      console.error("Failed to fetch predictions:", error);
      setPredictions([]);
    }
  };

  const handleInputChange = (event) => {
    const newText = event.target.value;
    setInputText(newText);
    updatePredictions(newText);
  };

  const handlePredictionClick = (word) => {
    let newText;
    if (predictionMode === 'next') {
      newText = inputText + word + ' ';
    } else {
      const words = inputText.trim().split(' ');
      words[words.length - 1] = word;
      newText = words.join(' ') + ' ';
    }
    
    setInputText(newText);
    updatePredictions(newText); 
    textareaRef.current.focus();
  };

  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      const maxHeight = 250; 
      textarea.style.height = 'auto';
      const scrollHeight = textarea.scrollHeight;
      if (scrollHeight > maxHeight) {
        textarea.style.height = `${maxHeight}px`;
        textarea.style.overflowY = 'auto';
      } else {
        textarea.style.height = `${scrollHeight}px`;
        textarea.style.overflowY = 'hidden';
      }
    }
  }, [inputText]);

  return (
    <div className="container">
      <h1 className="title">Next word prediction</h1>
      <textarea
        ref={textareaRef}
        className="chatbox"
        value={inputText}
        onChange={handleInputChange}
        placeholder="Start typing here..."
        autoFocus
        rows="1"
      />

      {predictions.length > 0 && (
        <div className="predictions-container">
          {predictions.map((word, index) => (
            <button
              key={index}
              className="prediction-button"
              onClick={() => handlePredictionClick(word)}
            >
              {word}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
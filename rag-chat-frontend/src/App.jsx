import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [model, setModel] = useState('mistral');
  const [history, setHistory] = useState([]);
  const [answer, setAnswer] = useState('');

  const handleAsk = async () => {
    if (!question.trim()) return;

    try {
      const res = await axios.post('http://localhost:8000/ask', {
        question,
        model,
        history, // optional: backend can use for follow-ups
      });

      const newEntry = {
        question,
        answer: res.data.answer,
      };

      setHistory(prev => [...prev, newEntry]);
      setAnswer(res.data.answer);
      setQuestion('');
    } catch (err) {
      console.error('Error fetching answer:', err);
    }
  };

  const handleNewChat = () => {
    setHistory([]);
    setAnswer('');
    setQuestion('');
  };

  return (
    <div className="container">
      {/* Left Sidebar */}
      <div className="sidebar">
        <h2>💬 Chat History</h2>
        <button onClick={handleNewChat}>🆕 New Chat</button>
        <div className="chat-history">
          {history.map((entry, index) => (
            <div key={index} className="chat-pair">
              <div className="chat-question">🧑‍💻 {entry.question}</div>
              <div className="chat-answer">🤖 {entry.answer}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Section */}
      <div className="chat-window">
        <h1>🧠 Local AI Chatbot</h1>

        <textarea
          value={question}
          onChange={e => setQuestion(e.target.value)}
          rows={4}
          placeholder="Ask your question..."
        />

        <div>
          <label>Model:</label>
          <select value={model} onChange={e => setModel(e.target.value)}>
            <option value="mistral">mistral</option>
            <option value="llama3">llama3</option>
            <option value="gemma">gemma</option>
          </select>
        </div>

        <button onClick={handleAsk}>Ask</button>

        {answer && (
          <div className="live-answer">
            <h3>Answer:</h3>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

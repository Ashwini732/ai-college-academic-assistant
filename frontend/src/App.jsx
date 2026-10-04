import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    const currentQuestion = question.trim();

    const history = messages.map((message) => ({
      role: message.type === "user" ? "user" : "assistant",
      text: message.text,
    }));

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: currentQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
          history,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          text: data.answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          text: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      <div className="chat-container">

        <header className="header">
          <div>
            <h1>🎓 College Academic Assistant</h1>
            <p>
              Ask about academics, exams, internships and study plans.
            </p>
          </div>

          {messages.length > 0 && (
            <button className="clear-btn" onClick={clearChat}>
              Clear
            </button>
          )}
        </header>

        <main className="chat-area">
          {messages.length === 0 && (
            <div className="welcome">
              <h2>How can I help you?</h2>

              <div className="suggestions">
                <button
                  onClick={() =>
                    setQuestion("What is the minimum attendance requirement?")
                  }
                >
                  📚 Academic information
                </button>

                <button
                  onClick={() =>
                    setQuestion("Summarize the internship guidelines")
                  }
                >
                  📄 Summarize documents
                </button>

                <button
                  onClick={() =>
                    setQuestion(
                      "Make a study plan for Algorithms and Databases, 3 hours a day, exam on 2026-11-20"
                    )
                  }
                >
                  🗓️ Create study plan
                </button>

                <button
                  onClick={() => setQuestion("What is 25 * 4 + 10?")}
                >
                  🧮 Calculate
                </button>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.type}`}
            >
              <div className="avatar">
                {message.type === "user" ? "You" : "AI"}
              </div>

              <div className="message">
                {message.type === "assistant" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.text}
                  </ReactMarkdown>
                ) : (
                  <p>{message.text}</p>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar">AI</div>

              <div className="message typing">
                Thinking<span>.</span><span>.</span><span>.</span>
              </div>
            </div>
          )}
        </main>

        <div className="input-container">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask your academic question..."
            rows="2"
          />

          <button
            className="send-btn"
            onClick={askQuestion}
            disabled={loading || !question.trim()}
          >
            {loading ? "..." : "Send"}
          </button>
        </div>

        <p className="footer-text">
          AI College Academic Assistant
        </p>

      </div>
    </div>
  );
}

export default App;
import React, { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [similarArticles, setSimilarArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const SUMMARIZE_URL = "https://ipw7srvzsm.us-east-2.awsapprunner.com/summarize";
  const SIMILAR_URL = "https://ipw7srvzsm.us-east-2.awsapprunner.com/compare"; // 🔁 CHANGE THIS

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSummary("");
    setSimilarArticles([]);

    try {
      const [similarRes] = await Promise.all([
        fetch(SIMILAR_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        }),
      ]);

      if (!similarRes.ok) throw new Error("One or more requests failed");

      const similarData = await similarRes.json();

      setSimilarArticles(similarData);
    } catch (err) {
      setError("Failed to fetch similar articles.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1 className="title">News Summarizer</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste your article here..."
          rows={10}
          cols={80}
        />
        <br />
        <button type="submit" disabled={loading || !text.trim()}>
          {loading ? "Loading..." : "Summarize"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {similarArticles.length > 0 && (
        <div className="similar-box">
          <h2>Top Similar Articles</h2>
          <ul>
            {similarArticles.map((article, idx) => (
              <li key={idx}>
                <a href={article.url} target="_blank" rel="noopener noreferrer">
                  {article.title}
                </a>
                {article.score && (
                  <span
                    style={{
                      marginLeft: "1em",
                      fontSize: "0.9em",
                      color: "#555",
                    }}
                  >
                    (Similarity: {article.score.toFixed(2)})
                  </span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
export default App;

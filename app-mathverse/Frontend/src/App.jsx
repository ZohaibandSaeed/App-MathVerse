import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Sparkles, Send, Activity, Volume2, Copy, Download, Moon, Sun, Layers, LayoutTemplate, Clock, Code2, FileText, Code } from 'lucide-react';
import Playground from './components/Playground';

export default function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [activeMode, setActiveMode] = useState("mathverse");

  const endOfResultRef = useRef(null);

  // Initialize Theme
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  // Symbol Toolbar Data
  const mathSymbols = [
    { label: "x²", value: "^2" },
    { label: "xⁿ", value: "^" },
    { label: "√x", value: "sqrt(" },
    { label: "∫", value: "integrate " },
    { label: "d/dx", value: "d/dx " },
    { label: "lim", value: "limit " },
    { label: "Σ", value: "sum " },
    { label: "π", value: "pi" },
    { label: "θ", value: "theta" },
    { label: "sin", value: "sin(" },
    { label: "cos", value: "cos(" },
    { label: "tan", value: "tan(" },
    { label: "∞", value: "infinity" },
    { label: "±", value: "+-" },
    { label: "≤", value: "<=" },
    { label: "≥", value: ">=" },
  ];

  const handleSymbolClick = (val) => {
    setQuery(prev => prev + val);
  };

  const handleSolve = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      // Use environment variable for backend URL if available, else fallback to localhost
      const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      
      const response = await axios.post(`${API_BASE_URL}/api/v1/solve`, {
        problem: query
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (result || error) {
      endOfResultRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [result, error]);

  // Utility Actions
  const handleVoice = () => {
    if (!result || !result.solution_text) return;
    const utterance = new SpeechSynthesisUtterance(result.solution_text);
    window.speechSynthesis.speak(utterance);
  };

  const handleCopy = () => {
    if (result && result.solution_text) {
      navigator.clipboard.writeText(result.solution_text);
    }
  };

  const handleDownloadPNG = () => {
    if (!result || !result.image_base64) return;
    const link = document.createElement('a');
    link.href = result.image_base64;
    link.download = 'mathly-render.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full flex flex-col items-center">

      {/* Header */}
      <header className="w-full max-w-6xl flex items-center justify-between py-6 px-4 md:px-8">
        <div className="flex items-center gap-3">
          <div className="bg-primary p-2 rounded-xl text-white">
            <Sparkles className="w-5 h-5" />
          </div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold font-sans">Mathly AI</h1>
            <span className="text-[10px] font-bold bg-primary/20 text-primary px-2 py-1 rounded-full uppercase tracking-widest border border-primary/30">
              V2.4 RAG
            </span>
          </div>
        </div>

        <div className="hidden md:flex items-center bg-gray-100 dark:bg-gray-800 p-1 rounded-full border border-gray-200 dark:border-gray-700">
          <button 
            onClick={() => setActiveMode("mathverse")}
            className={`flex items-center gap-2 px-6 py-2 rounded-full transition-all text-sm font-bold ${
              activeMode === "mathverse" 
                ? "bg-white dark:bg-gray-700 text-primary shadow-sm" 
                : "text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
            }`}
          >
            <Sparkles className="w-4 h-4" /> MathVerse
          </button>
          <button 
            onClick={() => setActiveMode("playground")}
            className={`flex items-center gap-2 px-6 py-2 rounded-full transition-all text-sm font-bold ${
              activeMode === "playground" 
                ? "bg-white dark:bg-gray-700 text-primary shadow-sm" 
                : "text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
            }`}
          >
            <Code className="w-4 h-4" /> Code
          </button>
        </div>

        <div className="flex items-center">
          <button onClick={toggleTheme} className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
            {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="w-full max-w-5xl flex-grow flex flex-col px-4 md:px-8 pt-10">
        
        {activeMode === "playground" ? (
          <Playground isDarkMode={isDarkMode} />
        ) : (
          <div className="flex flex-col items-center w-full">
            {/* Input Section */}
            <div className="w-full max-w-4xl flex flex-col gap-3">
              <form onSubmit={handleSolve} className="w-full relative group">
                <div className="panel p-2 flex items-center rounded-2xl relative z-10 focus-within:ring-2 focus-within:ring-primary/50 transition-all">
                  <input
                    type="text"
                    value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="solve the question: 3(x-2)+5=2x+9"
                className="flex-grow bg-transparent border-none outline-none px-4 py-3 text-lg font-mono placeholder-gray-400 dark:placeholder-gray-600"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="bg-primary hover:bg-blue-500 text-white p-3 rounded-xl transition-colors disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-primary/25"
              >
                {loading ? <Activity className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
              </button>
            </div>
          </form>

          {/* Symbol Toolbar */}
          <div className="panel px-4 py-2 rounded-xl flex items-center gap-2 overflow-x-auto whitespace-nowrap scrollbar-hide">
            <span className="text-xs font-bold text-primary uppercase tracking-wider flex items-center gap-1 mr-2">
              <Code2 className="w-4 h-4" /> Symbols:
            </span>
            {mathSymbols.map((sym, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSymbolClick(sym.value)}
                className="px-3 py-1 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 border border-gray-300 dark:border-slate-700 rounded-md text-sm font-mono font-medium transition-colors text-black dark:text-white shadow-sm active:scale-95"
              >
                {sym.label}
              </button>
            ))}
          </div>
        </div>

        {/* Error State */}
        {error && (
          <div className="w-full max-w-4xl panel p-6 border-red-500/50 mt-12 bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400">
            <h3 className="font-bold mb-2">Error Encountered</h3>
            <p className="text-sm font-mono">{error}</p>
          </div>
        )}

        {/* Results Area */}
        {result && !loading && (
          <div className="w-full grid grid-cols-1 lg:grid-cols-12 gap-6 mt-12 mb-24">

            {/* Left Column: Mathematical Steps */}
            <div className="lg:col-span-5 flex flex-col gap-4">
              <div className="panel p-5 h-full flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200 dark:border-gray-800">
                  <div className="flex items-center gap-2">
                    <div className="bg-gray-200 dark:bg-gray-800 p-1.5 rounded-lg">
                      <FileText className="text-primary w-5 h-5" />
                    </div>
                    <h3 className="font-semibold text-sm">Mathematical Steps</h3>
                  </div>
                  <div className="flex items-center gap-2">
                    <button onClick={handleVoice} className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-primary/20 hover:text-primary transition-colors text-gray-500 dark:text-gray-400">
                      <Volume2 className="w-4 h-4" />
                    </button>
                    <button onClick={handleCopy} className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-primary/20 hover:text-primary transition-colors text-gray-500 dark:text-gray-400">
                      <Copy className="w-4 h-4" />
                    </button>
                    <button onClick={handleDownloadPNG} className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-primary/20 hover:text-primary transition-colors text-gray-500 dark:text-gray-400">
                      <Download className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Steps Content */}
                <div className="flex-grow overflow-y-auto pr-2" style={{ maxHeight: '600px' }}>
                  <h4 className="text-primary font-bold text-lg mb-4 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary"></div>
                    Step-by-Step Breakdown
                  </h4>
                  <div className="text-sm leading-loose font-serif">
                    {result.solution_text.split('\n').map((line, idx) => {
                      if (!line.trim()) return <br key={idx} />;
                      // If it looks like an equation (contains '=' or numbers and is short), wrap in a panel
                      if (line.includes('=') && line.length < 50) {
                        return (
                          <div key={idx} className="my-3 py-3 px-4 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-black font-mono text-center shadow-sm">
                            {line}
                          </div>
                        );
                      }
                      return <p key={idx} className="mb-2">{line}</p>;
                    })}
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column: Visual Result */}
            <div className="lg:col-span-7 flex flex-col gap-4">
              <div className="panel p-5 h-full flex flex-col">
                {/* Header */}
                <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-200 dark:border-gray-800">
                  <div className="flex items-center gap-3">
                    <div className="bg-primary/10 p-2 rounded-lg">
                      <Activity className="text-primary w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-sm">Mathly Visual Engine</h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5 max-w-[200px] truncate">{query}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold bg-primary text-white px-2 py-1 rounded-md uppercase tracking-wider">
                      Interactive
                    </span>
                    <span className="text-[10px] font-bold bg-gray-200 dark:bg-gray-800 text-gray-600 dark:text-gray-300 px-2 py-1 rounded-md uppercase tracking-wider">
                      PNG Render
                    </span>
                    <button className="p-2 rounded-lg bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors text-gray-500 dark:text-gray-400">
                      <Layers className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Image Content */}
                <div className="flex-grow flex items-center justify-center bg-gray-100 dark:bg-black/50 rounded-xl border border-gray-200 dark:border-gray-800 p-2 overflow-hidden relative min-h-[400px]">
                  <img
                    src={result.image_base64}
                    alt="Mathly Rendered Output"
                    className="max-w-full h-auto rounded-lg shadow-2xl relative z-10"
                  />
                </div>

                {/* Footer */}
                <div className="mt-4 flex items-center justify-between text-xs text-gray-400 font-mono">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    Engine: High-Precision Coordinate Mesh
                  </div>
                  <div>Points evaluated: 1500+</div>
                </div>
              </div>
            </div>

          </div>
        )}
      </div>
    )}
        <div ref={endOfResultRef} className="h-10" />
      </main>
    </div>
  );
}

import React, { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import { Play, Loader2, AlertCircle } from 'lucide-react';
import axios from 'axios';

const DEFAULT_CODE = `from mathly.core.board import MathBoard
from mathly.algebra.grid2d import Grid2D

board = MathBoard("Mathly Playground")
grid = Grid2D(x_range=(-5, 5), y_range=(-5, 5))

# Draw a function
grid.plot_function("x**2", color="blue", label="f(x) = x^2")

board.add_visual(grid)
board.render("output.png")
`;

export default function Playground({ isDarkMode }) {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [loading, setLoading] = useState(false);
  const [resultImage, setResultImage] = useState(null);
  const [error, setError] = useState(null);

  const handleRunCode = async () => {
    setLoading(true);
    setError(null);
    setResultImage(null);

    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      const response = await axios.post(`${API_BASE_URL}/api/v1/run-playground`, {
        code: code
      });
      setResultImage(response.data.image_base64);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred during execution.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-col md:flex-row gap-6 h-[75vh]">
      {/* Editor Pane */}
      <div className="flex-1 flex flex-col panel rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800">
        <div className="flex items-center justify-between px-4 py-3 bg-gray-50 dark:bg-slate-800/50 border-b border-gray-200 dark:border-gray-800">
          <span className="text-sm font-bold font-mono text-gray-600 dark:text-gray-300">main.py</span>
          <button
            onClick={handleRunCode}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-1.5 bg-primary hover:bg-blue-500 text-white text-sm font-bold rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            Run Code
          </button>
        </div>
        <div className="flex-1">
          <Editor
            height="100%"
            language="python"
            theme={isDarkMode ? "vs-dark" : "light"}
            value={code}
            onChange={(val) => setCode(val || "")}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              padding: { top: 16 },
              scrollBeyondLastLine: false,
            }}
          />
        </div>
      </div>

      {/* Preview Pane */}
      <div className="flex-1 flex flex-col panel rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800 relative bg-white dark:bg-slate-900">
        <div className="px-4 py-3 bg-gray-50 dark:bg-slate-800/50 border-b border-gray-200 dark:border-gray-800">
          <span className="text-sm font-bold text-gray-600 dark:text-gray-300">Live Preview</span>
        </div>
        
        <div className="flex-1 flex items-center justify-center p-6 overflow-auto">
          {loading ? (
            <div className="flex flex-col items-center gap-4 text-gray-400">
              <Loader2 className="w-8 h-8 animate-spin text-primary" />
              <p className="font-mono text-sm animate-pulse">Compiling Mathly...</p>
            </div>
          ) : error ? (
            <div className="w-full h-full p-4 bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 font-mono text-sm overflow-auto rounded-xl border border-red-200 dark:border-red-900/50">
              <div className="flex items-center gap-2 mb-2 font-bold text-red-700 dark:text-red-500">
                <AlertCircle className="w-5 h-5" /> Execution Error
              </div>
              <pre className="whitespace-pre-wrap">{error}</pre>
            </div>
          ) : resultImage ? (
            <img src={resultImage} alt="Mathly Output" className="max-w-full rounded-xl shadow-lg border border-gray-200 dark:border-gray-800" />
          ) : (
            <div className="text-center text-gray-400 font-mono text-sm">
              <p>Hit "Run Code" to render your math visual.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

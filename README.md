<div align="center">
  <h1>🌌 MathVerse</h1>
  <p><b>The Ultimate AI-Powered Math Ecosystem</b></p>
  <p><i>A unified platform bridging the gap between LLMs, Mathematics, and Interactive Visualizations.</i></p>
  
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
  [![Vite](https://img.shields.io/badge/Vite-5+-646CFF.svg)](https://vitejs.dev/)
</div>

<br>

## 🚀 Overview

Welcome to **MathVerse**! This is a complete, end-to-end ecosystem designed to solve complex mathematical problems using Artificial Intelligence and render them beautifully. 

This repository is a **Monorepo** that contains two major components:

1. **`mathly` (The Core Library):** A lightweight, LLM-friendly Python library designed specifically for AI models to easily generate complex Calculus and Algebra graphs without the boilerplate code of traditional libraries.
2. **`app-mathverse` (The Web Platform):** A stunning full-stack web application featuring an interactive Coding Playground where users and AI can write `mathly` code and see live, real-time visual outputs.

---

## 🌍 Live Demo & Installation

**Test the Platform Live:**  
You can test the MathVerse web application and playground right now at:  
👉 **[https://appmathverse.netlify.app](https://appmathverse.netlify.app)**

**Install the Library:**  
The `mathly` AI library is published on PyPI. You can install it in your own Python projects via:
```bash
pip install mathly
```

---

## 📂 Repository Structure

```text
MathVerse/
├── mathly/                 # 📦 The Core Python Library (PyPI Package)
│   ├── src/                # Library Source Code (Algebra & Calculus components)
│   ├── tests/              # Unit tests
│   └── pyproject.toml      # Package Configuration
│
└── app-mathverse/          # 🌐 The Web Application (Platform)
    ├── Frontend/           # React + Vite UI (The Playground)
    └── Backend/            # FastAPI Server (AI Processing & Code Execution)
```

---

## 🌟 1. Mathly (The Library)

`To explore further mathly please visit: https://github.com/ZohaibandSaeed/MathVerse.git`

`mathly` is built to be the easiest tool for Large Language Models (LLMs) to use when they want to draw math. Instead of struggling with complex Matplotlib configurations, AI can use `mathly`'s simple classes like `CalculusGraph`, `Grid2D`, and `NumberLine` to generate high-precision mathematical visualisations.

### Key Features:
- **LLM-Optimized:** Intuitive APIs that prevent AI hallucinations.
- **Algebra & Calculus:** Built-in tools to plot vectors, intersections, polynomials, tangent lines, and area under the curve (Riemann Sums).
- **String Evaluation:** Pass mathematical equations as simple strings (e.g., `"x**2 + 2*x"`) and let `mathly` do the heavy lifting!

> 📖 *Check out the [mathly folder](./mathly) for its detailed README and prompt injection guides.*

---

## 🌐 2. App-MathVerse (The Platform)

The web platform is the face of the ecosystem. It provides a state-of-the-art **Playground** where users can experience the power of `mathly` directly in their browser.

### The Stack:
- **Frontend:** React, Vite, TailwindCSS, Monaco Editor (for a VS Code-like coding experience).
- **Backend:** Python FastAPI, LangChain, Groq/Gemini APIs for lightning-fast AI inference.

### Key Features:
- **Live Code Execution:** Write `mathly` Python code in the browser and instantly see the rendered graph in the preview panel.
- **AI Math Solver:** Scan or type mathematical problems and get step-by-step solutions with dynamic visual graphs.
- **Split-Pane Editor:** A seamless UI experience for developers and students alike.

---

## 🛠️ Local Development & Setup

### Running the Backend (FastAPI)
```bash
cd app-mathverse/Backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Running the Frontend (React/Vite)
```bash
cd app-mathverse/Frontend
npm install
npm run dev
```

*(Make sure to create a `.env` file in the Backend folder with your `GROQ_API_KEY` or `GEMINI_API_KEY`)*

---

## 🚀 Deployment

- **Frontend:** Ready to be deployed on **Netlify** or **Vercel** using `app-mathverse/Frontend` as the root directory.
- **Backend:** Ready to be deployed on **Render** or **Vercel** (includes `vercel.json`) using `app-mathverse/Backend` as the root directory.
- **Library:** Automated CI/CD pipeline using **GitHub Actions**. Pushing a new GitHub Release automatically publishes `mathly` to PyPI.

---

<div align="center">
  <i>Built with ❤️ for the Hackathon</i>
</div>

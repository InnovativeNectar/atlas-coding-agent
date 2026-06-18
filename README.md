# 🌌 Atlas Coding Agent

**Atlas** is a sophisticated, AI-powered pair programmer and coding agent designed specifically for **Termux** (Android) and **Ubuntu** (Linux) environments. Built with a modular "Harness & Subagent" architecture, Atlas isn't just a tool—it's a collaborator with a "Soul" and a "Heartbeat."

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/InnovativeNectar/atlas-coding-agent)
[![License](https://img.shields.io/badge/license-Apache--2.0-green.svg)](LICENSE)

---

## ✨ Core Features

### 🧠 The "Soul" (Identity)
Atlas uses a specialized Identity layer to manage different personas. Whether it's the **Orchestrator** planning the mission or the **Coder** performing surgical edits, each subagent has a distinct persona and behavioral system prompt.

### 💓 The "Heartbeat" (Vitality)
Atlas features a persistent telemetry system that monitors its own "vital signs."
- **Dashboard:** Real-time uptime, task completion rates, and LLM latency.
- **Logs:** Persistent heartbeat records that track the agent's life across sessions.

### 🛠 Modular Harness & Subagents
- **Agent Harness:** A standardized execution environment that provides secure access to FileSystem, Shell, and Git tools.
- **Specialized Subagents:**
  - **Atlas Prime (Orchestrator):** Mission coordination and strategic planning.
  - **Atlas Deep (Investigator):** Codebase mapping and dependency research.
  - **Atlas Craft (Coder):** Surgical, test-driven implementation.

### 🎨 World-Class UI/UX
- **Rich Dashboard:** A beautiful terminal interface using `rich.layout`.
- **Interactive Prompts:** High-fidelity input handling via `questionary`.
- **Real-time Status:** Distinct spinners and progress indicators for every subagent role.

---

## 🚀 One-Click Installation

Atlas is optimized for mobile (Termux) and desktop (Ubuntu) environments.

### 1. Clone & Setup
```bash
git clone https://github.com/InnovativeNectar/atlas-coding-agent.git
cd atlas-coding-agent
chmod +x setup.sh
./setup.sh
```

### 2. Configure API Key
Atlas is powered by **Gemini 2.0 Flash**. Add your API key to your environment:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 🛠 Usage

### 👋 Verify Installation
```bash
atlas hello
```

### 💬 Start Coding
```bash
atlas chat
```

### 📊 Check Vital Signs
```bash
atlas status
```

### 🔐 Secure Login
```bash
atlas login
```

---

## 🏗 Architecture

```text
atlas-coding-agent/
├── atlas/
│   ├── core/           # Harness, Heartbeat, Identity (The Core)
│   ├── agents/         # Specialized Subagents (The Brain)
│   ├── auth/           # Secure JWT & Identity management
│   ├── engine/         # Gemini 2.0 Flash Integration
│   └── tools/          # Atomic File & Shell tools
├── setup.sh            # One-click environment installer
└── main.py             # World-class CLI entrypoint
```

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit Pull Requests or open Issues for new features, bug fixes, or UI/UX enhancements.

---

## 📄 License

This project is licensed under the Apache-2.0 License - see the [LICENSE](LICENSE) file for details.

---
*Built with heart and soul by Innovative Nectar.*

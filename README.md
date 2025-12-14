<div align="center">

# 📦 EPI
### Evidence Packaged Infrastructure

> **"Don't just log it. Sign it."**
> 
> *The Standard for Verifiable AI Evidence.*

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-ffe500.svg?style=flat-square&logo=python&logoColor=black)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-Production_Ready-success.svg?style=flat-square)](https://pypi.org/project/epi-recorder/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mohdibrahimaiml/EPI-V2.1.0/blob/main/colab_demo.ipynb)

<br/>

[🎥 **Watch the Demo**](https://colab.research.google.com/github/mohdibrahimaiml/EPI-V2.1.0/blob/main/colab_demo.ipynb) &nbsp;•&nbsp; [📚 **Read the Docs**](docs/CLI.md) &nbsp;•&nbsp; [🐛 **Report Bug**](https://github.com/mohdibrahimaiml/EPI-V2.1.0/issues)

</div>

---

## ⚡ The Problem: AI is a Black Box

When an AI Agent takes an action (spends money, signs a contract, or diagnoses a patient), **logs are not enough**.
Logs can be faked. Screenshots can be edited.

**If you can't prove it happened, it didn't happen.**

## 💎 The Solution: The "PDF" for Execution

**EPI** is a new file format (`.epi`) that acts as a **cryptographically signed receipt** for any AI workflow.
It captures the code, the data, the API calls, and the environment into a single, sealed evidence package.

| Feature | 📄 PDF (Document Standard) | 📦 EPI (Execution Standard) |
| :--- | :--- | :--- |
| **Purpose** | Visual Consistency | Computational Integrity |
| **Captures** | Text, Fonts, Images | Code, API Calls, OS State |
| **Trust** | "Looks Correct" | **"Cryptographically Proven"** |
| **Security** | ⚠️ Can run JS (Unsafe) | ✅ **Static HTML (Safe)** |
| **Analogy** | A digital photo | A flight recorder |

---

## 🚀 Quick Start (Zero Config)

### 1️⃣ Install
```bash
pip install epi-recorder
```

### 2️⃣ Record
Wrap any script. EPI intercepts shell commands, file I/O, and LLM calls (OpenAI, Anthropic, Ollama).
```bash
epi record --out evidence.epi -- python agent.py
```
*> Creates `evidence.epi` (a ZIP containing the code, logs, and signatures)*

### 3️⃣ View
Open the evidence in your browser. **Zero-install, works offline.**
```bash
epi view evidence.epi
```

---

## ⚙️ The Architecture of Trust

EPI unifies three powerful components into one standard format:

### 📹 1. The Recorder
A system-level flight recorder that captures truth at the source.
*   **Intercepts**: Shell commands, Stdout/Stderr, Exit codes.
*   **Caches**: Every LLM request is hashed and cached for deterministic replay.
*   **Redacts**: Automatically scrubs API keys (`sk-...`) before saving.

### 📦 2. The Container
A portable, ZIP-based "Truth File" that runs everywhere.
```text
evidence.epi
├── manifest.json        # 📝 Metadata + Ed25519 Signature
├── steps.jsonl          # ⏱️ Micro-timeline of every event
├── artifacts/           # 💾 Content-addressed files (SHA-256)
├── cache/               # 🔄 Replay cache for deterministic runs
└── viewer/              # 🖥️ Embedded HTML5 Viewer (Offline)
```

### 🛡️ 3. The Verifier
Ensures the evidence is authentic and untampered.
*   ✅ **Integrity**: Verifies SHA-256 hashes of the timeline.
*   ✅ **Authenticity**: Validates the **Ed25519** signature against the author's key.

---

## 🔐 Security & Privacy

*   **Safe by Design**: The viewer is **100% static HTML/JSON**. It never executes the recorded code, making it safe to open files from untrusted sources.
*   **Privacy First**: API keys are automatically detected and **redacted** from logs.
*   **No Lock-In**: The format is open (ZIP + JSON). You can unzip it and audit the raw data anytime.

---

## 📚 Documentation

*   **[CLI Reference](docs/CLI.md)**: Master the `init`, `run`, `doctor`, and `keys` commands.
*   **[File Specification](docs/EPI-SPEC.md)**: Deep dive into the V2.1.0 format mechanics.

---

## 📄 License

**Apache 2.0** — Open for commercial and private use.

<div align="center">
  <br/>
  <b>Built for the future of the AI Economy.</b><br>
  <i>Turning opaque runs into verifiable proofs.</i>
</div>

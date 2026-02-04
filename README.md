<p align="center">
  <img src="https://raw.githubusercontent.com/mohdibrahimaiml/epi-recorder/main/docs/assets/logo.png" alt="EPI Logo" width="200"/>
  <br>
  <h1 align="center">EPI Recorder</h1>
  <p align="center"><strong>The PDF for AI Evidence</strong></p>
</p>

[![Release](https://img.shields.io/github/v/release/mohdibrahimaiml/epi-recorder?label=release&style=flat-square&color=00d4ff)](https://github.com/mohdibrahimaiml/epi-recorder/releases)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/epi-recorder/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/epi-recorder?style=flat-square&color=10b981)](https://pypi.org/project/epi-recorder/)

---

## The Problem

Before PDF, you couldn't trust a document. Was this the original? Was it edited? Could the other person even open it?

**PDF solved that.** One file. Opens anywhere. Tamper-evident.

Now we have the same problem with AI.

Your AI agent ran overnight. It made decisions. It spent money. It failed. **What actually happened?**

- Your logs are scattered across services
- You can't prove they weren't edited
- The context is incomplete
- You're taking screenshots and pasting JSON into Slack

---

## The Solution

**EPI is the PDF for AI evidence.**

One `.epi` file contains:
- ✅ **Every prompt and response** — Complete context, not fragments
- ✅ **Cryptographic signature** — Proof it wasn't tampered with
- ✅ **Embedded viewer** — Opens in any browser, no software needed
- ✅ **Offline verification** — Works air-gapped, no cloud required

```bash
pip install epi-recorder

# Record everything your agent does
epi run my_agent.py

# Open proof in browser
epi view recording.epi

# Verify it hasn't been tampered with
epi verify recording.epi
```

---

## What Makes This Revolutionary?

PDF became the universal document format because of three properties. EPI has the same three:

| Property | PDF | EPI |
|:---|:---|:---|
| **Self-Contained** | Fonts, images, layout — all in one file | Prompts, responses, environment — all in one file |
| **Universally Viewable** | Opens in any browser or reader | Opens in any browser (embedded HTML viewer) |
| **Tamper-Evident** | Digital signatures prove authenticity | Ed25519 signatures prove logs weren't edited |

**The difference:** PDFs contain *documents*. EPIs contain *proof of what an AI actually did*.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR AGENT RUNS                          │
│                                                             │
│   Agent calls OpenAI ──► EPI intercepts ──► Records call   │
│   Agent calls Gemini ──► EPI intercepts ──► Records call   │
│   Agent makes HTTP   ──► EPI intercepts ──► Records call   │
│                                                             │
│                    ▼                                        │
│              .epi file created                              │
│              (signed + sealed)                              │
└─────────────────────────────────────────────────────────────┘
```

**Zero code changes.** EPI uses Python's `sitecustomize.py` to inject instrumentation before your code runs. It intercepts LLM calls at the library level—your agent doesn't know it's being recorded.

**Crash-safe.** Every step is written to SQLite immediately. Power goes out? The evidence survives.

**Signed.** When recording finishes, EPI seals everything with an Ed25519 signature. Change one byte, the signature breaks.

---

## The .epi File Format

An `.epi` file is a ZIP archive with a defined structure:

```text
evidence.epi
├── mimetype              # "application/epi+zip"
├── manifest.json         # Metadata + cryptographic signature
├── steps.jsonl           # Every LLM call (NDJSON format)
├── env.json              # Python version, packages, env vars
└── viewer/
    └── index.html        # Self-contained offline viewer
```

**Open it in any browser.** Double-click the embedded `viewer/index.html` and you see a complete timeline of what happened, with verification status.

---

## CLI Reference

| Command | What It Does |
|:---|:---|
| `epi run <script.py>` | Record everything, save as `.epi` |
| `epi view <file.epi>` | Open the timeline viewer in browser |
| `epi verify <file.epi>` | Check cryptographic integrity |
| `epi debug <file.epi>` | Analyze for bugs (loops, hallucinations) |
| `epi chat <file.epi>` | Ask questions about the recording (via Gemini) |
| `epi init` | Interactive setup wizard |
| `epi doctor` | Fix common environment issues |

---

## Python API

```python
from epi_recorder import record

# Decorator
@record(goal="Test trading strategy")
def run_agent():
    ...

# Context manager
with record("evidence.epi"):
    agent.run()
```

---

## Security

| Layer | Implementation |
|:---|:---|
| **Signatures** | Ed25519 (same as Signal, SSH) |
| **Hashing** | SHA-256 content addressing |
| **Redaction** | Automatic API key removal |
| **Verification** | Client-side, zero-knowledge |

---

## Supported Frameworks

| Framework | Support |
|:---|:---|
| OpenAI | ✅ Native interception |
| Google Gemini | ✅ Native interception |
| LangChain | ✅ HTTP layer capture |
| CrewAI | ✅ HTTP layer capture |
| Anthropic | ✅ HTTP layer capture |
| Custom agents | ✅ Any `requests`/`httpx` calls |

---

## Release History

| Version | Date | Highlights |
|:---|:---|:---|
| **v2.2.0** | 2026-01-30 | Agent debugging, SQLite storage, async support |
| **v2.1.3** | 2026-01-24 | Gemini support, `epi chat` |
| **v2.1.2** | 2026-01-17 | Client-side signature verification |
| **v2.1.0** | 2025-12-15 | Initial release |

---

## Contributing

```bash
git clone https://github.com/mohdibrahimaiml/epi-recorder.git
cd epi-recorder
pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## License

MIT License. See [LICENSE](./LICENSE).

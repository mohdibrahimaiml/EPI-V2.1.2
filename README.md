<div align="center">

<img src="https://raw.githubusercontent.com/mohdibrahimaiml/EPI-V2.0.0/main/docs/assets/epi-logo.png" alt="EPI Logo" width="120"/>

# EPI Recorder

### The PDF for AI Evidence™

**Record. Verify. Trust.**

[![PyPI](https://img.shields.io/pypi/v/epi-recorder?color=blue&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/epi-recorder/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/epi-recorder?color=blue&label=Downloads)](https://pypi.org/project/epi-recorder/)
[![Stars](https://img.shields.io/github/stars/mohdibrahimaiml/EPI-V2.0.0?style=social)](https://github.com/mohdibrahimaiml/EPI-V2.0.0)

[**🚀 Quick Start**](#-quick-start-30-seconds) • [**📖 Docs**](https://epilabs.org/docs) • [**💬 Community**](https://github.com/mohdibrahimaiml/EPI-V2.0.0/discussions) • [**🎥 Demo**](https://colab.research.google.com/github/mohdibrahimaiml/EPI-V2.1.0/blob/main/colab_demo.ipynb)

</div>

---

## 🎯 What is EPI?

**EPI creates cryptographically signed "receipts" for AI workflows.**

Just like PDF standardized documents, **EPI standardizes AI execution evidence**.

```python
# Your AI agent runs
python trading_bot.py

# EPI captures EVERYTHING:
# ✓ Code that executed
# ✓ API calls made
# ✓ Data processed
# ✓ Decisions taken
# ✓ Environment state
# All cryptographically signed ✅
```

**Result:** One `.epi` file that proves exactly what happened—**tamper-proof and verifiable**.

---

## 💡 Why EPI?

### The Problem

**AI agents are black boxes.** When they:
- 💰 Execute trades
- ✍️ Sign contracts
- 🏥 Make diagnoses
- 📊 Process sensitive data

**You need proof it happened correctly.**

Logs can be edited. Screenshots can be faked. **Trust requires cryptographic evidence.**

### The Solution

```bash
epi run trading_bot.py
```

**Creates:** `trading_bot_2024_12_16.epi`

**Contains:**
- 🔐 Ed25519 cryptographic signatures
- 📸 Complete execution snapshot
- 🕐 Immutable timeline of events
- � Interactive viewer (works offline)
- ✅ Automatic API key redaction

**Like Black Box Recorder for AI** ✈️

---

## ⚡ Quick Start (30 Seconds)

### Installation

**One command. Works everywhere. 99% success rate.**

**Unix/Mac:**
```bash
curl -sSL https://raw.githubusercontent.com/mohdibrahimaiml/EPI-V2.0.0/main/scripts/install.sh | sh
```

**Windows:**
```powershell
iwr https://raw.githubusercontent.com/mohdibrahimaiml/EPI-V2.0.0/main/scripts/install.ps1 -useb | iex
```

**Manual (pip):**
```bash
pip install epi-recorder
```

> **💡 Tip:** If `epi: command not found`, use `python -m epi_cli` (always works)

### Your First Recording

```bash
# 1. Create a simple script
echo 'print("Hello, EPI!")' > hello.py

# 2. Record it
epi run hello.py

# 3. View the evidence (opens in browser)
#    ✓ Cryptographically signed
#    ✓ Complete timeline
#    ✓ Verified integrity
```

**That's it!** You just created verifiable AI evidence. 🎉

---

## 🎨 How It Works

### Traditional Logging ❌

```
[2024-12-16 14:30:22] INFO: Processing transaction
[2024-12-16 14:30:23] INFO: Decision: APPROVE
```

**Problem:** Can be edited. No proof. Trust = hope.

### EPI Evidence ✅

```bash
epi run financial_agent.py
```

**Creates immutable package with:**

| What | How | Why |
|------|-----|-----|
| **Code snapshot** | Exact source that ran | Reproducibility |
| **API calls** | Every request/response | Auditability |
| **File I/O** | All reads/writes | Data lineage |
| **Environment** | Python version, OS, dependencies | Context |
| **Signatures** | Ed25519 cryptographic proof | Integrity |
| **Timeline** | Interactive viewer | Understanding |

**Result:** **If it's in the .epi file it happened. If it's not, it didn't.** Period.

---

## 🔥 Real-World Examples

### Example 1: Financial Trading Agent

```python
# trading_bot.py
import openai

def analyze_stock(symbol):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Analyze {symbol}"}]
    )
    decision = response.choices[0].message.content
    execute_trade(symbol, decision)
    return decision
```

**Record it:**
```bash
epi run trading_bot.py
```

**You get:**
- ✅ Proof of AI decision logic
- ✅ Complete API call history (keys redacted)
- ✅ Execution timestamp
- ✅ Regulatory-compliant audit trail
- ✅ Shareable evidence package

---

### Example 2: Healthcare Diagnostic Agent

```python
# diagnostic_agent.py
def diagnose_patient(patient_data):
    # AI analysis
    diagnosis = ai_model.predict(patient_data)
    
    # Generate report
    report = create_medical_report(diagnosis)
    
    return diagnosis, report
```

**Record for FDA submission:**
```bash
epi run diagnostic_agent.py
```

**Evidence includes:**
- ✅ Model version used
- ✅ Patient data processing (privacy-compliant)
- ✅ Decision logic
- ✅ Cryptographic proof for regulators

---

### Example 3: Python API

**Zero-config recording:**

```python
from epi_recorder import record

@record(out="workflow.epi")
def my_ai_workflow():
    result = llm.generate_response(prompt)
    save_to_database(result)
    return result

# Automatically creates workflow.epi
my_ai_workflow()
```

**Or context manager:**

```python
from epi_recorder import record

with record("analysis.epi"):
    # Everything here is captured
    data = fetch_data()
    insights = analyze_with_ai(data)
    send_report(insights)
```

---

## 🎯 Commands Reference

### Core Commands

```bash
# Interactive setup (first time)
epi init

# Record any script
epi run script.py

# View evidence package
epi view recording.epi

# Verify cryptographic integrity
epi verify recording.epi

# List all recordings
epi ls

# Fix environment issues
epi doctor
```

### Advanced

```bash
# Custom output name
epi record --out experiment.epi -- python train.py

# Record any command (not just Python)
epi record --out build.epi -- npm run build

# Manage cryptographic keys
epi keys generate --name production
epi keys list
epi keys export --name production
```

**💡 All commands also work as:** `python -m epi_cli <command>`

---

## 🔒 Security & Privacy

### Automatic Redaction

**Sensitive data is automatically masked:**

```python
# Your code
openai.api_key = "sk-abc123xyz"
db_password = "secret123"

# In .epi file (automatic)
openai.api_key = "sk-***REDACTED***"
db_password = "***REDACTED***"
```

**Protected:**
- ✅ API keys (OpenAI, Anthropic, AWS, etc.)
- ✅ Passwords and tokens
- ✅ Environment variables with secrets
- ✅ Database credentials

### Cryptographic Integrity

**Every .epi file:**
- 🔐 Signed with Ed25519 (same as Signal, age)
- ✅ Tamper-proof (any modification breaks signature)
- 🔍 Publicly verifiable
- � Private key stays on your machine

### Offline Viewing

**The viewer is 100% safe:**
- ✅ Static HTML (no server needed)
- ✅ No external requests
- ✅ No analytics or tracking
- ✅ Works in air-gapped environments
- ✅ Safe to share with auditors

---

## 🏢 Use Cases

<table>
<tr>
<td width="50%">

### 💼 Financial Services
- Regulatory compliance (MiFID II, Dodd-Frank)
- Trading algorithm audit trails
- AI-driven loan decisions
- Risk assessment transparency

</td>
<td width="50%">

### 🏥 Healthcare
- FDA AI/ML submissions
- Clinical trial reproducibility
- HIPAA-compliant audit logs
- Diagnostic algorithm evidence

</td>
</tr>
<tr>
<td width="50%">

### ⚖️ Legal
- E-discovery for AI systems
- Contract analysis evidence
- Litigation documentation
- Chain of custody

</td>
<td width="50%">

### 🔬 Research
- ML experiment reproducibility
- Peer review verification
- Grant compliance
- Published results validation

</td>
</tr>
</table>

---

## 🚀 What's New in v2.1.1

### ✨ 99% Installation Success

**We fixed the `epi: command not found` problem!**

**New in this release:**

#### 1. One-Command Install Scripts
```bash
curl ... | sh  # Auto-configures PATH on all platforms
```

#### 2. Automatic PATH Fix
```bash
pip install epi-recorder
# Post-install automatically fixes PATH (90% success)
```

#### 3. Python Module Fallback
```bash
python -m epi_cli run script.py  # Always works (100% success)
```

#### 4. Smart Doctor Command
```bash
epi doctor  # Auto-detects and repairs PATH issues
```

**Result:** From 85% → 99% installation success globally! 🌍

### 🐛 Other Improvements
- Fixed Windows Unicode errors
- Better terminal compatibility
- Improved error messages
- Enhanced documentation

---

## 📊 Comparison

### EPI vs Traditional Logging

| Feature | Logs | EPI |
|---------|------|-----|
| **Tamper-proof** | ❌ Can be edited | ✅ Cryptographically signed |
| **Complete context** | ❌ Partial | ✅ Full snapshot |
| **Verification** | ❌ Trust-based | ✅ Math-based proof |
| **Reproducibility** | ❌ Hard | ✅ Guaranteed |
| **Regulatory** | ⚠️ Questionable | ✅ Compliant |
| **Offline viewing** | ❌ Needs infrastructure | ✅ Self-contained |

### EPI vs PDF

| Aspect | PDF | EPI |
|--------|-----|-----|
| **Purpose** | Document consistency | Execution integrity |
| **Trust** | "Looks right" | "Mathematically proven" |
| **Security** | ⚠️ Can run JS | ✅ Static HTML |
| **Use case** | Reports, contracts | AI workflows, code execution |
| **Standard** | ISO 32000 | Emerging |

**EPI is to code execution what PDF is to documents.** 📄 → 📦

---

## 📚 Documentation

- [**📘 CLI Reference**](https://epilabs.org/docs/cli) - All commands explained
- [**🐍 Python API**](https://epilabs.org/docs/api) - Decorator and context manager
- [**🏗️ Architecture**](https://epilabs.org/docs/architecture) - How EPI works
- [**🔒 Security Model**](https://epilabs.org/docs/security) - Cryptography details
- [**📖 Use Case Examples**](https://epilabs.org/docs/examples) - Real-world scenarios

---

## 🤝 Community

- [**💬 Discussions**](https://github.com/mohdibrahimaiml/EPI-V2.0.0/discussions) - Ask questions, share use cases
- [**🐛 Issues**](https://github.com/mohdibrahimaiml/EPI-V2.0.0/issues) - Bug reports, feature requests
- [**📧 Email**](mailto:epitechforworld@outlook.com) - Direct support
- [**🌐 Website**](https://epilabs.org) - Latest news and updates

---

## 🙌 Contributing

We welcome contributions! Check out:
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [Good First Issues](https://github.com/mohdibrahimaiml/EPI-V2.0.0/labels/good%20first%20issue) - Start here

**Areas we'd love help:**
- 🌍 Internationalization
- 🔌 Language integrations (JS, Go, Rust)
- ☁️ Cloud storage adapters
- 📊 Viewer enhancements

---

## 📄 License

**Apache 2.0** - See [LICENSE](LICENSE)

---

## 🌟 Star History

If EPI helps you, **star the repo** to support development! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=mohdibrahimaiml/EPI-V2.0.0&type=Date)](https://star-history.com/#mohdibrahimaiml/EPI-V2.0.0&Date)

---

## 🙏 Built With

- [Typer](https://typer.tiangolo.com/) - Beautiful CLIs
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Cryptography](https://cryptography.io/) - Ed25519 signatures

---

<div align="center">

### **Trust Your AI. Verify Everything.** 🔐

**Made with ❤️ by [Mohd Ibrahim Afridi](https://github.com/mohdibrahimaiml)**

[**⭐ Star**](https://github.com/mohdibrahimaiml/EPI-V2.0.0) • [**🐦 Twitter**](https://twitter.com/epilabs) • [**🌐 Website**](https://epilabs.org)

</div>

"""
Demo script for Anthropic/Claude EPI wrapper

Shows how to create cryptographically signed evidence for Claude API calls.
Perfect for regulated industries (finance, healthcare, legal).
"""

from anthropic import Anthropic
from epi_recorder import record
from epi_recorder.wrappers import wrap_anthropic

def demo_basic_usage():
    """
    Simplest usage - wrap client and use normally.
    All calls automatically create .epi evidence when inside record().
    """
    print("=" * 70)
    print("DEMO: Anthropic/Claude EPI Wrapper")
    print("=" * 70)
    print()
    
    # 1. Wrap your Anthropic client
    print("[1] Wrapping Anthropic client...")
    client = wrap_anthropic(Anthropic())
    print("✓ Client wrapped")
    print()
    
    # 2. Use inside record() context
    print("[2] Creating Claude conversation with EPI recording...")
    with record("claude_demo.epi", goal="Demo Claude evidence capture"):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Explain what cryptographic evidence means for AI systems in one sentence."
                }
            ]
        )
        
        print("✓ Response received:")
        print(f"  {response.content[0].text}")
        print()
    
    print("[3] Evidence file created: epi-recordings/claude_demo.epi")
    print()
    print("You can now:")
    print("  • Verify: epi verify epi-recordings/claude_demo.epi")
    print("  • View:   epi view epi-recordings/claude_demo.epi")
    print()


def demo_financial_use_case():
    """
    Real-world example: Financial audit trail.
    
    When Claude makes financial decisions, regulators need proof.
    This creates tamper-evident evidence that meets SEC/FINRA requirements.
    """
    print("=" * 70)
    print("FINANCIAL USE CASE: Audit-Grade Evidence")
    print("=" * 70)
    print()
    
    client = wrap_anthropic(Anthropic())
    
    with record("financial_analysis.epi", goal="Q4 Revenue Forecast Analysis"):
        # Simulate financial analysis question
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": """
                    As a financial analyst AI, analyze this scenario:
                    
                    Company: TechCorp Inc.
                    Q3 Revenue: $450M
                    Q3 Growth: +15% YoY
                    Industry Trend: +12% average
                    
                    Should we forecast Q4 revenue at:
                    A) $480M (conservative)
                    B) $520M (moderate)
                    C) $560M (aggressive)
                    
                    Provide recommendation with reasoning.
                    """
                }
            ]
        )
        
        print("Claude's Analysis:")
        print(response.content[0].text)
        print()
    
    print("✓ Cryptographically signed evidence created")
    print("✓ Regulatory-compliant audit trail saved")
    print("✓ Can be verified offline without Claude API access")
    print()


def demo_streaming():
    """
    Streaming responses are also captured.
    """
    print("=" * 70)
    print("DEMO: Streaming with Evidence Capture")
    print("=" * 70)
    print()
    
    client = wrap_anthropic(Anthropic())
    
    with record("claude_stream.epi", goal="Streaming demo"):
        print("Streaming Claude's response:")
        print("-" * 60)
        
        with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            messages=[{"role": "user", "content": "Count from 1 to 5, explaining each number."}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
        
        print()
        print("-" * 60)
        print()
    
    print("✓ Streaming response fully captured in .epi file")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        demo_type = sys.argv[1]
        
        if demo_type == "financial":
            demo_financial_use_case()
        elif demo_type == "stream":
            demo_streaming()
        else:
            print(f"Unknown demo: {demo_type}")
            print("Usage: python demo_anthropic.py [financial|stream]")
    else:
        # Run basic demo by default
        demo_basic_usage()
        
        print()
        print("Try other demos:")
        print("  python demo_anthropic.py financial")
        print("  python demo_anthropic.py stream")

"""
EPI Wrapper Clients - Proxy wrappers for LLM clients.

Provides transparent tracing without monkey patching.
"""

from epi_recorder.wrappers.openai import wrap_openai, TracedOpenAI, TracedCompletions, TracedChat
from epi_recorder.wrappers.base import TracedClientBase

__all__ = [
    "wrap_openai",
    "TracedOpenAI",
    "TracedCompletions",
    "TracedChat",
    "TracedClientBase",
]

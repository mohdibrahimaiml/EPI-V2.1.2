"""
OpenAI wrapper for EPI tracing.

Provides a proxy wrapper that automatically logs all LLM calls
without monkey patching.
"""

import time
from typing import Any, Optional
from datetime import datetime

from epi_recorder.wrappers.base import TracedClientBase


class TracedCompletions:
    """Proxy wrapper for openai.chat.completions."""
    
    def __init__(self, completions: Any, provider: str = "openai"):
        self._completions = completions
        self._provider = provider
    
    def _get_session(self):
        """Get the current active EPI recording session."""
        from epi_recorder.api import get_current_session
        return get_current_session()
    
    def create(self, *args, **kwargs) -> Any:
        """
        Create a chat completion with automatic EPI tracing.
        
        All arguments are passed through to the underlying client.
        """
        session = self._get_session()
        
        # Extract request info
        model = kwargs.get("model", "unknown")
        messages = kwargs.get("messages", [])
        
        # Log request if session is active
        if session:
            session.log_step("llm.request", {
                "provider": self._provider,
                "model": model,
                "messages": messages,
                "timestamp": datetime.utcnow().isoformat(),
            })
        
        # Call original method
        start_time = time.time()
        try:
            response = self._completions.create(*args, **kwargs)
            latency = time.time() - start_time
            
            # Log response if session is active
            if session:
                # Extract response content
                choices = []
                for choice in response.choices:
                    msg = choice.message
                    choices.append({
                        "message": {
                            "role": getattr(msg, "role", "assistant"),
                            "content": getattr(msg, "content", ""),
                        },
                        "finish_reason": getattr(choice, "finish_reason", None),
                    })
                
                # Extract usage
                usage = None
                if hasattr(response, "usage") and response.usage:
                    usage = {
                        "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                        "completion_tokens": getattr(response.usage, "completion_tokens", 0),
                        "total_tokens": getattr(response.usage, "total_tokens", 0),
                    }
                
                session.log_step("llm.response", {
                    "provider": self._provider,
                    "model": model,
                    "choices": choices,
                    "usage": usage,
                    "latency_seconds": round(latency, 3),
                    "timestamp": datetime.utcnow().isoformat(),
                })
            
            return response
            
        except Exception as e:
            latency = time.time() - start_time
            
            # Log error if session is active
            if session:
                session.log_step("llm.error", {
                    "provider": self._provider,
                    "model": model,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "latency_seconds": round(latency, 3),
                    "timestamp": datetime.utcnow().isoformat(),
                })
            
            raise


class TracedChat:
    """Proxy wrapper for openai.chat."""
    
    def __init__(self, chat: Any, provider: str = "openai"):
        self._chat = chat
        self._provider = provider
        self.completions = TracedCompletions(chat.completions, provider)


class TracedOpenAI(TracedClientBase):
    """
    Traced OpenAI client wrapper.
    
    Wraps an OpenAI client and automatically logs all LLM calls
    to the active EPI recording session.
    
    Usage:
        from openai import OpenAI
        from epi_recorder.wrappers import wrap_openai
        
        client = wrap_openai(OpenAI())
        
        with record("my_agent.epi"):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hello"}]
            )
    """
    
    def __init__(self, client: Any, provider: str = "openai"):
        """
        Initialize traced OpenAI client.
        
        Args:
            client: OpenAI client instance
            provider: Provider name for logging (default: "openai")
        """
        super().__init__(client)
        self._provider = provider
        self.chat = TracedChat(client.chat, provider)
    
    def __getattr__(self, name: str) -> Any:
        """
        Forward attribute access to underlying client.
        
        This allows access to non-chat APIs (embeddings, files, etc.)
        without explicit wrapping.
        """
        return getattr(self._client, name)


def wrap_openai(client: Any, provider: str = "openai") -> TracedOpenAI:
    """
    Wrap an OpenAI client for EPI tracing.
    
    Args:
        client: OpenAI client instance
        provider: Provider name for logging (default: "openai")
        
    Returns:
        TracedOpenAI wrapper
        
    Usage:
        from openai import OpenAI
        from epi_recorder.wrappers import wrap_openai
        
        # Wrap the client once
        client = wrap_openai(OpenAI())
        
        # Use normally - calls are automatically traced when inside record()
        with record("my_agent.epi"):
            response = client.chat.completions.create(...)
    """
    return TracedOpenAI(client, provider)

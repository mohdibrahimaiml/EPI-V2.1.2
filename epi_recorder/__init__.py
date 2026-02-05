"""
EPI Recorder - Runtime interception and workflow capture.

Python API for recording AI workflows with cryptographic verification.
"""

__version__ = "2.3.0"

# Export Python API
from epi_recorder.api import (
    EpiRecorderSession,
    record,
    get_current_session
)

# Export wrapper clients (new in v2.3.0)
from epi_recorder.wrappers import (
    wrap_openai,
    TracedOpenAI,
)

__all__ = [
    "EpiRecorderSession",
    "record",
    "get_current_session",
    "wrap_openai",
    "TracedOpenAI",
    "__version__"
]



 
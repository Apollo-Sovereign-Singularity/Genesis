"""
pytest configuration for Apollo Sovereign Singularity tests
Handles Python path setup for proper module imports
"""

import sys
from pathlib import Path

# Add the repository root to Python path for imports
repo_root = Path(__file__).parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

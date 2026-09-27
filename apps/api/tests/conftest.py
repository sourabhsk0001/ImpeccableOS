import sys
import os

# Ensure apps/api directory is at the front of sys.path for test discovery
api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

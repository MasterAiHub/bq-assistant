import time
from collections import defaultdict
from typing import Dict, Tuple
import os
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Advanced rate limiting for security"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.limit = int(os.getenv("RATE_LIMIT", 100))
        self.window = int(os.getenv("RATE_LIMIT_WINDOW", 60))
    
    def is_allowed(self, key: str) -> Tuple[bool, int]:
        """Check if request is allowed based on rate limits"""
        current_time = time.time()
        self.requests[key] = [t for t in self.requests[key] if t > current_time - self.window]
        
        if len(self.requests[key]) >= self.limit:
            return False, 0
        
        self.requests[key].append(current_time)
        remaining = self.limit - len(self.requests[key])
        return True, remaining
    
    def get_retry_after(self, key: str) -> int:
        """Calculate retry-after time in seconds"""
        if key not in self.requests:
            return 0
        
        current_time = time.time()
        oldest = min(self.requests[key]) if self.requests[key] else current_time
        return int(self.window - (current_time - oldest))

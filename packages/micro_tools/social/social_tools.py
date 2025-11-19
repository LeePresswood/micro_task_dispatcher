from dataclasses import dataclass
from typing import Optional

@dataclass
class SocialPostResult:
    """Standardized result for a social media post."""
    platform: str
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None

def post_to_threads(message: str) -> SocialPostResult:
    """
    Post a message to Threads.
    
    Args:
        message: The text content to post.
        
    Returns:
        SocialPostResult indicating success or failure.
    """
    print(f"[Threads] Posting: {message}")
    return SocialPostResult(platform="Threads", success=True, message_id="mock_threads_123")

def post_to_bluesky(message: str) -> SocialPostResult:
    """
    Post a message to Bluesky.
    
    Args:
        message: The text content to post.
        
    Returns:
        SocialPostResult indicating success or failure.
    """
    print(f"[Bluesky] Posting: {message}")
    return SocialPostResult(platform="Bluesky", success=True, message_id="mock_bsky_456")

def post_to_x(message: str) -> SocialPostResult:
    """
    Post a message to X (Twitter).
    
    Args:
        message: The text content to post.
        
    Returns:
        SocialPostResult indicating success or failure.
    """
    print(f"[X] Posting: {message}")
    return SocialPostResult(platform="X", success=True, message_id="mock_x_789")

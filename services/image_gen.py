"""
Higher-level image generation helpers (wraps openai_client.create_image).
"""
from .openai_client import create_image

def generate_storyboard_images(scene_prompts, size="1024x1024"):
    """
    scene_prompts: list of textual prompts for each scene
    returns list of image URLs
    """
    results = []
    for p in scene_prompts:
        url = create_image(p, size=size)
        results.append(url)
    return results

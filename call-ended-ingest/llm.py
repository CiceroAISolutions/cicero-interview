import time


def complete(prompt: str) -> str:
    """Stand-in for a hosted model. No API key. In production this is slow and billed.

    The return value is untrusted. It may be wrong or incomplete.
    """
    time.sleep(0.4)
    return (
        "Placeholder model output. Do not treat this as ground truth.\n"
        f"Prompt length: {len(prompt)} characters."
    )

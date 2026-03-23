from typing import List

def find_possible_emails(domain: str) -> List[str]:
    """
    Generate possible recruiter email addresses based on common patterns.

    Args:
        domain (str): The company domain (e.g., 'company.com')

    Returns:
        List[str]: List of possible email addresses
    """
    patterns = ['hr', 'careers', 'jobs', 'recruitment']
    return [f"{pattern}@{domain}" for pattern in patterns]
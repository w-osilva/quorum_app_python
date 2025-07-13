"""
Navigation helper for the Flask application
"""

from flask import url_for


def get_navigation_items():
    """Get the navigation items for the application"""
    return [
        {"title": "Legislators", "url": url_for("legislators.list_legislators")},
        {"title": "Bills", "url": url_for("bills.list_bills")},
        {"title": "Votes", "url": url_for("votes.list_votes")},
        {"title": "Vote Results", "url": url_for("vote_results.list_vote_results")},
    ]


def inject_navigation():
    """Context processor function to inject navigation items into templates"""
    return {"nav_items": get_navigation_items()}

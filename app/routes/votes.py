from flask import Blueprint, Response

from app.lib.multi_response import render
from app.models.vote import Vote

bp = Blueprint("votes", __name__)


@bp.route("/votes")
@bp.route("/votes/")
def list_votes() -> Response:
    votes = Vote.query.all()
    return render({"votes": votes}, template="votes/index.html", filename="votes.csv")


@bp.route("/votes/<int:vote_id>")
def show_vote(vote_id: int) -> Response:
    vote = Vote.query.get_or_404(vote_id)
    return render(
        {"vote": vote},
        template="votes/show.html",
        filename=f"vote_{vote_id}.csv",
    )

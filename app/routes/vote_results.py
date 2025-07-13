from flask import Blueprint, Response

from app.lib.multi_response import render
from app.models.vote_result import VoteResult

bp = Blueprint("vote_results", __name__)


@bp.route("/vote_results")
@bp.route("/vote_results/")
def list_vote_results() -> Response:
    vote_results = VoteResult.query.all()
    return render(
        {"vote_results": vote_results},
        template="vote_results/index.html",
        filename="vote_results.csv",
    )


@bp.route("/vote_results/<int:vote_result_id>")
def show_vote_result(vote_result_id: int) -> Response:
    vote_result = VoteResult.query.get_or_404(vote_result_id)
    return render(
        {"vote_result": vote_result},
        template="vote_results/show.html",
        filename=f"vote_result_{vote_result_id}.csv",
    )

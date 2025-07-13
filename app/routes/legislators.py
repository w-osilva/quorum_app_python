from flask import Blueprint, Response

from app.lib.multi_response import render
from app.models.legislator import Legislator

bp = Blueprint("legislators", __name__)


@bp.route("/legislators")
@bp.route("/legislators/")
def list_legislators() -> Response:
    legislators = Legislator.query.all()
    return render(
        {"legislators": legislators},
        template="legislators/index.html",
        filename="legislators.csv",
    )


@bp.route("/legislators/<int:legislator_id>")
def show_legislator(legislator_id: int) -> Response:
    legislator = Legislator.query.get_or_404(legislator_id)
    return render(
        {"legislator": legislator},
        template="legislators/show.html",
        filename=f"legislator_{legislator_id}.csv",
    )

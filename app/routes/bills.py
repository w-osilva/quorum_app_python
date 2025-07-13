from flask import Blueprint, Response

from app.lib.multi_response import render
from app.models.bill import Bill

bp = Blueprint("bills", __name__)


@bp.route("/bills")
@bp.route("/bills/")
def list_bills() -> Response:
    bills = Bill.query.all()
    return render({"bills": bills}, template="bills/index.html", filename="bills.csv")


@bp.route("/bills/<int:bill_id>")
def show_bill(bill_id: int) -> Response:
    bill = Bill.query.get_or_404(bill_id)
    return render(
        {"bill": bill},
        template="bills/show.html",
        filename=f"bill_{bill_id}.csv",
    )

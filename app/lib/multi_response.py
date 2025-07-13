from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from flask import Response, jsonify, render_template, request


class MultiResponse:
    """Simple multi-format response handler."""

    @staticmethod
    def _get_format() -> str:
        """Get response format: query param > URL extension > default HTML."""
        # 1. Query parameter (highest priority)
        format_param = request.args.get("format", "").lower()
        if format_param in ["json", "csv"]:
            return format_param

        # 2. URL extension (legacy support)
        if "." in request.path:
            extension = request.path.rsplit(".", 1)[-1].lower()
            if extension in ["json", "csv"]:
                return extension

        # 3. Accept header (API clients only)
        accept = request.headers.get("Accept", "")
        if "application/json" in accept and "text/html" not in accept:
            return "json"
        if "text/csv" in accept and "text/html" not in accept:
            return "csv"

        # 4. Default to HTML
        return "html"

    @staticmethod
    def render(
        context: dict[str, Any],
        template: str | None = None,
        filename: str | None = None,
    ) -> Response:
        """Render response in the appropriate format."""
        format_type = MultiResponse._get_format()

        if format_type == "json":
            return MultiResponse._render_json(context)

        if format_type == "csv":
            return MultiResponse._render_csv(context, filename)

        # html
        return render_template(template, **context)

    @staticmethod
    def _render_json(context: dict[str, Any]) -> Response:
        """Render JSON response using BaseModel serialization."""
        from app.models.base import BaseModel

        # Use BaseModel's helper method for consistent serialization
        serialized_context = BaseModel.serialize_for_json(context)

        response = jsonify(serialized_context)
        response.headers["Content-Type"] = "application/json"
        return response

    @staticmethod
    def _render_csv(context: dict[str, Any], filename: str | None = None) -> Response:
        """Render CSV response."""
        # Get the main data collection
        data = None
        key = None
        for k, v in context.items():
            if isinstance(v, list) and v:  # First non-empty list
                data = v
                key = k
                break

        if not data:
            return Response("No data to export", status=400, mimetype="text/plain")

        # Generate CSV from model data
        output = StringIO()
        first_item = data[0]

        # Use model's CSV methods if available for consistent column ordering
        if hasattr(first_item, "csv_headers") and hasattr(first_item, "to_csv"):
            headers = first_item.csv_headers()

            writer = csv.writer(output)
            writer.writerow(headers)

            for item in data:
                writer.writerow(item.to_csv())
        elif hasattr(first_item, "to_json"):
            # Fallback to JSON method but ensure consistent ordering
            sample = first_item.to_json()
            headers = list(sample.keys())

            writer = csv.DictWriter(output, fieldnames=headers)
            writer.writeheader()

            for item in data:
                writer.writerow(item.to_json())
        else:
            # Fallback for simple objects
            return Response(
                "Cannot export this data type",
                status=400,
                mimetype="text/plain",
            )

        # Set filename
        if not filename:
            filename = f"{key}.csv" if key else "export.csv"
        elif not filename.endswith(".csv"):
            filename += ".csv"

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )


def render(context, **args) -> Response:
    """Render response in the appropriate format."""
    return MultiResponse.render(context, **args)

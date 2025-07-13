from sqlalchemy import func

from app import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    def to_json(self):
        """Convert model instance to JSON representation including computed properties."""
        # Start with table columns
        result = {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

        # Add computed properties from the class
        for attr_name in dir(self.__class__):
            if not attr_name.startswith("_"):
                attr = getattr(self.__class__, attr_name)
                if isinstance(attr, property):
                    try:
                        prop_value = getattr(self, attr_name)
                        # Handle datetime objects and other non-serializable types
                        if hasattr(prop_value, "isoformat"):
                            result[attr_name] = prop_value.isoformat()
                        else:
                            result[attr_name] = prop_value
                    except Exception:
                        # Skip properties that can't be computed (e.g., due to missing relationships)
                        continue

        return result

    @staticmethod
    def serialize_for_json(obj):
        """Helper method to serialize any object or collection for JSON."""
        if obj is None:
            return None
        if isinstance(obj, list):
            return [BaseModel.serialize_for_json(item) for item in obj]
        if hasattr(obj, "to_json"):
            return obj.to_json()
        if isinstance(obj, dict):
            return {k: BaseModel.serialize_for_json(v) for k, v in obj.items()}
        return obj

    @classmethod
    def csv_headers(cls):
        """CSV headers for model export with logical ordering."""
        columns = [column.name for column in cls.__table__.columns]
        # Ensure id comes first, then other columns in a logical order
        if "id" in columns:
            columns.remove("id")
            columns.insert(0, "id")
        return columns

    def to_csv(self):
        """Convert model instance to CSV row format."""
        headers = self.csv_headers()
        return [getattr(self, column_name) for column_name in headers]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"

import os
import tempfile

import pytest

from app.models.legislator import Legislator
from app.services.importers.legislator_importer import LegislatorImporter


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing"""
    csv_content = """id,name
1,John Doe
2,Jane Smith
3,Bob Johnson"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    yield temp_file
    os.unlink(temp_file)


class TestLegislatorImporter:
    def test_import_legislators_success(self, sync_session, sample_csv_file):
        """Test successful import of legislators"""
        importer = LegislatorImporter(sync_session)
        result = importer.import_from_file(sample_csv_file)

        assert result.success is True
        assert result.imported_count == 3
        assert result.errors == []

        # Check that legislators were created
        legislators = sync_session.query(Legislator).all()
        assert len(legislators) == 3

        # Check specific legislator
        john_doe = sync_session.query(Legislator).filter_by(name="John Doe").first()
        assert john_doe is not None
        assert john_doe.id == 1

    def test_import_legislators_missing_file(self, sync_session):
        """Test import with missing file"""
        importer = LegislatorImporter(sync_session)
        result = importer.import_from_file("nonexistent_file.csv")

        assert result.success is False
        assert result.imported_count == 0
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()

    def test_import_legislators_invalid_csv(self, sync_session):
        """Test import with invalid CSV format"""
        # Create invalid CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("invalid,csv,format\nno,proper,headers")
            temp_file = f.name

        try:
            importer = LegislatorImporter(sync_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_legislators_duplicate_ids(self, sync_session):
        """Test import with duplicate IDs"""
        # Create CSV with duplicate IDs
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,name\n1,John Doe\n1,Jane Smith")
            temp_file = f.name

        try:
            importer = LegislatorImporter(sync_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Only first one imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_legislators_empty_file(self, sync_session):
        """Test import with empty file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,name\n")  # Only headers
            temp_file = f.name

        try:
            importer = LegislatorImporter(sync_session)
            result = importer.import_from_file(temp_file)

            assert result.success is True
            assert result.imported_count == 0
            assert result.errors == []
        finally:
            os.unlink(temp_file)

    def test_import_legislators_missing_required_fields(self, sync_session):
        """Test import with missing required fields"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id\n1\n2")  # Missing name column
            temp_file = f.name

        try:
            importer = LegislatorImporter(sync_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

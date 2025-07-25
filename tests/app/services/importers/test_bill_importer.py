import os
import tempfile

import pytest

from app.models.bill import Bill
from app.services.importers.bill_importer import BillImporter
from tests.factories import create_legislator


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing"""
    csv_content = """id,title,sponsor_id
1,Test Bill 1,1
2,Test Bill 2,1
3,Test Bill 3,1"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    yield temp_file
    os.unlink(temp_file)


class TestBillImporter:
    def test_import_bills_success(
        self,
        db_session,
        sample_csv_file,
    ):
        """Test successful import of bills"""
        # Create test legislator using factory
        create_legislator(id=1, name="Test Legislator")

        importer = BillImporter(db_session)
        result = importer.import_from_file(sample_csv_file)

        assert result.success is True
        assert result.imported_count == 3
        assert result.errors == []

        # Check that bills were created
        bills = db_session.query(Bill).all()
        assert len(bills) == 3

        # Check specific bill
        test_bill = db_session.query(Bill).filter_by(title="Test Bill 1").first()
        assert test_bill is not None
        assert test_bill.id == 1
        assert test_bill.sponsor_id == 1

    def test_import_bills_missing_file(self, db_session):
        """Test import with missing file"""
        importer = BillImporter(db_session)
        result = importer.import_from_file("nonexistent_file.csv")

        assert result.success is False
        assert result.imported_count == 0
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()

    def test_import_bills_invalid_csv(self, db_session):
        """Test import with invalid CSV format"""
        # Create invalid CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("invalid,csv,format\nno,proper,headers")
            temp_file = f.name

        try:
            importer = BillImporter(db_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_bills_duplicate_ids(self, db_session):
        """Test import with duplicate IDs"""
        # Create test legislator using factory
        create_legislator(id=1, name="Test Legislator")

        # Create CSV with duplicate IDs
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,title,sponsor_id\n1,Test Bill 1,1\n1,Test Bill 2,1")
            temp_file = f.name

        try:
            importer = BillImporter(db_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Only first one imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_bills_empty_file(self, db_session):
        """Test import with empty file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,title,sponsor_id\n")  # Only headers
            temp_file = f.name

        try:
            importer = BillImporter(db_session)
            result = importer.import_from_file(temp_file)

            assert result.success is True
            assert result.imported_count == 0
            assert result.errors == []
        finally:
            os.unlink(temp_file)

    def test_import_bills_missing_required_fields(self, db_session):
        """Test import with missing required fields"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,title\n1,Test Bill")  # Missing sponsor_id column
            temp_file = f.name

        try:
            importer = BillImporter(db_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_bills_invalid_sponsor_id(self, db_session):
        """Test import with invalid sponsor_id (non-existent legislator)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,title,sponsor_id\n1,Test Bill,999")  # Non-existent sponsor_id
            temp_file = f.name

        try:
            importer = BillImporter(db_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Bill still imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

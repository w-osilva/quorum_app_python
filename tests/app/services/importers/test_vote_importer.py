import os
import tempfile

import pytest

from app.models.vote import Vote
from app.services.importers.vote_importer import VoteImporter
from tests.factories import create_bill


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing"""
    csv_content = """id,bill_id
1,1
2,1
3,1"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    yield temp_file
    os.unlink(temp_file)


class TestVoteImporter:
    def test_import_votes_success(self, db_session, sample_csv_file):
        """Test successful import of votes"""
        # Create test bill using factory
        create_bill(id=1, title="Test Bill", sponsor_id=1)

        importer = VoteImporter(db_session)
        result = importer.import_from_file(sample_csv_file)

        assert result.success is True
        assert result.imported_count == 3
        assert result.errors == []

        # Check that votes were created
        votes = db_session.query(Vote).all()
        assert len(votes) == 3

        # Check specific vote
        test_vote = db_session.query(Vote).filter_by(id=1).first()
        assert test_vote is not None
        assert test_vote.bill_id == 1

    def test_import_votes_missing_file(self, db_session):
        """Test import with missing file"""
        importer = VoteImporter(db_session)
        result = importer.import_from_file("nonexistent_file.csv")

        assert result.success is False
        assert result.imported_count == 0
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()

    def test_import_votes_invalid_csv(self, db_session):
        """Test import with invalid CSV format"""
        # Create invalid CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("invalid,csv,format\nno,proper,headers")
            temp_file = f.name

        try:
            importer = VoteImporter(db_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_votes_duplicate_ids(self, db_session):
        """Test import with duplicate IDs"""
        # Create test bill using factory
        create_bill(id=1, title="Test Bill", sponsor_id=1)

        # Create CSV with duplicate IDs
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,bill_id\n1,1\n1,1")
            temp_file = f.name

        try:
            importer = VoteImporter(db_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Only first one imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_votes_empty_file(self, db_session):
        """Test import with empty file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,bill_id\n")  # Only headers
            temp_file = f.name

        try:
            importer = VoteImporter(db_session)
            result = importer.import_from_file(temp_file)

            assert result.success is True
            assert result.imported_count == 0
            assert result.errors == []
        finally:
            os.unlink(temp_file)

    def test_import_votes_missing_required_fields(self, db_session):
        """Test import with missing required fields"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id\n1")  # Missing bill_id column
            temp_file = f.name

        try:
            importer = VoteImporter(db_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_votes_invalid_bill_id(self, db_session):
        """Test import with invalid bill_id (non-existent bill)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,bill_id\n1,999")  # Non-existent bill_id
            temp_file = f.name

        try:
            importer = VoteImporter(db_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Vote still imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

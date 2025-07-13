import os
import tempfile

import pytest

from app.models.bill import Bill
from app.models.legislator import Legislator
from app.models.vote import Vote
from app.models.vote_result import VoteResult
from app.services.importers.vote_result_importer import VoteResultImporter


@pytest.fixture
def sample_data(sync_session):
    """Create sample data for testing"""
    # Create legislator
    legislator = Legislator(id=1, name="Test Legislator")
    sync_session.add(legislator)

    # Create bill
    bill = Bill(id=1, title="Test Bill", sponsor_id=1)
    sync_session.add(bill)

    # Create vote
    vote = Vote(id=1, bill_id=1)
    sync_session.add(vote)

    sync_session.commit()
    return {"legislator": legislator, "bill": bill, "vote": vote}


@pytest.fixture
def sample_csv_file():
    """Create a sample CSV file for testing"""
    csv_content = """id,legislator_id,vote_id,vote_type
1,1,1,1
2,1,1,2
3,1,1,1"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        temp_file = f.name

    yield temp_file
    os.unlink(temp_file)


class TestVoteResultImporter:
    def test_import_vote_results_success(
        self,
        sync_session,
        sample_data,
        sample_csv_file,
    ):
        """Test successful import of vote results"""
        importer = VoteResultImporter(sync_session)
        result = importer.import_from_file(sample_csv_file)

        assert result.success is True
        assert result.imported_count == 3
        assert result.errors == []

        # Check that vote results were created
        vote_results = sync_session.query(VoteResult).all()
        assert len(vote_results) == 3

        # Check specific vote result
        test_vote_result = sync_session.query(VoteResult).filter_by(id=1).first()
        assert test_vote_result is not None
        assert test_vote_result.legislator_id == 1
        assert test_vote_result.vote_id == 1
        assert test_vote_result.vote_type == 1

    def test_import_vote_results_missing_file(self, sync_session):
        """Test import with missing file"""
        importer = VoteResultImporter(sync_session)
        result = importer.import_from_file("nonexistent_file.csv")

        assert result.success is False
        assert result.imported_count == 0
        assert len(result.errors) > 0
        assert "not found" in result.errors[0].lower()

    def test_import_vote_results_invalid_csv(self, sync_session):
        """Test import with invalid CSV format"""
        # Create invalid CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("invalid,csv,format\nno,proper,headers")
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_vote_results_duplicate_ids(self, sync_session, sample_data):
        """Test import with duplicate IDs"""
        # Create CSV with duplicate IDs
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,legislator_id,vote_id,vote_type\n1,1,1,1\n1,1,1,2")
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Only first one imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_vote_results_empty_file(self, sync_session):
        """Test import with empty file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,legislator_id,vote_id,vote_type\n")  # Only headers
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            assert result.success is True
            assert result.imported_count == 0
            assert result.errors == []
        finally:
            os.unlink(temp_file)

    def test_import_vote_results_missing_required_fields(self, sync_session):
        """Test import with missing required fields"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,legislator_id\n1,1")  # Missing vote_id and vote_type columns
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            assert result.success is False
            assert result.imported_count == 0
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_vote_results_invalid_legislator_id(self, sync_session, sample_data):
        """Test import with invalid legislator_id (non-existent legislator)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "id,legislator_id,vote_id,vote_type\n1,999,1,1",
            )  # Non-existent legislator_id
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Vote result still imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_vote_results_invalid_vote_id(self, sync_session, sample_data):
        """Test import with invalid vote_id (non-existent vote)"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "id,legislator_id,vote_id,vote_type\n1,1,999,1",
            )  # Non-existent vote_id
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Vote result still imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

    def test_import_vote_results_invalid_vote_type(self, sync_session, sample_data):
        """Test import with invalid vote_type"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("id,legislator_id,vote_id,vote_type\n1,1,1,3")  # Invalid vote_type
            temp_file = f.name

        try:
            importer = VoteResultImporter(sync_session)
            result = importer.import_from_file(temp_file)

            # Should still succeed but with errors
            assert result.success is True
            assert result.imported_count == 1  # Vote result still imported
            assert len(result.errors) > 0
        finally:
            os.unlink(temp_file)

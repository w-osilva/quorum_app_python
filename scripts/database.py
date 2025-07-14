#!/usr/bin/env python3
"""
Simple Database Management CLI for Quorum App

Usage:
    python scripts/database.py <command> [table_names...] [options]

Commands:
    create      Create database tables
    drop        Drop database tables
    reset       Drop and recreate tables

Table Names:
    legislators, bills, votes, vote_results
    (if no table names provided, all tables are affected)

Examples:
    python scripts/database.py create
    python scripts/database.py create legislators bills
    python scripts/database.py drop legislators --confirm
    python scripts/database.py reset --with-data
"""

import argparse
import sys
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Bill, Legislator, Vote, VoteResult

# TODO: Discover models dynamically
TABLE_MODELS = {
    "legislators": Legislator,
    "bills": Bill,
    "votes": Vote,
    "vote_results": VoteResult,
}


def get_tables_to_process(table_names):
    """Get list of table models to process."""
    if not table_names:
        # Return all tables in dependency order (for safe operations)
        return [VoteResult, Vote, Bill, Legislator]

    tables = []
    for name in table_names:
        if name not in TABLE_MODELS:
            print(f"❌ Unknown table: {name}")
            print(f"Available tables: {', '.join(TABLE_MODELS.keys())}")
            sys.exit(1)
        tables.append(TABLE_MODELS[name])

    return tables


def create_tables(table_names=None):
    """Create database tables."""
    if table_names:
        tables = get_tables_to_process(table_names)
        print(f"Creating tables: {', '.join(table_names)}")
        for model in tables:
            model.__table__.create(db.engine, checkfirst=True)
        print("✅ Selected tables created successfully!")
    else:
        print("Creating all database tables...")
        db.create_all()
        print("✅ All database tables created successfully!")


def drop_tables(table_names=None):
    """Drop database tables."""
    if table_names:
        tables = get_tables_to_process(table_names)
        print(f"Dropping tables: {', '.join(table_names)}")
        # Drop in reverse order to respect foreign key constraints
        for model in reversed(tables):
            model.__table__.drop(db.engine, checkfirst=True)
        print("✅ Selected tables dropped successfully!")
    else:
        print("Dropping all database tables...")
        db.drop_all()
        print("✅ All database tables dropped successfully!")


def reset_tables(table_names=None, *, with_data=None):
    """Drop and recreate tables."""
    if with_data is None:
        with_data = False

    if table_names:
        print(f"Resetting tables: {', '.join(table_names)}")
    else:
        print("Resetting all database tables...")

    drop_tables(table_names)

    create_tables(table_names)

    # Import data if requested
    if with_data and not table_names:  # Only import all data for full reset
        print("Importing data...")
        try:
            from scripts.importer import main as import_data_main

            import_data_main()
            print("✅ Data imported successfully!")
        except Exception as e:
            print(f"❌ Error importing data: {e}")
            return False

    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Simple Database Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "command",
        choices=["create", "drop", "reset"],
        help="Database command to execute",
    )

    parser.add_argument(
        "table_names",
        nargs="*",
        help="Table names to operate on (legislators, bills, votes, vote_results)",
    )

    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompts for destructive operations",
    )

    parser.add_argument(
        "--with-data",
        action="store_true",
        help="Import data after reset (only for full reset)",
    )

    args = parser.parse_args()

    # Validate table names
    if args.table_names:
        for table_name in args.table_names:
            if table_name not in TABLE_MODELS:
                print(f"❌ Unknown table: {table_name}")
                print(f"Available tables: {', '.join(TABLE_MODELS.keys())}")
                sys.exit(1)

    # Create Flask app context
    app = create_app()

    with app.app_context():
        # Confirmation for destructive operations
        if args.command in ["drop", "reset"] and not args.confirm:
            tables_desc = (
                f"tables: {', '.join(args.table_names)}"
                if args.table_names
                else "ALL TABLES"
            )
            print(f"⚠️  WARNING: This will {args.command} {tables_desc}!")
            response = input("Are you sure? (y/N): ").lower().strip()
            if response not in ["y", "yes"]:
                print("Operation cancelled.")
                return

        # Execute command
        try:
            if args.command == "create":
                create_tables(args.table_names)
            elif args.command == "drop":
                drop_tables(args.table_names)
            elif args.command == "reset":
                reset_tables(args.table_names, args.with_data)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

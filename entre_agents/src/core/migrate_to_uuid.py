#!/usr/bin/env python3
"""
Migration script: Convert entrepreneur IDs to UUIDs

This script migrates existing entrepreneur IDs (like "default_user")
to UUID-based identifiers for cloud scalability.

Usage:
    python src/core/migrate_to_uuid.py --old-id default_user

Or to auto-generate UUID:
    python src/core/migrate_to_uuid.py --old-id default_user --auto
"""

import sys
import uuid
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config
from core.database import DatabaseAdapter


def generate_uuid() -> str:
    """Generate a new UUID4."""
    return str(uuid.uuid4())


def migrate_entrepreneur_id(db: DatabaseAdapter, old_id: str, new_id: str):
    """
    Migrate all records from old entrepreneur ID to new UUID.

    Args:
        db: Database adapter
        old_id: Current entrepreneur ID (e.g., "default_user")
        new_id: New UUID to migrate to
    """
    print(f"\n{'='*60}")
    print(f"MIGRATION: {old_id} → {new_id}")
    print(f"{'='*60}\n")

    # Check what we're migrating
    tables = ['conversations', 'business_context', 'decisions', 'agent_state']

    for table in tables:
        try:
            result = db.execute_query(
                f"SELECT COUNT(*) as count FROM {table} WHERE entrepreneur_id = ?",
                (old_id,)
            )
            count = result[0]['count'] if result else 0
            print(f"  {table}: {count} records")
        except Exception as e:
            print(f"  {table}: No records (table may be empty)")

    print()

    # Confirm migration
    response = input(f"Proceed with migration to UUID {new_id}? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("\nMigration cancelled.")
        return False

    print("\nMigrating...")

    # Perform migration for each table
    migrated_counts = {}
    for table in tables:
        try:
            # Update entrepreneur_id to new UUID
            db.execute_update(
                f"UPDATE {table} SET entrepreneur_id = ? WHERE entrepreneur_id = ?",
                (new_id, old_id)
            )

            # Count what was migrated
            result = db.execute_query(
                f"SELECT COUNT(*) as count FROM {table} WHERE entrepreneur_id = ?",
                (new_id,)
            )
            count = result[0]['count'] if result else 0
            migrated_counts[table] = count
            print(f"  ✓ {table}: {count} records migrated")

        except Exception as e:
            print(f"  ✗ {table}: Error - {e}")

    print(f"\n{'='*60}")
    print("MIGRATION COMPLETE")
    print(f"{'='*60}")
    print(f"\nNew Entrepreneur ID: {new_id}")
    print(f"\nTotal migrated:")
    for table, count in migrated_counts.items():
        print(f"  - {table}: {count} records")

    print(f"\n⚠️  IMPORTANT: Update your .env file:")
    print(f"   ENTREPRENEUR_ID={new_id}")
    print()

    return True


def update_env_file(env_path: str, new_id: str):
    """
    Update .env file with new UUID.

    Args:
        env_path: Path to .env file
        new_id: New UUID to set
    """
    env_file = Path(env_path)

    if not env_file.exists():
        print(f"\n⚠️  Warning: {env_path} not found")
        return

    # Read current .env
    with open(env_file, 'r') as f:
        lines = f.readlines()

    # Update ENTREPRENEUR_ID line
    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith('ENTREPRENEUR_ID='):
            lines[i] = f'ENTREPRENEUR_ID={new_id}\n'
            updated = True
            break

    # If not found, add it
    if not updated:
        lines.append(f'\nENTREPRENEUR_ID={new_id}\n')

    # Write back
    with open(env_file, 'w') as f:
        f.writelines(lines)

    print(f"✓ Updated {env_path}")


def main():
    """Main migration entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate entrepreneur ID to UUID"
    )
    parser.add_argument(
        '--old-id',
        type=str,
        required=True,
        help='Current entrepreneur ID to migrate (e.g., default_user)'
    )
    parser.add_argument(
        '--new-id',
        type=str,
        help='Specific UUID to migrate to (optional, will generate if not provided)'
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Auto-generate UUID and skip confirmation'
    )
    parser.add_argument(
        '--update-env',
        action='store_true',
        help='Automatically update .env file with new UUID'
    )

    args = parser.parse_args()

    try:
        # Load config
        config = Config()

        # Initialize database
        db = DatabaseAdapter(
            connection_string=config.get_database_connection_string(),
            db_type=config.database_type
        )

        # Generate or use provided UUID
        new_id = args.new_id or generate_uuid()

        # Validate UUID format
        try:
            uuid.UUID(new_id)
        except ValueError:
            print(f"Error: '{new_id}' is not a valid UUID")
            sys.exit(1)

        # Perform migration
        success = migrate_entrepreneur_id(db, args.old_id, new_id)

        if success and args.update_env:
            # Find .env file (assume it's in entre_agents directory)
            env_path = Path(__file__).parent.parent.parent / '.env'
            update_env_file(str(env_path), new_id)

        if success:
            print("\n✓ Migration successful!")
            print(f"\nYour new entrepreneur ID is: {new_id}")
            print("\nNext steps:")
            if not args.update_env:
                print(f"1. Update your .env file: ENTREPRENEUR_ID={new_id}")
            print(f"2. Restart the CLI: python3 src/cli.py")
            print("3. Your conversation history will be preserved!")

    except Exception as e:
        print(f"\nError during migration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

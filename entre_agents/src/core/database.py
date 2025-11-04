"""
Database abstraction layer for VEntre agents.
Supports both SQLite (local) and PostgreSQL (cloud) with the same interface.
"""

import sqlite3
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json


class DatabaseAdapter:
    """
    Database-agnostic adapter that works with SQLite or PostgreSQL.
    Provides consistent interface for all database operations.
    """

    def __init__(self, connection_string: str, db_type: str = "sqlite"):
        """
        Initialize database connection.

        Args:
            connection_string: For SQLite: file path. For PostgreSQL: connection URL
            db_type: "sqlite" or "postgresql"
        """
        self.db_type = db_type
        self.connection_string = connection_string
        self.conn = None
        self._connect()
        self._initialize_schema()

    def _connect(self):
        """Establish database connection."""
        if self.db_type == "sqlite":
            self.conn = sqlite3.connect(self.connection_string, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dicts
        elif self.db_type == "postgresql":
            try:
                import psycopg2
                from psycopg2.extras import RealDictCursor
                self.conn = psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
            except ImportError:
                raise ImportError("PostgreSQL support requires psycopg2: pip install psycopg2-binary")
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def _initialize_schema(self):
        """Create necessary tables if they don't exist."""

        # Conversations table - stores all message history
        self.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entrepreneur_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ if self.db_type == "sqlite" else """
            CREATE TABLE IF NOT EXISTS conversations (
                id SERIAL PRIMARY KEY,
                entrepreneur_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Business context table - stores current state
        self.execute("""
            CREATE TABLE IF NOT EXISTS business_context (
                entrepreneur_id TEXT PRIMARY KEY,
                business_phase TEXT,
                cognitive_state TEXT,
                strategic_convictions TEXT,
                goals TEXT,
                constraints TEXT,
                metadata TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ if self.db_type == "sqlite" else """
            CREATE TABLE IF NOT EXISTS business_context (
                entrepreneur_id TEXT PRIMARY KEY,
                business_phase TEXT,
                cognitive_state TEXT,
                strategic_convictions JSONB,
                goals JSONB,
                constraints JSONB,
                metadata JSONB,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Decisions table - tracks major decisions
        self.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entrepreneur_id TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                description TEXT NOT NULL,
                rationale TEXT,
                agents_consulted TEXT,
                outcome TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ if self.db_type == "sqlite" else """
            CREATE TABLE IF NOT EXISTS decisions (
                id SERIAL PRIMARY KEY,
                entrepreneur_id TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                description TEXT NOT NULL,
                rationale TEXT,
                agents_consulted JSONB,
                outcome TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Agent state table - tracks specialist agent states
        self.execute("""
            CREATE TABLE IF NOT EXISTS agent_state (
                entrepreneur_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                state_data TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (entrepreneur_id, agent_name)
            )
        """ if self.db_type == "sqlite" else """
            CREATE TABLE IF NOT EXISTS agent_state (
                entrepreneur_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                state_data JSONB,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (entrepreneur_id, agent_name)
            )
        """)

        self.commit()

    def execute(self, query: str, params: tuple = None) -> Any:
        """Execute a query and return cursor."""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def fetchone(self, query: str, params: tuple = None) -> Optional[Dict]:
        """Execute query and fetch one result as dictionary."""
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        if row:
            return dict(row) if self.db_type == "sqlite" else row
        return None

    def fetchall(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute query and fetch all results as list of dictionaries."""
        cursor = self.execute(query, params)
        rows = cursor.fetchall()
        if self.db_type == "sqlite":
            return [dict(row) for row in rows]
        return rows

    def commit(self):
        """Commit current transaction."""
        self.conn.commit()

    def rollback(self):
        """Rollback current transaction."""
        self.conn.rollback()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    # Helper methods for common operations

    def save_message(self, entrepreneur_id: str, agent_name: str, role: str,
                     content: str, metadata: Dict = None):
        """Save a conversation message."""
        metadata_json = json.dumps(metadata) if metadata else None
        self.execute(
            """INSERT INTO conversations
               (entrepreneur_id, agent_name, role, content, metadata)
               VALUES (?, ?, ?, ?, ?)""" if self.db_type == "sqlite" else
            """INSERT INTO conversations
               (entrepreneur_id, agent_name, role, content, metadata)
               VALUES (%s, %s, %s, %s, %s)""",
            (entrepreneur_id, agent_name, role, content, metadata_json)
        )
        self.commit()

    def get_conversation_history(self, entrepreneur_id: str, agent_name: str = None,
                                 limit: int = 100) -> List[Dict]:
        """Get conversation history for an entrepreneur."""
        if agent_name:
            query = """SELECT * FROM conversations
                      WHERE entrepreneur_id = ? AND agent_name = ?
                      ORDER BY created_at DESC LIMIT ?""" if self.db_type == "sqlite" else \
                   """SELECT * FROM conversations
                      WHERE entrepreneur_id = %s AND agent_name = %s
                      ORDER BY created_at DESC LIMIT %s"""
            return self.fetchall(query, (entrepreneur_id, agent_name, limit))
        else:
            query = """SELECT * FROM conversations
                      WHERE entrepreneur_id = ?
                      ORDER BY created_at DESC LIMIT ?""" if self.db_type == "sqlite" else \
                   """SELECT * FROM conversations
                      WHERE entrepreneur_id = %s
                      ORDER BY created_at DESC LIMIT %s"""
            return self.fetchall(query, (entrepreneur_id, limit))

    def get_business_context(self, entrepreneur_id: str) -> Optional[Dict]:
        """Get current business context for an entrepreneur."""
        query = """SELECT * FROM business_context WHERE entrepreneur_id = ?""" \
                if self.db_type == "sqlite" else \
                """SELECT * FROM business_context WHERE entrepreneur_id = %s"""
        return self.fetchone(query, (entrepreneur_id,))

    def update_business_context(self, entrepreneur_id: str, **kwargs):
        """Update business context fields."""
        # Convert dicts to JSON for SQLite
        if self.db_type == "sqlite":
            for key in ['strategic_convictions', 'goals', 'constraints', 'metadata']:
                if key in kwargs and isinstance(kwargs[key], dict):
                    kwargs[key] = json.dumps(kwargs[key])

        # Build update query dynamically
        fields = ', '.join([f"{k} = ?" if self.db_type == "sqlite" else f"{k} = %s"
                           for k in kwargs.keys()])
        query = f"""INSERT INTO business_context (entrepreneur_id, {', '.join(kwargs.keys())})
                   VALUES (?, {', '.join(['?'] * len(kwargs))})
                   ON CONFLICT(entrepreneur_id) DO UPDATE SET {fields}, updated_at = CURRENT_TIMESTAMP""" \
                if self.db_type == "sqlite" else \
                f"""INSERT INTO business_context (entrepreneur_id, {', '.join(kwargs.keys())})
                   VALUES (%s, {', '.join(['%s'] * len(kwargs))})
                   ON CONFLICT(entrepreneur_id) DO UPDATE SET {fields}, updated_at = CURRENT_TIMESTAMP"""

        params = (entrepreneur_id,) + tuple(kwargs.values()) + tuple(kwargs.values())
        self.execute(query, params)
        self.commit()

    def save_decision(self, entrepreneur_id: str, decision_type: str, description: str,
                     rationale: str = None, agents_consulted: List[str] = None,
                     outcome: str = None) -> int:
        """Save a decision record."""
        agents_json = json.dumps(agents_consulted) if agents_consulted else None
        self.execute(
            """INSERT INTO decisions
               (entrepreneur_id, decision_type, description, rationale, agents_consulted, outcome)
               VALUES (?, ?, ?, ?, ?, ?)""" if self.db_type == "sqlite" else
            """INSERT INTO decisions
               (entrepreneur_id, decision_type, description, rationale, agents_consulted, outcome)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (entrepreneur_id, decision_type, description, rationale, agents_json, outcome)
        )
        self.commit()
        return self.conn.cursor().lastrowid if self.db_type == "sqlite" else \
               self.conn.cursor().fetchone()['id']

    def get_agent_state(self, entrepreneur_id: str, agent_name: str) -> Optional[Dict]:
        """Get state data for a specific agent."""
        query = """SELECT state_data FROM agent_state
                  WHERE entrepreneur_id = ? AND agent_name = ?""" \
                if self.db_type == "sqlite" else \
                """SELECT state_data FROM agent_state
                  WHERE entrepreneur_id = %s AND agent_name = %s"""
        result = self.fetchone(query, (entrepreneur_id, agent_name))
        if result and result.get('state_data'):
            return json.loads(result['state_data']) if self.db_type == "sqlite" else result['state_data']
        return None

    def update_agent_state(self, entrepreneur_id: str, agent_name: str, state_data: Dict):
        """Update state data for a specific agent."""
        state_json = json.dumps(state_data) if self.db_type == "sqlite" else state_data
        query = """INSERT INTO agent_state (entrepreneur_id, agent_name, state_data)
                  VALUES (?, ?, ?)
                  ON CONFLICT(entrepreneur_id, agent_name)
                  DO UPDATE SET state_data = ?, updated_at = CURRENT_TIMESTAMP""" \
                if self.db_type == "sqlite" else \
                """INSERT INTO agent_state (entrepreneur_id, agent_name, state_data)
                  VALUES (%s, %s, %s)
                  ON CONFLICT(entrepreneur_id, agent_name)
                  DO UPDATE SET state_data = %s, updated_at = CURRENT_TIMESTAMP"""
        self.execute(query, (entrepreneur_id, agent_name, state_json, state_json))
        self.commit()

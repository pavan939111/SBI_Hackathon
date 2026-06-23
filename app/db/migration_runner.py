"""
Database Migrations Runner executing SQL files on DB initialization.
"""
import os
import logging
from sqlalchemy import text
from app.db.postgres import engine

logger = logging.getLogger("banksaathi.migrations")

async def run_migrations() -> None:
    """
    Finds and executes all SQL migration files located in app/db/migrations/
    in alphabetical order.
    """
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
    if not os.path.exists(migrations_dir):
        logger.warning(f"Migrations directory not found at {migrations_dir}")
        return

    # Gather and sort all SQL files
    sql_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith(".sql")])
    if not sql_files:
        logger.info("No SQL migration files found to execute.")
        return

    logger.info(f"Starting migrations runner. Found {len(sql_files)} file(s).")

    async with engine.begin() as conn:
        for file_name in sql_files:
            file_path = os.path.join(migrations_dir, file_name)
            logger.info(f"Executing migration: {file_name}")
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    sql_content = f.read()

                # Split statements by semicolon, filtering out empty ones
                statements = [
                    stmt.strip() for stmt in sql_content.split(";") if stmt.strip()
                ]

                for statement in statements:
                    # Execute each block
                    await conn.execute(text(statement))
                    
                logger.info(f"Finished executing: {file_name}")
            except Exception as e:
                logger.error(f"Migration execution failed for file {file_name}: {e}")
                raise e

    logger.info("Database migrations run completed successfully.")

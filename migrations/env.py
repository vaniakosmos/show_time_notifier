import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, dirname(dirname(abspath(__file__))))  # add root
from core.settings import DATABASE_URL
from core.db import Model


config = context.config
fileConfig(config.config_file_name)
target_metadata = Model.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(url=DATABASE_URL, target_metadata=target_metadata,
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    conf = config.get_section(config.config_ini_section)
    conf['sqlalchemy.url'] = DATABASE_URL
    connectable = engine_from_config(
        conf, prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

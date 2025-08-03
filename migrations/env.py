import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from src.api.models.base import Base
from src.api.models.exercises import Exercise  # noqa: F401
from src.api.models.plan_feedback import PlanFeedback  # noqa: F401
from src.api.models.session_exercises import SessionExercises  # noqa: F401
from src.api.models.user_profiles import UserProfile  # noqa: F401
from src.api.models.users import User  # noqa: F401
from src.api.models.workout_plans import WorkoutPlans  # noqa: F401
from src.api.models.workout_sessions import WorkoutSession  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

target_metadata = Base.metadata

# Get environment
env = os.getenv("ENV", "dev")

# Load .env only in non-test environments
if env != "test":
    import dotenv

    dotenv.load_dotenv()


# Use DATABASE_URL if available, otherwise construct from components
db_url = os.getenv("DATABASE_URL")
if not db_url:
    db_username = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_url = f"postgresql://{db_username}:{db_password}@{db_host}:5432/{db_name}"

config.set_main_option("sqlalchemy.url", db_url)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = config.get_main_option("sqlalchemy.url")
    engine = create_engine(url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

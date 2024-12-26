from logging.config import fileConfig
from pathlib import Path
from profile.settings import ApplicationSettings

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from yarl import URL

from alembic import context

alembic_config = context.config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)


def get_app_paths_map() -> dict[str, str]:
    bases = context.script.get_bases()
    mapper = {}
    for index, base_revision_hash in enumerate(bases):
        base_revision = context.script.get_revision(base_revision_hash)
        mapper["".join(base_revision.branch_labels)] = str(
            Path(context.script.version_locations[index]).parents[0]
        )
    return mapper


def load_app_models(app_path: str):
    pass


app_path_map = get_app_paths_map()
app_settings = ApplicationSettings()
alembic_config.set_main_option(
    "sqlalchemy.url",
    str(
        URL.build(
            scheme="postgresql+psycopg2",
            user=app_settings.db.username,
            password=app_settings.db.password.get_secret_value(),
            host=app_settings.db.host,
            port=app_settings.db.port,
            path="/" + app_settings.db.name,
        )
    ),
)
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run alembic in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run alembic in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

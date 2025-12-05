from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.mark.asyncio
async def test_5d_command_sends_embed():
    """Testet das `!5d` Kommando: erwartet einen gesendeten Embed.
    Hinweis: Dieser Test setzt voraus, dass der Bot ein Command `5d` registriert hat
    und `ctx.send(embed=...)` verwendet.
    """
    # Modulname beginnt mit Ziffer, daher via importlib über Pfad laden
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    # Bot und Command ermitteln
    bot = getattr(bot_module, "bot", None)
    assert bot is not None, "Bot-Instanz `bot` fehlt in 5d_discord_bot.py"
    cmd = bot.get_command("5d")
    assert cmd is not None, "Command `5d` nicht gefunden"

    # Kontext mocken
    ctx = MagicMock()
    ctx.send = AsyncMock()

    # Command aufrufen
    await cmd.callback(ctx)

    # Assertions: send wurde mit embed aufgerufen
    assert ctx.send.called, "ctx.send wurde nicht aufgerufen"
    kwargs = ctx.send.call_args[1]
    embed = kwargs.get("embed")
    assert embed is not None, "Embed wurde nicht übergeben"

    # Weiche Validierung: Beschreibung/Fields vorhanden
    desc = getattr(embed, "description", "")
    assert isinstance(desc, str)


@pytest.mark.asyncio
async def test_embed_structure_is_present():
    """Validiert nur die Struktur: Embed vorhanden, Titel/Description Strings."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, "bot", None)
    assert bot is not None
    cmd = bot.get_command("5d")
    assert cmd is not None

    ctx = MagicMock()
    ctx.send = AsyncMock()

    await cmd.callback(ctx)

    kwargs = ctx.send.call_args[1]
    embed = kwargs.get("embed")
    assert embed is not None
    # Minimale Strukturvalidierung
    assert isinstance(getattr(embed, "title", ""), str)
    assert isinstance(getattr(embed, "description", ""), str)


@pytest.mark.asyncio
async def test_help_command_exists():
    """Testet ob das `!help` Kommando existiert."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, "bot", None)
    assert bot is not None
    # Help command is built-in or custom
    assert bot.help_command is not None or bot.get_command("help") is not None


@pytest.mark.asyncio
async def test_stats_command_sends_message():
    """Testet das `!stats` Kommando falls vorhanden."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, "bot", None)
    assert bot is not None
    cmd = bot.get_command("stats")

    if cmd is None:
        pytest.skip("Command `stats` nicht implementiert")

    ctx = MagicMock()
    ctx.send = AsyncMock()

    await cmd.callback(ctx)
    assert ctx.send.called, "ctx.send wurde nicht aufgerufen"


@pytest.mark.asyncio
async def test_project_command_sends_message():
    """Testet das `!project` Kommando falls vorhanden."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, "bot", None)
    assert bot is not None
    cmd = bot.get_command("project")

    if cmd is None:
        pytest.skip("Command `project` nicht implementiert")

    ctx = MagicMock()
    ctx.send = AsyncMock()

    await cmd.callback(ctx)
    assert ctx.send.called, "ctx.send wurde nicht aufgerufen"


@pytest.mark.asyncio
async def test_embed_contains_imp_score():
    """Testet ob der Embed IMP-bezogene Informationen enthält."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, "bot", None)
    cmd = bot.get_command("5d")
    assert cmd is not None

    ctx = MagicMock()
    ctx.send = AsyncMock()

    await cmd.callback(ctx)

    kwargs = ctx.send.call_args[1]
    embed = kwargs.get("embed")
    assert embed is not None

    # Check if IMP-related keywords are present
    embed_text = str(getattr(embed, "description", "")).lower()
    embed_title = str(getattr(embed, "title", "")).lower()

    has_imp_content = (
        "imp" in embed_text
        or "imp" in embed_title
        or "autonomie" in embed_text
        or "motivation" in embed_text
        or "resilienz" in embed_text
        or "partizipation" in embed_text
    )

    assert has_imp_content, "Embed sollte IMP-bezogene Inhalte enthalten"


def test_bot_module_can_be_imported():
    """Testet ob das Bot-Modul importiert werden kann."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")

    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    assert spec is not None
    assert spec.loader is not None

    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)  # type: ignore

    # Check for essential attributes
    assert hasattr(bot_module, "bot"), "Bot-Instanz fehlt"


def test_bot_has_commands():
    """Testet ob der Bot Commands registriert hat."""
    import importlib.util
    import pathlib

    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")

    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, "bot", None)
    assert bot is not None

    # Check for at least one command
    commands = list(bot.commands)
    assert len(commands) > 0, "Bot sollte mindestens ein Command haben"

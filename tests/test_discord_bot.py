import pytest
from unittest.mock import MagicMock, AsyncMock

@pytest.mark.asyncio
async def test_5d_command_sends_embed():
    """Testet das `!5d` Kommando: erwartet einen gesendeten Embed.
    Hinweis: Dieser Test setzt voraus, dass der Bot ein Command `5d` registriert hat
    und `ctx.send(embed=...)` verwendet.
    """
    # Modulname beginnt mit Ziffer, daher via importlib über Pfad laden
    import importlib.util, sys, pathlib
    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    # Bot und Command ermitteln
    bot = getattr(bot_module, 'bot', None)
    assert bot is not None, "Bot-Instanz `bot` fehlt in 5d_discord_bot.py"
    cmd = bot.get_command('5d')
    assert cmd is not None, "Command `5d` nicht gefunden"

    # Kontext mocken
    ctx = MagicMock()
    ctx.send = AsyncMock()

    # Command aufrufen
    await cmd.callback(ctx)

    # Assertions: send wurde mit embed aufgerufen
    assert ctx.send.called, "ctx.send wurde nicht aufgerufen"
    kwargs = ctx.send.call_args[1]
    embed = kwargs.get('embed')
    assert embed is not None, "Embed wurde nicht übergeben"

    # Weiche Validierung: Beschreibung/Fields vorhanden
    desc = getattr(embed, 'description', '')
    assert isinstance(desc, str)

@pytest.mark.asyncio
async def test_embed_structure_is_present():
    """Validiert nur die Struktur: Embed vorhanden, Titel/Description Strings."""
    import importlib.util, sys, pathlib
    bot_path = pathlib.Path(__file__).resolve().parent.parent / "5d_discord_bot.py"
    if not bot_path.exists():
        pytest.skip("5d_discord_bot.py nicht gefunden")
    spec = importlib.util.spec_from_file_location("five_d_discord_bot", str(bot_path))
    bot_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(bot_module)  # type: ignore

    bot = getattr(bot_module, 'bot', None)
    assert bot is not None
    cmd = bot.get_command('5d')
    assert cmd is not None

    ctx = MagicMock()
    ctx.send = AsyncMock()

    await cmd.callback(ctx)

    kwargs = ctx.send.call_args[1]
    embed = kwargs.get('embed')
    assert embed is not None
    # Minimale Strukturvalidierung
    assert isinstance(getattr(embed, 'title', ''), str)
    assert isinstance(getattr(embed, 'description', ''), str)

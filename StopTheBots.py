# ba_meta require api 9
from __future__ import annotations

import random
import bascenev1 as bs
import babase
import bauiv1 as bui

from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.actor.spazbot import (
    SpazBotSet,
    BomberBot,
    BomberBotPro,
    BrawlerBot,
    ChargerBot,
    TriggerBot,
)
from bascenev1lib.maps.football import FootballStadium


# ba_meta export game
class StopTheBots(bs.CoopGameActivity[bs.Player, bs.Team]):

    name = "Stop The Bots"
    description = "Sobrevive a las oleadas de bots."

    @classmethod
    def get_supported_maps(cls) -> list[str]:
        return ["Football Stadium"]

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.CoopSession)

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._bots = SpazBotSet()
        self._scoreboard = Scoreboard()
        self._wave = 0

    def on_begin(self) -> None:
        super().on_begin()
        self._start_wave()

    def _start_wave(self) -> None:
        self._wave += 1
        self._spawn_wave()
        bs.timer(8.0, self._start_wave)

    def _spawn_wave(self) -> None:
        bot_types = [
            BomberBot,
            BomberBotPro,
            BrawlerBot,
            ChargerBot,
            TriggerBot,
        ]

        for _ in range(self._wave + 2):
            bot_type = random.choice(bot_types)
            pos = (random.uniform(-5, 5), 1, random.uniform(-3, 3))
            self._bots.spawn_bot(bot_type, pos=pos)

    def handlemessage(self, msg: bs.Message) -> None:
        super().handlemessage(msg)


# ba_meta export plugin
class StopBotsPlugin(babase.Plugin):

    def on_app_running(self) -> None:
        classic = babase.app.classic
        if classic is None:
            return

        classic.add_coop_practice_level(
            bs.Level(
                name="Stop The Bots",
                gametype=StopTheBots,
                settings={},
                preview_texture_name="footballStadiumPreview",
            )
        )
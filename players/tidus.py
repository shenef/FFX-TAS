import logging

import battle
import memory
import xbox
from players.base import Player

logger = logging.getLogger(__name__)


class TidusImpl(Player):
    def __init__(self):
        super().__init__("Tidus", 0, [0, 19, 20, 22, 1])

    def overdrive(self, direction=None, version: int = 0, character=99):
        while not memory.main.other_battle_menu():
            xbox.tap_left()
        while not memory.main.interior_battle_menu():
            xbox.tap_b()
        battle.main._navigate_to_position(
            version, battle_cursor=memory.main.battle_cursor_3
        )
        while memory.main.interior_battle_menu():
            xbox.tap_b()
        if character != 99 and memory.main.get_enemy_current_hp()[character - 20] != 0:
            while (
                character != memory.main.battle_target_id()
                and memory.main.get_enemy_current_hp()[character - 20] != 0
            ):
                xbox.tap_left()
        elif direction:
            if direction == "left":
                xbox.tap_left()
        while not self.overdrive_active():
            xbox.tap_b()
        memory.main.wait_frames(12)
        xbox.tap_b()  # First try pog
        logger.info("Hit Overdrive")

    def overdrive_active(self):
        return memory.main.read_val(0x00F3D6F4, 1) == 4


Tidus = TidusImpl()

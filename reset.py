import datetime
import logging

import logs
import memory.main
import vars
import xbox
from memory.main import battle_wrap_up_active, turn_ready, user_control

logger = logging.getLogger(__name__)
game_vars = vars.vars_handle()

FFXC = xbox.controller_handle()


def mid_run_reset(land_run: bool = False, start_time=datetime.datetime.now()):
    if land_run:
        end_time = logs.time_stamp()
        total_time = end_time - start_time
        logs.write_stats("Total time:")
        logs.write_stats(str(total_time))
        logger.info(f"The game duration was: {total_time}")
        logger.info(
            "This duration is intended for comparison reference only, "
            + "not as a true timer."
        )
        logger.info("Please do not use this as your submitted time.")
        memory.main.wait_frames(30)
        logger.info("--------")
        logger.info("In order to conform with speedrun standards,")
        memory.main.wait_frames(60)
        logger.info("we now wait until the end of the credits and stuff")
        memory.main.wait_frames(60)
        logger.info("and then will open up the list of saves.")
        memory.main.wait_frames(60)
        logger.info(
            "This will show the autosave values, which conforms to the speedrun rules."
        )
        # Bring up auto-save
        while memory.main.get_map() != 23:
            if memory.main.get_map() in [348, 349]:
                xbox.tap_start()
            elif memory.main.cutscene_skip_possible():
                xbox.skip_scene()
        memory.main.wait_frames(180)
        while not memory.main.save_menu_open():
            xbox.tap_b()
        memory.main.wait_frames(180)
        xbox.menu_a()
        xbox.menu_a()
        xbox.menu_a()
    else:
        memory.main.wait_frames(60)
        reset_to_main_menu()

    # Now to re-start
    game_vars.set_start_vars()
    rng_seed = memory.main.rng_seed()
    if land_run:
        rng_seed += 0
        if rng_seed == 256:
            rng_seed = 0
    logs.reset_stats_log()
    logs.next_stats(rng_seed)  # Start next stats file
    if game_vars.rng_mode() in ["set", "preferred"]:
        memory.main.set_rng_seed(rng_seed)
    logger.info(f"This run will be using RNG seed: {rng_seed}")
    logs.next_stats(rng_seed)
    logs.write_stats("RNG seed:")
    logs.write_stats(rng_seed)
    gamestate = "none"
    step_counter = 1

    return gamestate, step_counter


def _attempt_reset():
    memory.main.wait_frames(30 * 0.07)
    if memory.main.s_grid_active():
        logger.debug("Reset: S-grid open")
        from menu_grid import (
            first_position,
            move_active,
            move_complete,
            move_ready,
            move_use_menu,
            quit_grid_ready,
            ready_select_sphere,
            ready_use_sphere,
            use_ready,
        )

        while memory.main.s_grid_active():
            if ready_use_sphere():
                logger.debug("Using the current item.")
                xbox.menu_b()
            elif first_position():
                logger.debug("Opening the Quit menu")
                xbox.menu_a()
            elif quit_grid_ready():
                logger.debug("quitting sphere grid")
                xbox.menu_b()
            elif (
                move_use_menu()
                or move_ready()
                or move_active()
                or move_complete()
                or use_ready()
                or ready_select_sphere()
            ):
                xbox.menu_a()
        while memory.main.menu_number() != 5:
            pass
    if memory.main.game_over():
        logger.debug("Reset: game over")
        while memory.main.get_map() not in [23, 62, 348, 349]:
            xbox.tap_b()
            return
    if battle_wrap_up_active():
        logger.debug("Reset: end of battle")
        while battle_wrap_up_active():
            xbox.menu_b()
    if memory.main.menu_open():
        logger.debug("Reset: menu open")
        memory.main.close_menu()
    while not (user_control() or turn_ready()) and memory.main.get_map() not in [
        23,
        62,
        348,
        349,
    ]:
        xbox.tap_a()

    while memory.main.get_map() not in [23, 348, 349]:
        logger.info("Attempting reset")
        logger.info(f"FFX map: {memory.main.get_map()}")
        memory.main.set_map_reset()
        memory.main.wait_frames(30 * 0.1)
        memory.main.force_map_load()
        memory.main.wait_frames(30 * 1)


def reset_to_main_menu():
    FFXC.set_neutral()
    if memory.main.get_story_progress() <= 8:
        _attempt_reset()
    elif memory.main.battle_active():
        logger.info("Battle is active. Forcing battle to end so we can soft reset.")
        while not memory.main.turn_ready():
            xbox.menu_a()
        memory.main.reset_battle_end()
        while memory.main.get_map() not in [23, 348, 349]:
            xbox.menu_b()

    else:
        _attempt_reset()
    logger.info("Resetting")


def reset_no_battles():
    memory.main.wait_frames(90)
    while not (user_control() or turn_ready()) and memory.main.get_map() not in [
        23,
        62,
        348,
        349,
    ]:
        xbox.tap_a()

    while memory.main.get_map() not in [23, 348, 349]:
        logger.info("Attempting reset")
        logger.info(f"FFX map: {memory.main.get_map()}")
        memory.main.set_map_reset()
        memory.main.wait_frames(30 * 0.1)
        memory.main.force_map_load()
        memory.main.wait_frames(30 * 1)

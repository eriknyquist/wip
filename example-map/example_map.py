import example_map_rooms as rooms

import text_game_maker
from text_game_maker.crafting import crafting
from text_game_maker.tile import tile
from text_game_maker.utils import utils, runner
from text_game_maker.utils.utils import serializable_callback

# If player is still locked in the starting room and does not yet have the
# lighter equipped, give them a hint
@serializable_callback
def lighter_equip_hint(player, turns):
    # No need for a hint if player has already gotten out, or equipped lighter
    if (player.current.tile_id != rooms.startingcell_id) or player.can_see():
        return

    # No need for a hint if player has already unlocked the cell door but is
    # still/back in the cell with no light source for some reason
    if ((not player.current.east.is_door())
            or (not player.current.east.locked)):
        return

    utils._wrap_print("Hint: say things like 'pockets', 'inventory', or just "
        "'i' to show your inventory")
    utils._wrap_print("Hint: say things like 'use lighter' or 'equip lighter' "
        "to use the lighter as a light source")

@serializable_callback
def light_source_decay_callback(player, turns):
    if player.equipped and player.equipped.is_light_source:
        player.equipped.decrement_fuel()

    player.schedule_task(light_source_decay_callback, 1)

# Called when the game starts
def on_game_run(player):
    # read name from player
    player.read_player_name_and_set()
    player.schedule_task(light_source_decay_callback, 1)
    player.schedule_task(lighter_equip_hint, 10)

class ExampleMapRunner(runner.MapRunner):
    def build_map(self, builder):
        # Build starting cell
        rooms.prison_starting_cell(builder)

        # Build prison entrance
        builder.move_east()
        rooms.prison_entrance_hall(builder)

        # Build prison_hallway
        builder.move_south()
        rooms.prison_hallway(builder)

        # Build other cell
        builder.move_south()
        rooms.other_cell(builder)

        # Build prison yard
        builder.move_north()
        builder.move_west()
        rooms.prison_yard(builder)

        # Build prison office
        builder.move_east()
        builder.move_north(2)
        rooms.prison_office(builder)

        # Build alleyway
        builder.move_south()
        builder.move_east()
        rooms.prison_alleyway(builder)

        # Build pawn shop
        builder.move_east()
        rooms.pawn_shop(builder)

        # Set the input prompt
        builder.set_input_prompt(" > ")

        # Set on_game_run callback to get player's name
        builder.set_on_game_run(on_game_run)

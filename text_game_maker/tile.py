import text_game_maker as gamemaker

class Tile(object):
    """
    Represents a single 'tile' or 'room' in the game
    """

    def __init__(self, name=None, description=None, on_enter=None,
            on_exit=None):
        """
        Initialise a Tile instance

        :param str name: short description, e.g. "a dark cellar"
        :param str description: long description, printed when player enters\
            the room e.g. "a dark, scary cellar with blah blah blah... "
        :param on_enter: callback to be invoked when player attempts to enter\
            this tile (see documentation for\
            text_game_maker.map_builder.MapBuilder.set_on_enter()
        :param on_exit: callback to be invoked when player attempts to exit\
            this tile (see documentation for\
            text_game_maker.map_builder.MapBuilder.set_on_exit()
        """

        self.name = name
        if description:
            self.description = gamemaker._remove_leading_whitespace(description)

        # If tile is locked, player will only see a locked door.
        self.locked = False

        # Adjacent tiles to the north, south, east and west of this tile
        self.north = None
        self.south = None
        self.east = None
        self.west = None

        # Items on this tile
        self.items = []

        # People on this tile
        self.people = []

        # Enter/exit callbacks
        self.on_enter = on_enter
        self.on_exit = on_exit

    def _get_name(self, tile, name):
        if tile:
            if tile.locked:
                msg = "a locked door"
            else:
                msg = tile.name

            return "to the %s is %s" % (name, msg)
        else:
            return None

    def summary(self):
        """
        Return a description of all available directions from this tile
        """

        ret = []

        north = self._get_name(self.north, 'north')
        south = self._get_name(self.south, 'south')
        east = self._get_name(self.east, 'east')
        west = self._get_name(self.west, 'west')

        if north: ret.append(north)
        if south: ret.append(south)
        if east: ret.append(east)
        if west: ret.append(west)

        return '\n'.join(ret)

    def is_locked(self):
        """
        Returns true/false indicating whether this tile is locked.
        :return: True if tile is locked, False if unlocked.
        :rtype: bool
        """

        return self.locked

    def set_locked(self):
        """
        Lock this tile-- player will only see a locked door
        """

        self.locked = True

    def set_unlocked(self):
        """
        Unlock this tile-- player can enter normally
        """

        self.locked = False

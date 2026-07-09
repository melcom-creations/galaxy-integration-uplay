import logging as log
from consts import UBISOFT_CONFIGURATIONS_BLACKLISTED_NAMES
from definitions import GameStatus, GameType


STATUS_PRIORITY = {
    GameStatus.Unknown: 0,
    GameStatus.NotInstalled: 1,
    GameStatus.Installed: 2,
    GameStatus.Running: 3,
}


class GamesCollection(list):

    @staticmethod
    def _status_rank(status):
        return STATUS_PRIORITY.get(status, -1)

    @staticmethod
    def _has_useful_name(game):
        if not game.name:
            return False
        if game.name.lower() in UBISOFT_CONFIGURATIONS_BLACKLISTED_NAMES:
            return False
        if game.name.startswith("steam_linked_"):
            return False
        return True

    def _copy_preferred_metadata(self, target, source):
        if source.space_id:
            target.space_id = source.space_id
        if source.install_id:
            target.install_id = source.install_id
        if source.launch_id:
            target.launch_id = source.launch_id
        if source.path:
            target.path = source.path
        if source.special_registry_path:
            target.special_registry_path = source.special_registry_path
        if source.exe:
            target.exe = source.exe
        if source.third_party_id:
            target.third_party_id = source.third_party_id
        if source.type and target.type != GameType.Steam:
            target.type = source.type
        if self._has_useful_name(source) or not self._has_useful_name(target):
            if source.name:
                target.name = source.name

    def _should_replace_metadata(self, current, incoming):
        if self._status_rank(incoming.status) > self._status_rank(current.status):
            return True

        if current.space_id and incoming.space_id and current.space_id == incoming.space_id:
            if current.type == GameType.Steam and incoming.type != GameType.Steam:
                if self._has_useful_name(incoming) and not self._has_useful_name(current):
                    return True
                if incoming.install_id and incoming.launch_id and incoming.install_id == incoming.launch_id:
                    return True

        if self._has_useful_name(incoming) and not self._has_useful_name(current):
            return True

        return False

    def get_local_games(self):
        local_games = []
        for game in self:
            if game.status in [GameStatus.Installed, GameStatus.Running]:
                local_games.append(game)
        return local_games

    def append(self, _):
        raise AssertionError('Method not available. Use extend')

    def _extend_existing_game_entry(self, game):
        for game_in_list in self:
            if (game.space_id and game.space_id == game_in_list.space_id) or (game.install_id and game.install_id == game_in_list.install_id) or \
                    (game.launch_id and game.launch_id == game_in_list.launch_id):
                if self._should_replace_metadata(game_in_list, game):
                    log.debug(f"Extending existing game entry {game_in_list} with preferred metadata from {game}")
                    self._copy_preferred_metadata(game_in_list, game)
                if game.install_id and game.launch_id and game.install_id != game.launch_id and (game_in_list.install_id == game_in_list.launch_id):
                    log.debug(f"Extending existing game entry {game_in_list} with more specific install/launch id launch id: {game.launch_id} and install id: {game.install_id}")
                    game_in_list.install_id = game.install_id
                    game_in_list.launch_id = game.launch_id
                if game.install_id and not game_in_list.install_id:
                    log.debug(f"Extending existing game entry {game_in_list} with launch id: {game.launch_id} and install id: {game.install_id}")
                    game_in_list.install_id = game.install_id
                    game_in_list.launch_id = game.launch_id
                if game.space_id and not game_in_list.space_id:
                    log.debug(f"Extending existing game entry {game_in_list} with space id: {game.space_id}")
                    game_in_list.space_id = game.space_id
                if self._status_rank(game.status) > self._status_rank(game_in_list.status):
                    log.debug(f"Extending existing game entry {game_in_list} with installation status: {game.status}")
                    game_in_list.status = game.status
                    self._copy_preferred_metadata(game_in_list, game)
                if game.owned is not None:
                    log.debug(f"Extending existing game entry {game_in_list} with owned status: {game.owned}")
                    game_in_list.owned = game.owned
                if game.activation_id:
                    log.debug(f"Extending existing game entry {game_in_list} with activation_id: {game.activation_id}")
                    game_in_list.activation_id = game.activation_id

    def extend(self, games):
        spaces = set([game.space_id for game in self if game.space_id])
        installs = set([game.install_id for game in self if game.install_id])
        launches = set([game.launch_id for game in self if game.launch_id])

        for game in games:
            if game.space_id not in spaces and game.install_id not in installs and (game.launch_id not in launches and game.launch_id not in installs):
                if game.space_id:
                    spaces.add(game.space_id)
                log.info(f"Adding new game to collection {game.name} {game.space_id} {game.launch_id}/{game.install_id}")
                super().append(game)
            elif game.space_id in spaces or game.install_id in installs or game.launch_id in launches or game.launch_id in installs:
                self._extend_existing_game_entry(game)

    def __getitem__(self, key):
        if type(key) == int:
            return super().__getitem__(key)
        elif type(key) == str:
            for i in self:
                if key in (i.launch_id, i.space_id):
                    return i
            raise KeyError(f'No game with id: {key}')
        else:
            raise TypeError(f'Excpected str or int, got {type(key)}')

    def get(self, key):
        try:
            return self.__getitem__(key)
        except (KeyError, TypeError):
            return None

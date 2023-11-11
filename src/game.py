class Demon:
    name: str
    health: int


class Item:
    name: str


class Player:
    name: str
    items: list[Item]
    position: int
    health: int
    gold: int

    def __init__(self, name, health=100, gold=10, position=0, items=None):
        if items is None:
            items = []

        self.name = name
        self.items = items
        self.health = health
        self.position = position
        self.gold = gold

    def give_item(self, item: Item):
        self.items.append(item)

    def use_item(self, item_to_use: Item):
        self.items = list(filter(
            lambda item: item.name != item_to_use.name,
            self.items
        ))


class Game:
    grid: tuple[int, int]
    players: list[Player]
    player_name_to_index: dict[str, int]
    demons: list[Demon]

    def __init__(self, player_names: list[str]):
        self.players = []
        self.player_name_to_index = {}
        self.initialize_players(player_names)
        self.assign_grid(len(player_names))

    def initialize_players(self, player_names: list[str]):
        self.players = list(map(
            lambda name: Player(name),
            player_names
        ))
        self.player_name_to_index = dict(zip(
            player_names,
            range(len(player_names))
        ))

    def add_player(self, player_name: str):
        self.player_name_to_index[player_name] = len(self.players)
        self.players.append(Player(player_name))

    def move_player(self, player_name: str, new_position: int):
        self.players[self.player_name_to_index[player_name]]\
            .position = new_position

    def assign_grid(self, player_count: int):
        if player_count in [2, 3]:
            self.grid = (4, 5)
        elif player_count in [4, 5]:
            self.grid = (5, 6)
        else:
            self.grid = (6, 7)

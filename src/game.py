from yaml import safe_load as load, safe_dump as dump


class Demon:
    name: str
    health: int

    def __init__(self, name, health):
        self.name = name
        self.health = health

    def serialize(self):
        return {
            "name": self.name,
            "health": self.health
        }

    @staticmethod
    def from_serial_data(data: dict):
        pure_info = {}
        for key in ["name", "health"]:
            value = data.get(key)
            if value is None:
                return None
            pure_info[key] = value

        return Demon(**pure_info)


class Item:
    name: str
    description: str

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            "name": self.name,
            "description": self.description
        }

    @staticmethod
    def from_serial_data(data: dict):
        pure_info = {}
        for key in ["name", "description"]:
            value = data.get(key)
            if value is None:
                return None
            pure_info[key] = value

        return Item(**pure_info)


class Player:
    name: str
    items: list[Item]
    position: int
    health: int
    power: int
    gold: int

    def __init__(self, name, health=100, power=10, gold=10, position=0, items=None):
        if items is None:
            items = []

        self.name = name
        self.items = items
        self.health = health
        self.power = power
        self.position = position
        self.gold = gold

    def serialize(self):
        def serializer(x): return x.serialize()

        return {
            "name": self.name,
            "items": list(map(serializer, self.items)),
            "position": self.position,
            "health": self.health,
            "power": self.power,
            "gold": self.gold
        }

    @staticmethod
    def from_serial_data(data: dict):
        pure_info = {}
        for key in ["name", "items", "position", "power", "health", "gold"]:
            value = data.get(key)
            if value is None:
                return None
            if key == "items":
                value = list(map(
                    lambda x: Item.from_serial_data(x),
                    value
                ))

            pure_info[key] = value

        return Player(**pure_info)

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

    items: list[Item]

    def __init__(
            self,
            items: list[Item],
            demons: list[Demon],
            player_names: list[str] = None,
            players: list[Player] = None
    ):
        if player_names is None and players is None:
            raise RuntimeError
        if player_names:
            self.players = []
            self.player_name_to_index = {}
            self.initialize_players(player_names)
            self.assign_grid(len(player_names))
        elif players:
            self.players = players
            self.player_name_to_index = {}
            self.generate_player_name_to_index(players)
            self.assign_grid(len(players))
        self.items = items
        self.demons = demons

    @staticmethod
    def from_file(file_name: str):
        data = None
        with open(file_name, 'r') as file:
            data = load(file)
        pure_info = {}
        for (key, constructor) in [
            ("players", Player),
            ("demons", Demon),
            ("items", Item)
        ]:
            value = data.get(key)
            if value is None:
                return None
            if constructor:
                value = list(map(
                    lambda x: constructor.from_serial_data(x),
                    value
                ))
            pure_info[key] = value

        return Game(**pure_info)

    def to_file(self, file_name: str):
        with open(file_name, 'w') as file:
            dump(self.serialize(), file)

    def serialize(self):
        def serializer(x): return x.serialize()

        return {
            "players": list(map(serializer, self.players)),
            "demons": list(map(serializer, self.demons)),
            "items": list(map(serializer, self.items))
        }

    def initialize_players(self, player_names: list[str]):
        self.players = list(map(
            lambda name: Player(name),
            player_names
        ))
        self.player_name_to_index = dict(zip(
            player_names,
            range(len(player_names))
        ))

    def generate_player_name_to_index(self, players: list[Player]):
        for i, player in enumerate(players):
            self.player_name_to_index[player.name] = i

    def add_player(self, player_name: str):
        self.player_name_to_index[player_name] = len(self.players)
        self.players.append(Player(player_name))

    def move_player(self, player_name: str, new_position: int):
        self.players[self.player_name_to_index[player_name]] \
            .position = new_position

    def assign_grid(self, player_count: int):
        if player_count in [2, 3]:
            self.grid = (4, 5)
        elif player_count in [4, 5]:
            self.grid = (5, 6)
        else:
            self.grid = (6, 7)


# items = [
#     Item("Teleport", "Used to teleport to any square"),
#     Item("Luck", "Spin the lucky wheel"),
#     Item("Fireball I", "Gain 5 power points"),
#     Item("Fireball II", "Gain 10 power points"),
#     Item("Fireball III", "Gain 20 power points")
# ]
#
#
# def get_items(indices: list[int]):
#     return list(map(lambda x: items[x], indices))
#
#
# demons = [
#     Demon("Charlie", 100),
#     Demon("John", 92),
#     Demon("Hydra", 80),
#     Demon("Goblin", 50)
# ]
# players = [
#     Player("Comet", items=get_items([0, 0, 1])),
#     Player("SG", items=get_items([1, 2, 2])),
#     Player("Marcel", items=get_items([4]))
# ]
# game = Game(items, demons, players=players)
# game.to_file("data.yaml")
game = Game.from_file("data.yaml")
print(game.serialize())

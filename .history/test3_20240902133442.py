from Scrabble import PlayerQueue, Player

players: list[Player] = [Player() for _ in range(4)]
queue = PlayerQueue(players)
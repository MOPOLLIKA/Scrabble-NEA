from Scrabble import PlayerQueue, Player

players: list[Player] = [Player() for _ in range(3)]
queue: PlayerQueue = PlayerQueue(players)
print(queue.nextTurn())
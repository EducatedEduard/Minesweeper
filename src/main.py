from minesweeper.game.game import Game
from minesweeper.game.gamestate import GameState
from minesweeper.ui.ui_human import HumanUI
from minesweeper.bot.random_bot import RandomBot

def main():
    state = GameState(minecount= 60, size= (20, 20))
    game = Game(initial_state=state)

    ui = HumanUI()
    bot = RandomBot()

    # while not game.gamestate.lost:
    while True:
        ui.render(game.gamestate)

        action = ui.get_action(game.gamestate)
        # action = bot.select_action(game.gamestate)

        game.step(action)

    ui.render(game.gamestate)

if __name__ == "__main__":
    main()

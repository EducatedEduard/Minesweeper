from minesweeper.game.game import Game
from minesweeper.game.gamestate import GameState
from minesweeper.ui.ui_human import HumanUI
from minesweeper.bot.random_bot import RandomBot

def main():
    state = GameState(minecount= 3, size= (10, 10))
    game = Game(initial_state=state)

    ui = HumanUI()
    bot = RandomBot()

    while not game.gamestate.lost:
        ui.render(game.gamestate)

        action = ui.get_action(game.gamestate)
        # action = bot.select_action(engine.state)

        game.step(action)

    ui.render(engine.state)

if __name__ == "__main__":
    main()

from minesweeper.game.game import Game
from minesweeper.game.gamestate import GameState
from minesweeper.ui.ui_human import HumanUI
from minesweeper.bot.random_bot import RandomBot
from minesweeper.bot.basic_bot import BasicBot

def main():
    state = GameState(minecount= 60, size= (20, 20))
    game = Game(initial_state=state)

    ui = HumanUI()
    # bot = RandomBot()
    bot = BasicBot()

    # while not game.gamestate.lost:
    while True:
        ui.render(game.gamestate)

        # action = ui.get_action(game.gamestate)
        action = bot.select_action(game.gamestate)

        if action:
            game.step(action)

    ui.render(game.gamestate)
    bot.stop()
    
if __name__ == "__main__":
    main()

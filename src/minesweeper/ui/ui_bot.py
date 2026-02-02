class BotUI:
    def __init__(self, bot):
        self.bot = bot

    def get_action(self, state):
        return self.bot.select_action(state)

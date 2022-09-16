from Enum.ResEnum import ImgEnumG
from UiPage.BasePage import BasePageG


class LoginUiPageG(BasePageG):

    def start_game(self):
        self.start_game()

    def start_login(self):
        self.air_loop_find(ImgEnumG.GAME_ICON, 1, True)
        self.time_sleep(30)
        # for i in range(3):

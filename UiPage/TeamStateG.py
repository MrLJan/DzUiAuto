from UiPage.BasePage import BasePageG


class TeamState(BasePageG):
    def __init__(self, devinfo, mnq_name, sn):
        super(TeamState, self).__init__()
        self.dev = devinfo[0]
        self.serialno = devinfo[-1]
        self.sn = sn
        self.mnq_name = mnq_name

    def CheckTeamState(self):
        pass

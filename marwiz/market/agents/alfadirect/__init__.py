"""\
Wrapper for AlfaDirect trading terminal: http://www.alfadirect.ru/
"""

from win32com import client

########################################################################
class AlfaDirectAgent(object):
    """"""

    def __init__(self):
        """
        Automatically joining with API.
        """
        self.client = client.Dispatch("ADLite.AlfaDirect")
        
    #----------------------------------------------------------------------
    def __del__(self):
        """"""
        # Preparing for removing:
        # if user forget to logout do it
        if self.isconnected:
            self.logout()
        del self.client
        

    def login(self, user, pasw):
        """
        Login to a system.
        """
        self.client.UserName = user
        self.client.Password = pasw
        self.client.Connected = True

    def logout(self):
        """
        Logout from a system.
        """
        self.client.Connected = False
        self.client.Password = ""
        self.client.UserName = ""
        
    @property
    def isconnected(self):
        """
        Returns True when user have logged in.
        """
        return self.client.Connected
        
from __future__ import print_function



class wp_excption(Exception):
    def __init__(self,msg):
        super(wp_excption, self).__init__()
        self.errmsg = msg
        
from __future__ import print_function
#from pymavlink import mavutil
import sys
import ui
__metaclass__=type

def main(argv=None):
    app = ui.sctrlp_ui()
    app.draw()

    
if __name__ == '__main__': 
    sys.exit(main())
else:
    print("It can not be imported")
    sys.exit()



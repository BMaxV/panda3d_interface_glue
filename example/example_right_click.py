from direct.gui.DirectGui import DirectFrame
from direct.showbase.ShowBase import ShowBase
from direct.gui import DirectGuiGlobals as DGG
from panda_interface_glue import right_click_drop_down
import time

class RightClick:
    def __init__(self):
        self.output = []
        
        frame_size = (-0.1, 0.1, -0.1, 0.1)
        pos1 = (0, 0, 0)
        self.F1 = DirectFrame(pos=pos1, frameSize=frame_size, state=DGG.NORMAL)
        
        # frame styling is not done yet...
        right_click_drop_down.setup_right_click(self.F1,["A","B","C"],self.output)
        
        
        pos1 = (0.5, 0, 0.5)
        self.F2 = DirectFrame(pos=pos1, frameSize=frame_size, state=DGG.NORMAL)
        
        # frame styling is not done yet...
        right_click_drop_down.setup_right_click(self.F2,["xy","zd","asdf"],self.output)
        
        
        
        
        
        
        
class Wrapper:
    def __init__(self):
        self.b = ShowBase()

        # this sets up the elements for the demo.
        self.RightClick = RightClick()

def main():
    W = Wrapper()
    while True:
        W.b.taskMgr.step()
        if W.RightClick.output!=[]:
            print("myoutput",W.RightClick.output)
            while len(W.RightClick.output)>0:
                W.RightClick.output.pop(0)
                


if __name__ == "__main__":
    main()

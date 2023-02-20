import drag_main

class App:
    def __init__(self):
        #DirectFrame(pos=(0.5,0.1,0.1),frameSize=(-1,1,-1,1))
        #DirectButton(pos=(0.5,0,0))
        # for demonstration purposes:
        # get a few colors as "types"

        # red green blue white black
        # only provide red green blue cubes
        

        # add a title/instructions
        wp = drag_main.WindowProperties.getDefault()
        wp.set_title("Drag & Drop the colored squares")
        drag_main.WindowProperties.setDefault(wp)
        # init showvase
        base = drag_main.ShowBase.ShowBase()
        
        self.DC=drag_main.Drag_Container()
        self.DC.dac=drag_main.demo_arg_cont()
        
        
        #this is the grid where the draggables are supposed to be at the start.
        
        self.DC.default_grid = drag_main.Grid((64, 300), (64, 64), (4, 1))
        
        self.DC.my_grids = [self.DC.default_grid]
        
        #self.DC.default_grid.setColorOff(0)
        drag_main.bind_grid_events(self.DC.default_grid.d,self.DC.hover_in,self.DC.hover_out)
        
        self.DC.grid = drag_main.TargetColoredGrid((32, 32), (64, 64), self.DC.dac.colors)
        
        drag_main.bind_grid_events(self.DC.grid.d,self.DC.hover_in,self.DC.hover_out)
        Ds=drag_main.make_drag_items(self,3)
        
        c=0
        m=len(Ds)
        for d in Ds:
            key=str((c,0))
            #key is where it is supposed to go.
            drag_main.lock(d,self.DC.default_grid.d,self.DC.drag_items,key)
            c+=1
 
def old():
    app = App()
    base.run()

if __name__=="__main__":
    old()

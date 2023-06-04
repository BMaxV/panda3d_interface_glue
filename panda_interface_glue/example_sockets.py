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
        
        pixels=False
        
        self.DC=drag_main.Drag_Container()
        self.DC.pixels=pixels
        self.DC.dac=drag_main.demo_arg_cont()
        
        
        #this is the grid where the draggables are supposed to be at the start.
        
        
        if pixels:
            pos,offset=(64, 300), (64, 64)
        else:
            pos,offset=(-0.5,0,0), (0.2,0.2)
        
        self.DC.default_grid = drag_main.Grid(pos,offset, (4, 1),pixels=pixels)
        
        #pixels=True
        
        self.DC.my_grids = [self.DC.default_grid]
        
        #self.DC.default_grid.setColorOff(0)
        drag_main.bind_grid_events(self.DC.default_grid.d,self.DC.hover_in,self.DC.hover_out)
        
        
        if pixels:
            pos,offset=(32, 32), (64, 64)
        else:
            pos,offset=(-0.5,0,0.5), (0.2,0.2)
        
        self.DC.grid = drag_main.TargetColoredGrid(pos,offset, self.DC.dac.colors,pixels=pixels)
        
        drag_main.bind_grid_events(self.DC.grid.d,self.DC.hover_in,self.DC.hover_out)
        Ds=drag_main.make_drag_items(self,3,pixels=pixels)
        
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

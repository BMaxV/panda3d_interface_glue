import drag_main

class App2:
    def __init__(self):
        #######
        # this is panda stuff
        # init window and rendering
        # add a title/instructions
        wp = drag_main.WindowProperties.getDefault()
        wp.set_title("smooth container arrangement")
        
        drag_main.WindowProperties.setDefault(wp)
        # init showvase
        self.b = drag_main.ShowBase.ShowBase()
        
        #####
        # this sets up the elements for the demo.
        
        self.DC = drag_main.Drag_Container()
        self.DC.adjust_existing = True
        
        self.F = drag_main.container_surface(pos=(200,200))
        self.F2 = drag_main.container_surface(pos=(200,400))
        
        a = drag_main.construct_draggable(self.DC,None,rel_col=(1.0,0,0,1.0),represented_item='A')
        b = drag_main.construct_draggable(self.DC,None,rel_col=(1.0,0,0,1.0),represented_item='B')
        c = drag_main.construct_draggable(self.DC,None,rel_col=(1.0,0,0,1.0),represented_item='C')
        
        l=[a,b,c]
        
        for x in l:
            x.drop_this_smooth=True
        
        self.F2.sorted_elements=[]
        self.F.sorted_elements=[]
        
        drag_main.position_on(self.DC,self.F,l)
        
        drag_main.bind_single_events(self.F,self.DC.hover_in,self.DC.hover_out)
        drag_main.bind_single_events(self.F2,self.DC.hover_in,self.DC.hover_out)
        
        
        
def new():
    app = App2()
    app.b.run()
    
if __name__=="__main__":
    new()


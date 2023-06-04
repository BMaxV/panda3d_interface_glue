import drag_main
from drag_main import DirectFrame

class App2:
    
    def do_aspect_bullshit(self,*args):
        print("yo")
        #self.DC.aspect_ratio=self.b.getAspectRatio()
        
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
        
        #self.b.accept("window-event",self.do_aspect_bullshit)
        #####
        # this sets up the elements for the demo.

        self.DC = drag_main.Drag_Container()
        self.DC.adjust_existing = True

        pixels = False
        
        if False:
            c=0
            m=10
            while c < m:
                pos=(-1+0.2*c,0,0)
                size=(-0.05, 0.05, -0.05, 0.05)
                DirectFrame(pos=pos,frameSize=size)
                c+=1
        #return
        
        if pixels:
            pos1 = (200, 200)
            pos2 = (200, 400)
            size = (200, 50)
        else:
            pos1 = (0.5, 0, 0.2)
            pos2 = (0.5, 0, -0.5)
            size = (-0.2, 0.2, -0.05, 0.05)

        self.DC.pixels = pixels

        self.F = drag_main.container_surface(
            pos=pos1, size=size, pixels=pixels)

        self.F2 = drag_main.container_surface(
            pos=pos2, size=size, pixels=pixels)

        if not pixels:
            pos = (0.5, 0, -0.3)
            size = (-0.1, 0.1, -0.05, 0.05)

            self.F3 = drag_main.container_surface(
                pos=pos, size=size, pixels=pixels)

            drag_main.bind_single_events(
                self.F3, self.DC.hover_in, self.DC.hover_out)

            pos = (0.5, 0, -0.1)
            size = (-0.3, 0.3, -0.05, 0.05)

            self.F4 = drag_main.container_surface(
                pos=pos, size=size, pixels=pixels)

            drag_main.bind_single_events(
                self.F4, self.DC.hover_in, self.DC.hover_out)

        a = drag_main.construct_draggable(self.DC, None, rel_col=(
            1.0, 0, 0, 1.0), represented_item='Aasdfasdfasdf', pixels=pixels)
        b = drag_main.construct_draggable(self.DC, None, rel_col=(
            1.0, 0, 0, 1.0), represented_item='B', pixels=pixels)
        c = drag_main.construct_draggable(self.DC, None, rel_col=(
            1.0, 0, 0, 1.0), represented_item='C', pixels=pixels)

        l = [a, b, c]

        for x in l:
            x.drop_this_smooth = True

        self.F2.sorted_elements = []
        self.F.sorted_elements = []

        if pixels:
            size = 200
        else:
            size = 0.4

        drag_main.position_on(self.DC, self.F, l, size=size, pixels=pixels)

        drag_main.bind_single_events(
            self.F, self.DC.hover_in, self.DC.hover_out)

        drag_main.bind_single_events(
            self.F2, self.DC.hover_in, self.DC.hover_out)


def new():
    app = App2()
    app.b.run()


if __name__ == "__main__":
    new()

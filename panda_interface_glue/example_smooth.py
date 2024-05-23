import drag_main
from drag_main import DirectFrame


class Wrapper:
    def __init__(self):
        wp = drag_main.WindowProperties.getDefault()
        wp.set_title("smooth container arrangement")

        drag_main.WindowProperties.setDefault(wp)

        self.b = drag_main.ShowBase.ShowBase()

        # this sets up the elements for the demo.
        self.DragDemo = MyDraggableDemo()


class MyDraggableDemo:

    def __init__(self):
        #######
        # this is panda stuff
        # init window and rendering
        # add a title/instructions
        self.build()

    def build(self):
        pixels = False

        self.DC = drag_main.Drag_Container()
        self.DC.adjust_existing = True
        self.DC.pixels = pixels

        # build my target surface frames
        input_l = [
            ((0.5, 0, 0.2), (-0.2, 0.2, -0.05, 0.05)),
            ((0.5, 0, -0.5), (-0.2, 0.2, -0.05, 0.05)),
            ((0.5, 0, -0.3), (-0.1, 0.1, -0.05, 0.05)),
            ((0.5, 0, -0.1), (-0.3, 0.3, -0.05, 0.05)),
        ]

        frames = []
        for pos, size in input_l:

            F = drag_main.container_surface(
                pos=pos, size=size, pixels=pixels)
            F.sorted_elements = []
            drag_main.bind_single_events(
                F, self.DC.hover_in, self.DC.hover_out)
            frames.append(F)

        # construct draggable elements:

        config_d = {"rel_col": (1.0, 0, 0, 1.0), "pixels": pixels}
        items = ['Aasdfasdfasdf', 'B', 'C']
        my_draggable_items = []
        for my_item in items:
            config_d["represented_item"] = my_item
            my_drag_item = drag_main.construct_draggable(
                self.DC, None, **config_d)
                
            # this has to be enabled, because I use the same constructor
            # for smooth and socket modes.    
            my_drag_item.drop_this_smooth = True    
            my_draggable_items.append(my_drag_item)
            
        # why?
        frames[0].sorted_elements = []
        frames[1].sorted_elements = []

        target_frame = frames[0]
        drag_main.position_on(self.DC, target_frame,
                              my_draggable_items, pixels=pixels)


def main():
    W = Wrapper()
    while True:
        W.b.taskMgr.step()


if __name__ == "__main__":
    main()

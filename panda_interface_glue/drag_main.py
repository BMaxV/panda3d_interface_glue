'''
Drag & Drop Demo

you can drag the the smaller,darker colored squares in the "correct" bigger colored
squares.

there are default values and "types" that make the small square fall back to the
last valid "anchor"

there are three main functions parts that need to be understood to understand
the program:

drag and drop functions are functions that are executed when the object
is picked up or dropped

update is a task that runs continously and updates the position of the dragged
object

Output has to be copied from a .output variable of the grid.
to see if things have changed.

'''

import random

from direct.showbase import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase import ShowBase
from direct.showbase.MessengerGlobal import messenger
        
colors = {"red": (0.8, 0.2, 0.2, 1.0), "light_red": (1, 0.5, 0.5, 1.0),
              "green": (0.2, 0.8, 0.2, 1.0), "light_green": (0.5, 1, 0.5, 1.0),
              "blue": (0.2, 0.2, 0.8, 1.0), "light_blue": (0.5, 0.5, 1, 1.0),
              "white": (1, 1, 1, 1.0), "black": (0, 0, 0, 1.0)}
    
color_l = ["red", "green", "blue"]


class Grid:
    """utility class to build a grid quickly.
    
    when using multiple grids, grid_key_prefix is can be used, to
    differentiate different sets of grids in the same drag controller
    keys are then formed like this:
    'key=grid_key_prefix + str((x_i,y_i))'
    """

    def __init__(self, pos, offset, rows_collums=(3, 3), frame_kwargs={},default=True,grid_key_prefix="",owner=None):
        
        self.default_drops=[]
        
        x, y = rows_collums
        self.d = {}
        c=0
        x_i = 0
        while x_i < x:

            y_i = 0
            while y_i < y:

                dd_type = None

                if x_i == 2:
                    dd_type = "red"
                
                pos_i = (pos[0] + offset[0] * x_i, pos[1] + offset[1] * y_i)
                
                if "drag_drop_type" not in frame_kwargs:
                    frame_kwargs["drag_drop_type"]=dd_type
                
                key=grid_key_prefix + str((x_i,y_i))
                
                frame_kwargs["pos"]=pos_i
                frame_kwargs["key"]=key
                frame_kwargs["owner"]=owner
                frame = construct_frame(**frame_kwargs)
                self.default_drops.append(key)
                self.d[key] = frame
                
                    
                frame.index=c
                
                c+=1
                y_i += 1
            x_i += 1


class TargetColoredGrid(Grid):
    def __init__(self, pos, offset, colors, rows_collums=(6, 1),shuffle=True,grid_key_prefix="target"):
        
        Grid.__init__(self,pos,offset,rows_collums,grid_key_prefix=grid_key_prefix)
        
        #super(TargetColoredGrid,self).__init__(pos,offset,rows_collums)
        
        if not rows_collums[0] <= len(colors) :
            raise ValueError("collumn items have to be equal or fewer than colors")
        # making sure the "targets" are shuffled, so they rely on
        # the type system
        col_l = ["white", "black", "light_red", "light_blue", "light_green"]
        
        if shuffle:
            random.shuffle(col_l)

        #color setting
        x, y = rows_collums
        
    
        col_key = col_l[0]
        col_i = colors[col_key]
        y_i = 0
        for key in self.d.keys():
            if y_i < len(col_l)-1:
                col_key = col_l[y_i]
                col_i = colors[col_key]
                self.d[key].setColor(col_i)
                if "light" in col_key:
                    col_key=col_key[(len("light")+1):]
                self.d[key].drag_drop_type=col_key
            y_i += 1
        l=list(self.d.keys())
        last_key=l[-1]
        
        self.d[last_key].setColor(col_i)
        self.d[last_key].drag_drag_type=None

def create_drag_tooltip(parent,pixel2d,text="hello there",*args):
    """create tooltip for draggables"""
    
    print("draggable created")
    if base.mouseWatcherNode.has_mouse():
    
        mpos = base.mouseWatcherNode.get_mouse()
        pos = Point3(mpos.get_x(), 0, mpos.get_y())
        pixel2d.get_relative_point(render2d, pos)
    position=(0.5,0.5,-0.5)
    tooltip=OnscreenText(text=text, scale=.07,
     pos=pos,fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))#DirectLabel(text=text,pos=position,scale=(0.1,0.1,0.1),textMayChange=0)
    tooltip.reparent_to(pixel2d)
    parent.spawned_tooltip=tooltip 
    
    
def destroy_drag_tooltip(parent,*args):
    """destroy tooltip for draggables"""
    print("parent,args",parent,args)
    if "spawned_tooltip" in dir(parent):
        ob=parent.spawned_tooltip
        ob.removeNode()
        parent.spawned_tooltip=None
    else:
        print("this thing seems to have no tooltip")
    
def drop_decide(DC,frame,*args,**kwargs):
    
    drop_this_smooth = False
    if DC.last_hover_in != None:
        if "sorted_elements" in dir(DC.last_hover_in):
            drop_this_smooth = True
    
    if "sorted_elements" in dir(DC.current_dragged.last_drag_drop_anchor):
        drop_this_smooth = True
    
    if drop_this_smooth:
        DC.drop_smooth(frame)
    else:
        DC.drop(frame)
    

def construct_draggable(abstract_container,
                        drag_type,
                        rel_col=(1.0,1.0,1.0,1.0),
                        represented_item=None,
                        amount=1):
    """construct a draggable frame that contains another object
    there is some... design foo involved.
    by having it contain a different object, the interactions may not be 
    completely trivial at the same time I want users, people as well as programs,
    to be able to access the contained object's data,
    so actually referencing the object is a good idea from that perspective
    
    so right now, represented_item can be either just text
    or it should support .name or .text, which will then be displayed.
    (checks are in this order)    
    """
    
    frame = DirectFrame(    frameSize=_rec2d(30, 30),
                            state=DGG.NORMAL,
                            parent=pixel2d,
                            #sortOrder=0,
                            )
    
    frame.key=None
    frame.drop_this_smooth=False
    
    frame.is_draggable=True
    frame.represented_item=represented_item
    frame.amount=amount
    
    frame.setColorOff(1)
    frame.setColor(rel_col)
    # bind the events
    frame.bind(DGG.B1PRESS, abstract_container.left_mouse_decide, [frame])
    frame.bind(DGG.B1RELEASE, drop_decide, [abstract_container, frame])
    
    h, w = get_local_center(frame)
    pos=(0.4,-0.3,-0.5)
    
    
    this_dir=dir(represented_item)
    if type(represented_item)==str:
        text=represented_item
        
    elif "name" in this_dir:
        text=represented_item.name
    
    elif "name" in this_dir and "text" in this_dir:
        #plus something with textwrap? eh...
        text=represented_item.name+"\n"+represented_item.text
        
    elif "text" in dir(represented_item):
        text=represented_item.text
    else:
        text=str(represented_item)
        
    T=OnscreenText(text=text, 
                    scale=15,
                    pos=pos,
                    fg=(0,0,0, 1),
                    shadow=(1,1,1, 0.5))#DirectLabel(text=text,pos=position,scale=(0.1,0.1,0.1),textMayChange=0)
    
    T.reparent_to(frame)
    T.setAlign(0)
    T.setPos(0,-10)
    
    if amount!=1:
        pos2=(0,0,0)#0.4,-0.3,-0.55)
        T=OnscreenText(text=str(amount), scale=15,
        pos=pos2,fg=(0,0,0, 1), shadow=(1,1,1, 0.5))#DirectLabel(text=text,pos=position,scale=(0.1,0.1,0.1),textMayChange=0)
        T.reparent_to(frame)
        T.setAlign(0)
        T.setPos(0,-20)
    
    #should work but doesn't show. ask in irc
    #frame.bind(DGG.WITHIN , create_drag_tooltip,[frame,pixel2d,represented_item.name])
    #frame.bind(DGG.WITHOUT, destroy_drag_tooltip,[frame])
    
    # the type in our case is just the color, but it can be
    # anything that you can compare
    
    frame.drag_drop_type = drag_type
    
    return frame
    
def lock(frame,grid,drag_items,key):
    """ this assigns the default location 
    
    for "frame" 
    in an already defined grid "grid"
    by means of a "key" that goes into grid.d
    also key must not be in "drag_items"
    to make sure no items are in the same place
    
    #it's a bi directional lookup.
    #I can look up from the grid and it will return the anchor
    #and I can look from the drag items and they will be
    #listed with the anchor key as key.
    
    #so the key is the identifier
    
    snap snaps object to anchorframe
    """
    
    frame.last_drag_drop_anchor = grid[key]
    snap(frame, grid[key])
    frame.key=key
    frame.is_draggable=True
    assert key not in drag_items #don't overwrite
    drag_items[key] = frame  # took out y this one should be unique.
    frame.current_key=key

def construct_frame(pos, 
                    size=(50,50),
                    color=(1, 1, 1, 1.0),
                    drag_drop_type=None,
                    key=None,
                    owner=None,
                    ):
    #color=(
       # 1, 1, 1, 1.0),
       
    kwargs = {"frameColor": color,
              "frameSize": _rec2d(*size),
              "state": DGG.NORMAL,
              "parent": pixel2d, #aspect2d
              #"sortOrder":1,
              }
    
    frame = DirectFrame(**kwargs)
    #frame.setColorOff(0)
    frame.set_pos(_pos2d(*pos))
    frame.drag_drop_type = drag_drop_type
    frame.key=key
    frame.is_draggable=False
    frame.index=float("inf")
    frame.owner=owner
    return frame

# Helper functions


def _pos2d(x, y):
    return Point3(x, 0, -y)


def _rec2d(width, height):
    return (width, 0, 0, -height)


def get_local_center(ob):

    h = ob.getHeight()
    w = abs(ob.getWidth())

    w = w / 2
    h = h / 2

    return h, w


def get_mid_point(ob):
    h, w = get_local_center(ob)

    r = ob.getPos()

    r = r - LPoint3f(h, w)

    return r
    left, right, bottom, top = ob.frameSize()

    half_r = (right - left) / 2
    half_b = (bottom - top) / 2

    mid_x = left + half_r
    mid_y = top + half_b

    return mid_x, mid_y

class demo_arg_cont:
    colors = {"red": (0.8, 0.2, 0.2, 1.0), "light_red": (1, 0.5, 0.5, 1.0),
              "green": (0.2, 0.8, 0.2, 1.0), "light_green": (0.5, 1, 0.5, 1.0),
              "blue": (0.2, 0.2, 0.8, 1.0), "light_blue": (0.5, 0.5, 1, 1.0),
              "white": (1, 1, 1, 1.0), "black": (0, 0, 0, 1.0)}
    
    color_l = ["red", "green", "blue"]
     
class Drag_Container:
    """container object for the various that are necessary,
    keeping track of which object is being dragged,
    what the valid targets are,
    where the default return to tile is, etc.
    
    there are two important dicts, as far as the UI and containing is concerned:
    .grid and .drag_items
    .grid contains the anchor point objects, the frames you drag and drop into
    .drag_items contains the frames that represent the items you drag around
    
    if you confuse the two, you might be wondering why your stored object is seemling not there anymore.
    it's... not very clear from the code how stuff gets assigned. Sorry
    
    both .grid and .grad_items contain the same string converted 2d coordinates / object pairs
    the "lock" function creates the cross links
    
    "snap" moves the drag_item-frame to the grid-frame's position
    
    drop callback will be called once an item has been dropped anywhere
    to enable you to do something custom on that event.
    
    Stack Splitting REQUIRES a .my_grids list to be defined
    Since those depend on your use case, I can't do it automatically.
    Sort of. Or at least I'm too lazy right now.
    
    
    """
    def __init__(self,drop_callback=None):
        # helper attributes
        
        self.adjust_existing = False
        self.current_last_drag_drop_anchor = None
        
        self.current_dragged = None
        self.last_hover_in = None
        self.current_last_anchor = None
        self.current_drag_drop_type = None
        self.last_hover_drag_drop_type = None
        
        self.drag_items = {}
        # run a task tracking the mouse cursor
        taskMgr.add(self.update, "update", sort=-50)

        self.output_info=[]
        self.ignore_ownership=False
        self.drop_option=None
        
        self.drop_callback = drop_callback
        
        self.my_grids=[]
        self.split_frame=None
        self.event_handler = DirectObject.DirectObject()
        
        self.state = {"ctrl":False,"shift":False}
        
        self.event_handler.accept("control",self.set_state,["enter","ctrl"])
        self.event_handler.accept("shift",self.set_state,["enter","shift"])
        self.event_handler.accept("control-up",self.set_state,["leave","ctrl"])
        self.event_handler.accept("shift-up",self.set_state,["leave","shift"])
        
        # for more complex interactions
        self.split_object_collection =[]
    
    def next_free_key(self):
        xl=self.grid.d.keys()
        xl2=[]
        for x in xl:
            xl2.append((self.grid[x],x))
        xl2.sort(key=lambda x : x[0].index)
        c=0
        while True:
            tup=xl2[c]
            if tup[1] not in self.drag_items:
                return tup[1]
            c+=1
    
    def hover_in(self, widget, mouse_pos=None):
        '''Set the widget to be the target to drop objects onto'''

        self.last_hover_in = widget
        self.last_hover_drag_drop_type = widget.drag_drop_type

    def hover_out(self, mouse_pos=None):
        '''Clear the target to drop objects onto'''
        self.last_hover_in = None
        self.last_hover_drag_drop_type = None
        
    def split_size(self,diff,other):
        """set my split size with one of the buttons"""
        self.split_size_max
        
        in_range = (0 < self.split_size_counter + diff < self.split_size_max)
        
        if in_range:
            self.split_size_counter+=diff
            
        if self.split_object_collection!=[]:
            text=self.split_object_collection[0]
            text.enterText(str(self.split_size_counter))
        
    def finalize_split(self,cancel=False,other=None):
        if cancel:
            self.destroy_split_UI()
        my_value = None
        in_range = False
        if self.split_object_collection!=[]:
            text=self.split_object_collection[0]
            my_text=text.get()
            try:
                my_value=int(my_text)
                in_range = (0 < my_value < self.split_size_max)
            except ValueError:
                pass
        
        
        if not cancel and my_value != None and in_range:
            # find an empty slot, actually do that first.
            # create a new draggable
            grid=None
            for grid in self.my_grids:
                if self.split_frame.key in grid.d:
                    break
            
            # go by owner?
            if grid!=None:
            
                key = next_free_key(grid.d,self.drag_items)
                
                if key != None:
                    self.split_frame.amount-=my_value
                    nf=construct_draggable(self,self.split_frame.represented_item,amount=my_value)
                    # bind or something
                    lock(nf,grid.d,self.drag_items,key)
            else:
                print("eh? for stack splitting, something needs to be set up where to drop the new stack")        
                
            self.destroy_split_UI()

    def destroy_split_UI(self):
        for x in self.split_object_collection:
            x.removeNode()
        self.split_object_collection=[]
        self.split_frame=None
        
    def try_set_counter(self,*args):
        if self.split_object_collection!=[]:
            text=self.split_object_collection[0]
            my_text=text.get()
            try:
                my_value=int(my_text)
                in_range = (0 < my_value < self.split_size_max)
                self.split_size_counter=my_value
            except ValueError:
                pass

    def left_mouse_decide(self,frame,mouse):
        """
        sooooooo because of shenanigans, I can't bind an action
        directly to multiple keys.
        
        Instead what I have to do here is to bind this monster
        to left click, then check what state I have entered before
        by pressing or releasing or control.
        
        
        
        """
        if self.state["shift"]:
            if frame.amount > 1:
                
                # record some things.
                self.split_frame = frame
                self.split_size_counter = frame.amount.__floordiv__(2)
                self.split_size_max = frame.amount
                
                # create my number entry things.
                text_entry = DirectEntry(pos=(0.5,0.3,-0.3),scale=0.05,focusOutCommand=self.try_set_counter,focusOutExtraArgs=tuple())
                
                up_b1 = create_button("more",(0.8,0.3,-0.3),0.05,self.split_size,(1,))
                down_b2 = create_button("less",(0,0.3,-0.3),0.05,self.split_size,(-1,))
                set_button = create_button("ok",(0,0.4,-0.5),0.05,self.finalize_split,(False,))
                cancel_button = create_button("cancel",(0.8,0.4,-0.5),0.05,self.finalize_split,(True,))
                self.split_object_collection = [text_entry, up_b1, down_b2, set_button, cancel_button]                
        else:
            #whatever I was doing before?
            self.drag(frame)
    
    def set_state(self,*tup):
        if tup[0]=="enter":
            self.state[tup[1]] = True
        if tup[0]=="leave":
            self.state[tup[1]] = False
    

    def update(self, task=None):
        '''Track the mouse pos and move self.current_dragged to where the cursor is '''
        
        #I supposed if I was dragging around and wanted to insert something
        #between two, this would be where I would be doing that?
        #calculate the closest two,
        #and if I drop, pick the appropriate insert location and move everything
        #else?
        #also to move the ones that are currently inside those.
        #but that's probably easier to do if I didn't have a grid?
        
        if self.current_dragged:

            if base.mouseWatcherNode.has_mouse():
                mpos = base.mouseWatcherNode.get_mouse()
                pos = Point3(mpos.get_x(), 0, mpos.get_y())
                pos = pixel2d.get_relative_point(render2d, pos)
                self.current_dragged.set_pos(pos)
                
                # also, update positions of other elements
                # depending on this one and if I'm currently hover in one
                
                if self.adjust_existing:
                    if self.last_hover_in!=None and "sorted_elements" in dir(self.last_hover_in):
                        els=list(self.last_hover_in.sorted_elements)
                        if self.current_dragged in els:
                            els.remove(self.current_dragged)
                        position_on(self,self.last_hover_in,els)
                        
                        parent_pos=self.last_hover_in.get_pos()
                        
                        shift_to_make_space(els,parent_pos,pos)
        
        if task:
            return task.again

    def drag(self, widget, mouse_pos=None):
        '''Set the widget to be the currently dragged object'''

        self.current_last_drag_drop_anchor = widget.last_drag_drop_anchor
        
        if "sorted_elements" in dir(widget.last_drag_drop_anchor):
            widget.old_order=list(widget.last_drag_drop_anchor.sorted_elements)
            
        h, w = get_local_center(widget)

        widget.reparent_to(pixel2d)
        self.current_dragged = widget
        self.current_dragged.h = h
        self.current_dragged.w = w
        self.update()

    def drop_smooth(self,frame):
        """
        figure out where the dragged element is in relation to other 
        contained items and insert it at the appropriate position
        """
        pos = None
        if base.mouseWatcherNode.has_mouse():
            mpos = base.mouseWatcherNode.get_mouse()
            pos = Point3(mpos.get_x(), 0, mpos.get_y())
        
        if pos==None:
            raise ValueError
        if self.current_dragged:
            # if I'm dragging something
            if self.last_hover_in:
                # and I'm hovering somewhere.
                parent_pos=self.last_hover_in.get_pos()
                pos = pixel2d.get_relative_point(render2d, pos)
                
                these=list(self.last_hover_in.sorted_elements)
                if self.current_dragged in these:
                    these.remove(self.current_dragged)
                i=0
                for x in these:
                    el_pos=x.get_pos()
                    val1=el_pos[0]+parent_pos[0]
                    if val1 > pos[0]:
                        break
                    i+=1
                these.insert(i,self.current_dragged)
                
                other_elements = these
                position_on(self,self.last_hover_in,other_elements)
                
                self.drag_items[self.last_hover_in.key]=self.current_dragged
                self.current_dragged.key=self.last_hover_in.key
                
            else:
                # drop it back into the thing I took it from?
                
                if "old_order" in dir(self.current_dragged):
                    these = self.current_dragged.old_order
                else:
                    these = frame.last_drag_drop_anchor.sorted_elements
                    these.append(self.current_dragged)
                position_on(self,frame.last_drag_drop_anchor,these)
            
            self.current_dragged=None
            
    def drop(self, mouse_pos=None):
        '''Drop the currently dragged object on the last object the cursor hovered over'''
        
        #eh, I need to switch places with whatever I'm dropping
        #if the target is "occupied"
        
        #and I still need to send that signal somehow.
        
        if self.current_dragged:
            #if I'm dragging something
            if self.last_hover_in:
                #if I'm hovering inside something that makes sense.
                cond11=(self.last_hover_drag_drop_type == None)
                cond12=(self.current_dragged.drag_drop_type == self.last_hover_drag_drop_type)
                if self.ignore_ownership==False:
                    cond2=(self.last_hover_in.owner==self.current_last_drag_drop_anchor.owner)
                else:
                    cond2=True
                
                #that's just... what. it's meant to prevent stacking.
                #but if they keys are the same, it's nonsense.
                
                cond3=(self.last_hover_in.key not in self.drag_items)
                
                #if type is ok or doesn't matter
                #and ownership of tiles and containers is ok
                #and the target is a tile and not a dragable
                big_cond=(( cond11 or cond12) and cond2 and cond3)
                
                
                if big_cond:
                    
                    #if it's empty and the type matches and it belongs to the same grid
                    
                    # everything in order, snap to the one that's currently being
                    # hovered over.
                    snap_target = self.last_hover_in
                    old_owner=self.current_dragged.last_drag_drop_anchor.owner
                    self.current_dragged.last_drag_drop_anchor = snap_target
                    self.output_info.append((self.current_dragged,snap_target,self.current_dragged.represented_item,old_owner,snap_target.owner))
                    
                else:
                    error_message=[
                    [self.current_dragged.drag_drop_type, self.last_hover_drag_drop_type],
                    cond11,
                    cond12,
                    cond2,
                    cond3,
                    self.last_hover_in.key , self.drag_items]
                    print("error type doesn't match, fall back",str(error_message))
                    # in this case the frame the user hovers over is invalid.
                    # the last one gets picked as default target and is
                    # snapped to.
                    snap_target = self.current_last_drag_drop_anchor
                    
            else:
                
                self.drop_option=self.current_dragged
                
                print("last_hover_hin is none")
                snap_target=self.current_last_drag_drop_anchor
            
            
            if snap_target.is_draggable:
                #oops, trying to drop an item on the item,
                #reassign
                #or better don't allow.
                snap_target=self.current_last_drag_drop_anchor
                
            if snap_target.key in self.drag_items:
                snap_target=self.current_last_drag_drop_anchor
            
            new_key=snap_target.key
            old_key=self.current_dragged.key
            #if old_key!=new_key:
            #    snap_target = self.current_last_drag_drop_anchor
            
            self.drag_items.pop(old_key)
            
            #swap things around
            if len(snap_target.children)!=0:
                if False:
                    #don't do this, meant for swapping need to look 
                    #at it again.
                    other.snap_target.children[0]
                    
                    snap(other,self.grid[old_key])
                    print("oldkey",old_key)
                    self.drag_items[old_key]=other
                    other.key=old_key
                    self.output_info.append((other,self.grid[old_key]))
            
            snap(self.current_dragged, snap_target)
            
            self.drag_items[snap_target.key]=self.current_dragged
            self.current_dragged.key=new_key
            
            self.current_dragged = None
        
        
        if self.drop_callback!=None:
            self.drop_callback()
        
def bind_grid_events(grid,hover_in,hover_out):
    """bind hover and hover out functions to all elements in the grid"""
    
    # bind the events
    for key1 in grid.keys():
        ob = grid[key1]
        ob.bind(DGG.WITHIN , hover_in, [ob])
        ob.bind(DGG.WITHOUT, hover_out)

def bind_single_events(ob,hover_in,hover_out):
    
    ob.bind(DGG.WITHIN , hover_in, [ob])
    ob.bind(DGG.WITHOUT, hover_out)

def snap(ob, target):

    # this is just some math for nice centering
    lock_pos = get_mid_point(target)
    
    h, w = get_local_center(ob)
    h2,w2=get_local_center(target)
        
    # this does the actual snapping
    
    ob.wrt_reparent_to(target)
    ob.setPos(LVecBase3f(*(-h2+h,-w2+w)))
    
def make_drag_items(self,c):
    # make some squares to be drag/dropped
    c=0
    Ds=[]
    while c < 3:
        col=color_l[c]
        rel_col = colors[col]
        key=str((c,0))
        D=construct_draggable(self.DC,col,rel_col,key)
        Ds.append(D)
        c += 1
    
    col=color_l[0]
    rel_col = colors[col]
    key=str((3,0))+"h"
    D=construct_draggable(self.DC,col,rel_col,key)
    Ds.append(D)
    
    return Ds

def next_free_key(the_dict,drag_items):
    xl=the_dict.keys()
    xl2=[]
    for x in xl:
        xl2.append((the_dict[x],x))
    xl2.sort(key=lambda x : x[0].index)
    c=0
    while True:
        tup=xl2[c]
        if tup[1] not in drag_items:
            return tup[1]
        c+=1

def container_surface(pos=(0,0),grid_key_prefix="this",grid_key="(smooth)"):
    
    F = construct_frame(pos=pos,size=(200,50))
    F.key=grid_key_prefix+grid_key
    return F

def shift_to_make_space(els,parent_pos,pos):
    """weakness at the moment is that this is still
    done in pixels. same as the rest."""
    
    
    # when these get too big, it will disturb how the positioning 
    # is done with position_on and it will change the order
    # in unintended ways, because picking it up will shift the position
    # so much it will change the order. So just picking up and letting
    # go, can alter stuff.
    
    # e.g. pick up first of 4 elements. pick one up, it's now 3 elements.
    # 3 elements get resorted, picked up element will move slightly to the
    # right and now longer be first
    # if dropped immediately it will be inserted as second.
    
    # how to solve this... I would have to keep the old order around
    # for position_on
    # and not drastically resort, until my actually moved distance is 
    # so much I need to move things. Or I don't move things when I pick them up.
    # at least not on the x axis. 
    
    lim = 80 # when things start to get moved
    move_d = 20 # how far they are moved at most 
    
    for x in els:
        el_pos=x.get_pos()
        full=parent_pos+el_pos
        #el_pos = pixel2d.get_relative_point(render2d, el_pos)
        
        d=((full[0]-pos[0])**2)**0.5
        
        if d < lim:
            direc = full[0]-pos[0]
            fac = 1-(d/lim)
            if direc>0:
                np_pos = el_pos+(LVecBase3f(*(fac*move_d,0)))
            else:
                np_pos = el_pos+(LVecBase3f(*(fac*-move_d,0)))
        else:
            np_pos = el_pos
        
        x.set_pos(np_pos)

def create_button(text,position,scale,function, arguments,text_may_change=0,frame_size=(-4.5,4.5,-0.75,0.75)):
    
    position=LVector3(*position)
    button = DirectButton(text=text,
                    pos=position,
                    scale=scale,
                    frameSize=frame_size,
                    textMayChange=text_may_change)#(.9, 0, .75), text="Open"))
                                   #scale=.1, pad=(.2, .2),
                                   #rolloverSound=None, clickSound=None,
                                   #command=self.toggleMusicBox)
    position[0]+=0.1
    
    button.setPos(*position)
    
    if function!=None and arguments!=None:
        arguments=list(arguments)
        button.bind(DGG.B1PRESS,function,arguments)
        
    return button


def create_contents(my_list,DC,grid,color=colors["red"]):
    """
    for elements in a list, create draggable items
    that represent those items and bind them to 
    available sockets?
    """
    for item in my_list:
        D = construct_draggable(DC,
                            drag_type = None,
                            represented_item = str(item),
                            rel_col = color,
                            )
        drag_items = DC.drag_items
        key = next_free_key(grid,DC.drag_items)
        lock(D,grid,drag_items,key)

def get_prefix_from_grid_key(x):
    index = x.find("(")
    prefix = x[:index]
    return prefix

def some_function(elements):
    max_x=len(elements)
    x=0
    my_length=200
    step_size=my_length/max_x
    while x < max_x:
        #15 is from the size of the tile?
        yield ((0.5+x)*(step_size)-15,0,0)
        x+=1
    
def position_on(drag_controller,big_frame,elements):
    my_gen=some_function(elements)
    for x in elements:
        pos=my_gen.__next__()
        x.wrt_reparent_to(big_frame)
        x.last_drag_drop_anchor=big_frame
        #x.is_draggable=True
        x.setPos(pos)
    # ok this is somewhat limiting the things that I want to drop.
    new_elements = list(set(elements))
    assert len(new_elements)==len(elements)
    #elements.sort(key = lambda x : x.getPos()[0])
    big_frame.sorted_elements = elements
    
    # this is necessary for compatibility with the other system
    # that one binds to a position in that grid, 
    # grid(position)
    # this one doesn't have a "grid" so I'm doing 
    # bigframe.key(index)
    
    for i in elements:
        ind = elements.index(i)
        if i.key !=None and i.key in drag_controller.drag_items:
            drag_controller.drag_items.pop(i.key)
        my_new_key=big_frame.key+"("+str(ind)+")"
        drag_controller.drag_items[my_new_key]=i
        i.key=my_new_key

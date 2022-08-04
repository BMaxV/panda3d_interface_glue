#import panda3d.core import *
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectGui import DirectScrolledFrame

from direct.gui.DirectScrolledList import DirectScrolledList

from panda3d.core import Geom, GeomTriangles, GeomLines
from panda3d.core import GeomVertexFormat, GeomVertexData, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import NodePath


from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase import ShowBase

import random

#from panda3d.core import render2d
#from direct.gui.DirectGui import render2d

from panda_interface_glue import drag_main

def draw_shape_2d(shape=None):
    if shape==None:
        shape=()
    
    
    #prepare new interface object container
    tformat=GeomVertexFormat.getV3t2()
    #this is the format we'll be using.
    vdata = GeomVertexData('convexPoly', tformat, Geom.UHStatic)

    #these are access shortcuts
    vertex = GeomVertexWriter(vdata, 'vertex')
    uv = GeomVertexWriter(vdata, "texcoord")
    vdata.setNumRows(2)# define  number of points.
    poly = Geom(vdata)
    ci=0


    p1=[-0.8, 0, 0.5]
    
    p2=[-0.5, 0, 0.5]
        
    verts=[p1,p2]
    
    for p in verts:
        color_t=(255,255,0)
        vertex.addData3(p[0],p[1],p[2])
        uv.addData2(p[0],p[1])
    
    tris = GeomLines(Geom.UHStatic)
    #add index to geometry.
    tris.addVertices(ci,ci+1)
    tris.closePrimitive()
    
    poly.addPrimitive(tris)
    
    snode = GeomNode('Object1')
    snode.addGeom(poly)
    path=NodePath(snode)
    path.reparent_to(render2d)
    #text_obs.append(path)
    return path
    #this should do ti completely.

def display_active_cells(current_active_cells,text_obs,game_d):
    #engine calculates pos 2d. that's not passed on right now.
    #that's why this isn't working.
    
    if "World" in game_d:
        if "active cells" in game_d["World"]:
            #if game_d["World"]["active_cells"]!=current_active_cells:
            current_active_cells=game_d["World"]["active cells"][3]
            
            
            for n in text_obs:
                n.removeNode()
            text_obs=[]
            
            #prepare new interface object container
            tformat=GeomVertexFormat.getV3t2()
            #this is the format we'll be using.
            vdata = GeomVertexData('convexPoly', tformat, Geom.UHStatic)

            #these are access shortcuts
            vertex = GeomVertexWriter(vdata, 'vertex')
            uv = GeomVertexWriter(vdata, "texcoord")
            vdata.setNumRows(len(current_active_cells)*2)
            poly = Geom(vdata)
            ci=0
                        
            target_list=[]
            for c in current_active_cells:
                #text_pos=[-0.8, 0, 0.5-0.1*c_p]
                if c.pos_2d!=None:
                    l=[]
                    for i in c.pos_2d:
                        l.append(i)
                    
                    pos_2d=c.pos_2d
                    pos_2d[2]=pos_2d[1]
                    pos_2d[1]=0
                    
                    target=pos_2d
                    
                    target_list.append([target,c])
            
            target_list.sort(key=lambda x:x[0][2],reverse=True)
            
            c_p=0
            for t in target_list:
                
                text_pos=[-0.8, 0, 0.5-0.1*c_p]
                
                target=t[0]
                c=t[1]
                    
                verts=[text_pos,target]
                
                for p in verts:
                    color_t=(255,255,0)
                    vertex.addData3(p[0],p[1],p[2])
                    uv.addData2(p[0],p[1])
                
                tris = GeomLines(Geom.UHStatic)
                tris.addVertices(ci,ci+1)
                tris.closePrimitive()
                poly.addPrimitive(tris)
                ci+=2
                    
                string=str(c.center[0])[0:4]+","+str(c.center[1])[0:4]+" "+str(c.face_id)
                text=create_textline(string,tuple(text_pos))
                
                text_obs.append(text)
                c_p+=1
            
            snode = GeomNode('Object1')
            snode.addGeom(poly)
            path=NodePath(snode)
            path.reparent_to(render2d)
            text_obs.append(path)
        
    return current_active_cells,text_obs

def destroy_buildmenu(d):
    for key in d:
        el=d[key]
        el.removeNode()

def destroy_inventory(drag_main_container):
    for key in drag_main_container.grid:
        #if type(x_key)==str:
        el=drag_main_container.grid[key]
        el.removeNode()

def destroy_store_interface(drag_main_container):
    
    grids=[ drag_main_container.grid1,
            drag_main_container.grid2,
            ]
            
    for grid in grids:
        for key in grid:
            el=grid[key]
            el.removeNode()

def destroy_trade_interface(drag_main_container):
    
    grids=[ drag_main_container.grid1,
            drag_main_container.grid11,
            drag_main_container.grid2,
            drag_main_container.grid21 ]
            
    for grid in grids:
        for key in grid:
            el=grid[key]
            el.removeNode()

def destroy_crafting_ui(objects):
    for el in objects:
        el.removeNode()

def button_dummy(*args):
    print("button_dummy function",args)

def build_hierarchy_interface(layers=None):
    
    if layers==None:
        #debug default
        
        layers={0:["Alice"],1:["Bob"],2:["Peter","Gabi"]}
    
    
    DC=drag_main.Drag_Container()
    #now to define some "slots"...
    #pos in pixel, left to right
    x_base=50
    ranks=len(layers)
    c=0
    DC.grid={}
    #grid=drag_main.Grid((x_base-30,230),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(4,5))#,"color":drag_main.colors["light_red"]})
            
    #ok what kind of information do I want as I/O?
    #I want both the hierarchy, and the current filling.
    
    #and it probably makes the most sense to keep the hierarchy static
    #and give additional info on who currently occupies it.
    
    elements=[]
    
    while c < ranks:
        layer=layers[c]
        pc=0
        m=len(layer)
        
        
        while pc < m:
            person=layer[pc]
            print("creating")
            location_key=str((c,pc))
            
            #I want the position centered.
            #but that's something I can math later.
            drag_type="person"
            DC.grid[location_key]=drag_main.construct_frame(**{"pos":(x_base+pc*70,70+70*c),"color":drag_main.colors["light_red"]},drag_drop_type=drag_type,key="person")
            
            D=drag_main.construct_draggable(DC,drag_type=drag_type,#,
                            rel_col=drag_main.colors["red"])
                            #represented_item=item)
            
            drag_items=DC.drag_items
            
            drag_main.lock(D,DC.grid,drag_items,location_key)#position
            pc+=1
        c+=1
    print("done")
    return DC
    
def destroy_hierchy_interface(drag_main_container):
    for key in drag_main_container.grid:
        #if type(x_key)==str:
        el=drag_main_container.grid[key]
        el.removeNode()

def delete_step(*args,):
    DC_object,D,key=args[:3]
    print("this works",D,D.represented_item)
    #that's annoying.
    print("trying to delete step")
    
    keys=list(DC_object.drag_items.keys())
    #this fails when the key is none
    #showed up in the case of the plan display.
    #but I will program custom behavior for that.
    #so that should be fine.
    keys.sort()
    
    new_plan=[]
    for this_key in keys:
        ob=DC_object.drag_items[this_key]
        if ob==D:
            continue
        text=ob.represented_item
        
        if this_key==key:
            continue
        new_plan.append(text)
    
    destroy_plan_content(DC_object.drag_items)
    DC_object.drag_items={}
    build_plan_content(DC_object,new_plan)
            

def build_plan_display(plan):
    """ see home thing.
    the toolbox should be a another grid in the same dc container?
    
    
    """
    DC=drag_main.Drag_Container()
    
    
    
    DC.output_list=None
    
    #now to define some "slots"...
    #pos in pixel, left to right
    x_base = 0
    
    #this is the main grid containing the plan.
    #fill the box with some instructions.
    grid = drag_main.Grid((50,400),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(5,1))#,"color":drag_main.colors["light_red"]})
    DC.grid = grid.d
    
    #maybe I should rather look at how I build my interface than building more grids.
    #toolbox_grid containing the instruction blocks
    tool_grid=drag_main.Grid((50,100),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(3,3),grid_key_prefix="toolbox")
    
    #utility boxes to find abstract targets
    
    DC.grid["bin_box"]= drag_main.construct_frame(**{"pos":(400,100)},drag_drop_type=None,key=None)
    DC.grid["search_result_box"]= drag_main.construct_frame(**{"pos":(400,160)},drag_drop_type=None,key=None)
    #DC.grid["feet"]     = drag_main.construct_frame(**{"pos":(x_base+60,150),"color":drag_main.colors["light_red"]},drag_drop_type="feet",key="feet")
    
    #bind all functions for all grid squares.
    #drag_main.bind_grid_events(DC.grid,DC.hover_in,DC.hover_out)
    grid_c=0
    for x in [DC.grid,tool_grid.d]:
        print("x",grid_c)
        drag_main.bind_grid_events(x,DC.hover_in,DC.hover_out)
        grid_c+=1
        
    
    
    #ok so the problem here is that I have somehow built
    #some display stuff into the draggable thing.
    grid = DC.grid
    
    print("myplan",plan)
    
    #two functions I need,
    #delete
    #insert
    # both need to be in DC, I think.
    
    # delete_step deletes a step
    # insert_step inserts a new step
    
    this_plan=plan
    build_plan_content(DC,this_plan)
    
    #make a save button that saves the current text configuration to 
    #a list that I can retrieve.
    pos,scale=(0.3,0,-0.3),0.05
    DC.save_button=create_button("save",pos,scale,save_plan_list,(DC,))
    
    #and the destroy function won't work now.
    
    return DC
    
def save_plan_list(DC,*args):
    keylist=list(DC.drag_items.keys())
    keylist.sort()
    text_list=[]
    for key in keylist:
        DI=DC.drag_items[key]
        text_list.append(DI.represented_item)
    DC.output_list=text_list
    
def build_plan_content(DC,plan):
    grid=DC.grid
    xc=0
    print("Building")
    for x in plan:
        drag_type=None
        key=None
        print("x",x)
        D = drag_main.construct_draggable(DC,drag_type=drag_type,
                            rel_col=drag_main.colors["red"],
                            represented_item=x)#,amount=1)
        
        drag_items = DC.drag_items
        key=str((xc,0))
        drag_main.lock(D,grid,drag_items,key)
        
        #position
        #create a frame? 
        #create text objects displaying stuff
        #add a delete button
        #oh and grabbing an element 
        #should move it and all after it.
        #then there should be a "compress" option
        
        #ok and make a button to delete it from the plan.
        new_pos=list(D.getPos())
        
        #above?
        new_pos[1]+=1
        #up and to the side?
        new_pos[0]+=1
        new_pos[2]+=1
        
        new_pos=[0.5+xc*0.05,0.5,0.5] 
        #this can't look up by key,
        #because then dragging would be nonsense.
        B=create_button("x",new_pos,10,delete_step,(DC,D),frame_size=(-0.6,0.6,-0.6,0.6))
        pos2=(33,-0.2,0.5)
        
        B.reparent_to(D)
        B.setPos(pos2)
                
        xc+=1

def destroy_plan_content(plan_drag_items):
    for key in plan_drag_items:
        ob=plan_drag_items[key]
        ob.removeNode()
        
def destroy_plan_display(plan_ui):
    for key in plan_ui:
        ob=plan_ui[key]
        ob.removeNode()
    #I don't think this cleans up the draggable items?
    #because of C stuff
    

def build_buildmenu(options):
    #naive_test()
    #return 
    x_base = 50
    
    #better do it with buttons?
    pos=(x_base-30,230)#,(60,60)
    rows_collums=(4,5)
    
    offset=(60,60)
    grid_key_prefix="hurr"
    x, y = rows_collums
    d = {}
    c=0
    x_i = 0
    while x_i < x:

        y_i = 0
        while y_i < y and c < len(options):

            dd_type = None

            if x_i == 2:
                dd_type = "red"
            
            pos_i = (-1+0.2*x_i,-0.2, 0.7-0.2*y_i)
            
            key=grid_key_prefix + str((x_i,y_i))
                        
            #ob_thing = construct_frame(**frame_kwargs)
            #self.default_drops.append(key)
            scale=0.1
            
            eh="D"+str(x_i)+","+str(y_i)
            eh=options[c]
            option=options[c]
            button_function=option[0]
            text=option[1][0]
            
            button= create_button(text,pos_i,0.07,button_function,text,frame_size=(-1,1,-1,1))
            
            
            d[key] = button #ob_thing
            
            
            c+=1
            y_i += 1
        x_i += 1

    return d

def build_inventory_ui(inventory={}):
    print("build invent\n\n")
    #ok so this is the main container that defines the functions.
    DC=drag_main.Drag_Container()
    
    #now to define some "slots"...
    #pos in pixel, left to right
    x_base = 50
    
    grid = drag_main.Grid((x_base-30,230),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(4,5))#,"color":drag_main.colors["light_red"]})
    
    DC.grid = grid.d
        
    #snap target frames
    DC.grid["main hand"]= drag_main.construct_frame(**{"pos":(x_base,70),"color":drag_main.colors["light_red"]},drag_drop_type="main hand",key="main hand")
    DC.grid["head"]     = drag_main.construct_frame(**{"pos":(x_base+60,30),"color":drag_main.colors["light_red"]},drag_drop_type="head",key="head")
    DC.grid["off hand"] = drag_main.construct_frame(**{"pos":(x_base+120,70),"color":drag_main.colors["light_red"]},drag_drop_type="weapon",key="off hand")
    DC.grid["chest"]    = drag_main.construct_frame(**{"pos":(x_base+60,90),"color":drag_main.colors["light_blue"]},drag_drop_type="chest",key="chest")
    DC.grid["feet"]     = drag_main.construct_frame(**{"pos":(x_base+60,150),"color":drag_main.colors["light_red"]},drag_drop_type="feet",key="feet")
        
    drag_main.bind_grid_events(DC.grid,DC.hover_in,DC.hover_out)
    
    #ok what do I want/need
    #I want to create the item,
    #I want to assign it to a valid grid tile and snap to that
    #tile
    #and apparently I want to be able to specify
    #both grid and tile, and not just container.:
    
    l=list(DC.grid.keys())
    l.sort()
    
    tps=[]
    for item in inventory:
        detail_dict = inventory[item]
        
        position = detail_dict["position_key"]
        amount = detail_dict["amount"]
        if position == None:
            tps.append(("bag",item,amount))
        else:
            tps.append((position,item))
    
    for tup in tps:
        if len(tup)==3:
            position,item,amount = tup
        else:
            position,item = tup
            amount=1
            
        if position == "bag":
            
            #location keys are in l
            for lkey in l:
                if lkey not in DC.drag_items:
                    if "item_slot_type" in dir(item):
                        drag_type=item.item_slot_type
                        col="red"
                        
                    else:
                        drag_type=None
                        col="green"
                    key=lkey
                    break
                    
        else:
            key = position
             
        if item == None:
            continue
        
        grid = DC.grid
        
        if "item_slot_type" in dir(item):
            drag_type = item.item_slot_type
            col = "red"
        else:
            col = "green"
            drag_type = None
        
        print("draggable inputs",drag_type,col,item,amount)
        
        D = drag_main.construct_draggable(DC,drag_type=drag_type,
                            rel_col=drag_main.colors[col],
                            represented_item=item)
        
                                    
        drag_items = DC.drag_items
        print("lock inputs",D,grid,drag_items,key)
        drag_main.lock(D,grid,drag_items,key)#position
        
        #hier funktioniert das auch.
        
        #ok so I need to get the drop information to the interface somehow.
        #I could od it with a message and the task manager...
        
        #Or I can save it in the object and retrieve it later...
        #the later would probably be more modular.
        #let's try that first.
    
    return DC

def create_contents(the_dict,key_string_prefix,DC,grid,color=drag_main.colors["red"]):
    for item in the_dict:
        #ya don't do this, find any open slot.
        #key="key_string_prefix"+str(item)
        #dis
        D=drag_main.construct_draggable(DC,
                            drag_type=None,
                            represented_item=item,
                            rel_col=color
                            )
        
        drag_items=DC.drag_items
        key=drag_main.next_free_key(grid,DC.drag_items)
        
        drag_main.lock(D,grid,drag_items,key)
        

def build_two_inventories(inventory_self,inventory_other,trade_function,interface_object,trade=True):
    
    DC = drag_main.Drag_Container()
    
    x_base = 50
    
    grid=drag_main.Grid((x_base-30,230),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(3,5),grid_key_prefix="me",owner="self")#,"color":drag_main.colors["light_red"]})
    DC.grid1=grid.d
    drag_main.bind_grid_events(DC.grid1,DC.hover_in,DC.hover_out)
    
    #fairly sure the prefixes do nothing now
    prefix_self="met"
    
    if trade:
        grid=drag_main.Grid((x_base+200,230),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(2,5),grid_key_prefix=prefix_self,owner="self")#,"color":drag_main.colors["light_red"]})
        DC.grid11=grid.d
        drag_main.bind_grid_events(DC.grid11,DC.hover_in,DC.hover_out)
    
    grid=drag_main.Grid((x_base+500,230),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(3,5),grid_key_prefix="other",owner="other")#,"color":drag_main.colors["light_red"]})
    DC.grid2=grid.d
    drag_main.bind_grid_events(DC.grid2,DC.hover_in,DC.hover_out)
    
    #the ts are actually important for the trading...
    prefix_other="othert"
    
    if trade:
        grid=drag_main.Grid((x_base+350,230),(60,60),frame_kwargs={"drag_drop_type":None},rows_collums=(2,5),grid_key_prefix=prefix_other,owner="other")#,"color":drag_main.colors["light_red"]})
        DC.grid21=grid.d
        drag_main.bind_grid_events(DC.grid21,DC.hover_in,DC.hover_out)
    
    #this is to make sure I can drop somewhere that's not my inventory.
    if not trade:
        DC.ignore_ownership=True
    
    return DC,prefix_self,prefix_other

def build_store_interface(inventory_self,inventory_other,trade_function,interface_object):
    DC,prefix_self,prefix_other=build_two_inventories(inventory_self,inventory_other,trade_function,interface_object,trade=False)
    
    create_contents(inventory_self,prefix_self,DC,DC.grid1)
    create_contents(inventory_other,prefix_other,DC,DC.grid2)
    
    return DC
    
def build_trade_interface(inventory_self,inventory_other,trade_function,interface_object):#,trade_function):
    DC,prefix_self,prefix_other=build_two_inventories(inventory_self,inventory_other,trade_function,interface_object,trade=True)
    
    create_contents(inventory_self,prefix_self,DC,DC.grid1)
    create_contents(inventory_other,prefix_other,DC,DC.grid2)
    if False:
        for key in inventory_self:
            item=key
            key="self"+str(key)
            D=drag_main.construct_draggable(DC,
                                represented_item=item)
                                
            grid=DC.grid1
            drag_items=DC.drag_items
            
            drag_main.lock(D,grid,drag_items,key)

        for key in inventory_other:
            
            item=inventory_other[key]
            key="other"+str(key)
            D=drag_main.construct_draggable(DC,drag_type="main hand",
                                rel_col=drag_main.colors["red"],
                                represented_item=item)
                                
            grid=DC.grid2
            drag_items=DC.drag_items
            drag_main.lock(D,grid,drag_items,key)
    
    #ok so the trade function will move
    #the items from the "trade" part to the inventory
    #of the other guy
    #but should it do that *here*?
    #hm, i can just pass the grids as additional arguments.
    
    #more like a barter system, really...
    #those are the wrong thingies...
    #the wrong dicts...
    b=create_button("trade",(0.4,0.5,0.5),0.1,trade_strip,[trade_function,interface_object,DC.drag_items,prefix_self,prefix_other])#trade_function,[DC.grid11,DC.grid21,self,other])
    #create_button(
    DC.button=b
    
    return DC

def trade_strip(real_f,interface_object,drag_items,prefix_self,prefix_other,*args):
    
    l1=[]
    l2=[]
    
    for key in drag_items:
        if prefix_self in key:
            l1.append(drag_items[key].represented_item)
        if prefix_other in key:
            l2.append(drag_items[key].represented_item)
    
    #this adds a trade offer to my output.
    real_f((l1,l2))

def create_text_entry(position,
                        scale,
                        focusInCommand=None,
                        focusOutCommand=None,
                        command=None):
                            
    # that's not saving any work so far...
    # maybe  
    E=DirectEntry(pos=position,
                    scale=scale,
                    focusInCommand=focusInCommand,
                    focusOutCommand=focusOutCommand,
                    command=command
                    )
    return E

def package_my_table(my_table,element_size=1):
    xs=len(my_table[0])/2
    ys=len(my_table)
    xfac=0.4*(element_size)
    yfac=0.2
    canvasSize1=(-0.2, xs*xfac, -ys*yfac, 0.2)
    
    myframe = DirectScrolledFrame(canvasSize=canvasSize1, frameSize=(-.8, .8, 0, .8))
    myframe.setPos(0, 0, 0)
    canvas=myframe.getCanvas()
    elements=[myframe]
    posscale=0.2
    y=0
    for row in my_table:
        x=0
        for element in row:
            el=create_textline(element,(posscale*x*element_size,0,-posscale*y))
            elements.append(el)
            el.reparentTo(canvas)
            x+=1
        y+=1
    return elements

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

def create_log_scroll_list():
    o=DirectScrolledList(pos=LVector3(0.5,-0.55),scale=(0.1,0.1,0.1))
    return o

def create_onscreentext(text="default",pos=(0.5,-0.5),align="right"):
    if align=="right":
        align=TextNode.ARight
    elif align=="left":
        align=TextNode.ALeft
    else:
        raise TypeError
    o=OnscreenText(text=text, scale=.07,
    align=align, pos=pos,
    fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
    return o

def create_textline(text,position=(0.0,0.0,-0.6)):
    tooltip=DirectLabel(text=text,pos=position,scale=(0.1,0.1,0.1),textMayChange=1)
    return tooltip

def create_charge_bar(position=(0.0,0.0,0.5)):
    #like a tooltip, but scale it?
    
    #background=DirectFrame(pos=position,scale=(0.11,0.11,0.11),color=")
    charge_bar=DirectWaitBar(pos=position,scale=(0.1,0.1,0.1))
    charge_bar["range"]=1.0
    charge_bar["value"]=0.0
    charge_bar.setRange()
    charge_bar.setValue()
    
    return charge_bar

def create_tooltip(text):
    print("creating tooltip?!")
    #how is this added to the renderer?
    tooltip=DirectLabel(text=text,pos=(0.0,0.0,-0.5),scale=(0.1,0.1,0.1),textMayChange=1)
    return tooltip
    
def naive_test():
    create_button("hello",(0.5,0.5,0.5),0.1,print,[(0,1,2),(3,4)])
    create_button("-xhello",(-0.5,0.5,0.5),0.1,print,[(0,1,2),(3,4)])
    create_button("-yhello",(0.5,-0.5,0.4),0.1,print,[(0,1,2),(3,4)])
    create_button("-zhello",(0.4,0.5,-0.5),0.1,print,[(0,1,2),(3,4)])
    
    position=LVector2(0,0)
    
    button = DirectButton(text="eh",
                    pos=position,
                    scale=1)
    
def start_key_listening(f,inputs):
    base.buttonThrowers[0].node().setButtonDownEvent("rebindevent")
    base.accept("rebindevent",f,list(inputs))


def end_key_listening(*inputs):
    
    base.buttonThrowers[0].node().setButtonDownEvent("")
    #wait no that's an event name. shit.
    #rebind(inputs[0],inputs[1])
    #return key_or_input


def rebind(eventname,function):
    base.accept(eventname,function)

def key_event_listening():
    #from the manual:
    #https://www.panda3d.org/manual/index.php/Keyboard_Support
    
    def myFunc(keyname):
        #forget about it.
        base.buttonThrowers[0].node().setButtonDownEvent("")
                
    base.buttonThrowers[0].node().setButtonDownEvent("rebindevent")
    base.accept("rebindevent",myFunc)
    
    base.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
    self.accept('keystroke', self.myFunc)
 
    def myFunc(self, keyname):
        print("test?",keyname)
    
    # Get the current keyboard layout.
    # This may be a somewhat expensive operation, so don't call
    # it all the time, instead storing the result when possible.
    map = base.win.get_keyboard_map()
     
    # Use this to print all key mappings
         
    # Find out which virtual key is associated with the ANSI US "w"
    raw_key = map.get_mapped_button("w")
     
    # Get a textual representation for the button
    w_label = map.get_mapped_button_label("w")
    if w_label:
        # There is none, use the event name instead.
        w_label = str(w_button)
    w_label = w_label.capitalize()
     
    # Use this label to tell the player which button to press.
    self.tutorial_text = "Press %s to move forward." % (w_label)
     
    # Poll to check if the button is pressed...
    if base.mouseWatcherNode.is_button_down(w_button):
        print("%s is currently pressed" % (w_label))
     
    # ...or register event handlers
    #self.accept("%s" % (w_button), self.start_moving_forward)
    #self.accept("%s-up" % (w_button), self.stop_moving_forward)
    
    return raw_key,key_name
    
if __name__=="__main__":
    a=1

import random

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

from panda3d.core import TextNode

from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase import ShowBase



#from panda3d.core import render2d
#from direct.gui.DirectGui import render2d

from panda_interface_glue import drag_main

from my_save import sxml_main

def write_example_style(fn="mystyle.xml"):
    
    my_dict = {
    "font":'DelaGothicOne-Regular.ttf',
    "fontpixels":150,
    "foreground color":(0.2,0.2,0.2,1),
    "outline color":(1,1,1,1),
    "outline thickness":3,
    "outline fading":0.5,    
    "frameColor":(0.8,0.8,0.8,1),
    "frameSize":(-3,3,-1,2),
    "frametexturefilename":"gradient_square.png",
    "borderUvWidth":(0.2, 0.2),
    }
    
    sxml_main.write(fn,my_dict)

def load_style(showbase_instance,path="mystyle.xml"):
    # let's assume I'm doing things locally.
    
    # i'm not doing this with css. I'm doing it with my xml loading.
    #sxml_main.load(
    
    
    d = sxml_main.read("mystyle.xml")
    
    
    my_style = {
            "frameColor":(0.8,0.8,0.8,1), # this is default a
            "frameSize":(-3,3,-1,2),
            }
    
    if "frame color" in d:
        my_style["frameColor"] = d["frame color"]
    
    if "frame size" in d:
        my_style["frameSize"]=d["frameSize"]
    
    if "frametexturefilename" in d:
        fn = d["frametexturefilename"]#"gradient_square.png"
        # this is creating the background texture.
        tex = showbase_instance.loader.loadTexture(fn)
        tex.wrap_u = SamplerState.WM_clamp
        tex.wrap_v = SamplerState.WM_clamp
        tex.wrap_w = SamplerState.WM_clamp
        my_style["frameTexture"] = tex
        # give UV width a default.
        my_style["borderUvWidth"] = (0.2, 0.2)
        my_style["relief"] = DGG.TEXTUREBORDER
        
    if "borderUvWidth" in d:
        # bigger number here means smaller border
        my_style["borderUvWidth"] = d["borderUvWidth"]
    
    if "font" in d:
        # this is setting up the font
        fn = d["font"]
        font = showbase_instance.loader.loadFont(fn)
        fontpixels = 100
        
        if "fontpixels" in d:
            fontpixels = d["fontpixels"]
            
        font.setPixelsPerUnit(fontpixels) # increase for font sharpness
        my_style["font"] = font
        # again, defaults.
        my_style["foreground color"] = (0.2,0.2,0.2,1)
        my_style["outline color"] = (1,1,1,1)
            
    if "outline color" in d:
        my_style["outline color"] = d["outline color"]
    
    if "foreground color" in d:
        my_style["foreground color"] = d["foreground color"]
    
    if "font" in my_style:
        # if I have a custom font, make sure to apply my different colors.
        font = my_style["font"]
        font.clear()
        fgc = my_style["foreground color"]
        bgc = my_style["outline color"]
        outline_thickness = 3
        outline_fading = 0.5
        if "outline thickness" in d:
            outline_thickness = d["outline thickness"]
        if "outline fading" in d:
            outline_fading = d["outline fading"]
        font.setFg(fgc)
        font.setOutline(bgc,outline_thickness,outline_fading)
    # first number controls the thickness of the border, 
    # second controls the fading, 0, no transparency, same as the other, fully transparent and you don't see anything.
           
    return my_style
    

def flip_yz(vector):
    new_vector=vector[0],vector[2],vector[1]
    return new_vector

def draw_2d_line(p1,p2,color=(255,255,0)):
    
    
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

    #p1=[-0.8, 0, 0.5]
    #p2=[-0.5, 0, 0.5]
        
    verts=[p1,p2]
    
    for p in verts:
        #color_t=(255,255,0)
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
    

    
def package_my_table(b,my_table,element_spacing=1,table_pos=(0,0,0)):
    """
    ok so, `my_table` is a list of lists of strings that will be converted to
    labels by default.
    if you want to support actions on those things,
    that's first of all difficult because there needs to be 
    an object where the output of that is being passed to.
    
    then it can be defined that an entry in a row should be a button or
    support right click functionality.
    
    """
    xs=len(my_table[0])/2
    ys=len(my_table)
    xfac=0.4*(element_spacing)
    yfac=0.2
    canvasSize1=(-0.2, xs*xfac, -ys*yfac, 0.2)
    
    myframe = DirectScrolledFrame(canvasSize=canvasSize1, frameSize=(-.8, .8, 0, .8))
    
    
    
    myframe.setPos(table_pos)
    canvas=myframe.getCanvas()
    elements=[myframe]
    posscale=0.2
    y=0
    for row in my_table:
        x=0
        for element in row:
                    
            el=create_textline(str(element),(posscale*x*element_spacing,0,-posscale*y))
            elements.append(el)
            el.reparentTo(canvas)
            x+=1
        y+=1
        
    # I kind of want another frame that's also being controlled by the same 
    # horizontal scroll bar but doesn't get scrolled out of view.
    canvasSize2=(-0.2, xfac, 0, 0)
    b.frame1=myframe
    myframe2 = DirectScrolledFrame(canvasSize=canvasSize1, frameSize=(-.8, .8, 0, 0.2), horizontalScroll_command = b.controlOtherFrame)
    b.frame2=myframe2
    #myframe2["horizontalScroll_arguments"]=(myframe,myframe2)
    myframe2.setPos((0,0,0.6))
    
    
    myframe2.horizontalScroll.destroy()
    #myframe2.verticalScroll.destroy()
    #myframe2.guiItem.setHorizontalSlider(myframe.horizontalScroll.guiItem)
    
    canvas=myframe2.getCanvas()
    headers=["a","b","c"]   
    myheaders=[]
    x=0
    y=0
    for element in headers:
         el=create_textline(str(element),(posscale*x*element_spacing,0,0.1))
         myheaders.append(el)
         el.reparentTo(canvas)
         x+=1
    
    
    elements+=myheaders
    
    
    return elements , myframe2

def create_custom_button(mytext,position,function,arguments,style=None):
    """this will be a fully custom button, with text and shit.
    
    This will be moderately awful, since I'm using DirectFrame, because
    I know how hover in and click events work for that one.
    """
    # styling for the text.
    text_node = TextNode("my text node")
    text_node.set_align(2)
    text_node.set_text(mytext)
    if "font" in style:
        my_font = style.pop("font")
        text_node.set_font(my_font)
    
    pop_list = ["foreground color","outline color"]
    
    for x in pop_list:
        if x in style:
            style.pop(x)
    
    
    # default styling for the frame
    
    default_style = {"pos":(0,0,0),
                    "scale":0.05,
                    "frameSize":(-4.5,4.5,-0.75,0.75),
                    "state": DGG.NORMAL,
                    "frameColor": (0.1,0.1,0.1,1),}
    
    # if there is supposed to be a background... 
    # let me see how I did that with the frame wrap.
    
    active_style = dict(default_style)
    active_style.update(style)
    
    mybutton = DirectFrame(**active_style)
    mybutton.bind(DGG.B1PRESS,function,arguments)
    mybutton.setTransparency(1)
    
    
    
    textNodePath = aspect2d.attachNewNode(text_node)
    textNodePath.setScale(default_style["scale"])
    textNodePath.setPos(default_style["pos"])
    
    mybutton.textnodepath=textNodePath
    mybutton.textnode=text_node
    
    return mybutton
    
def create_button(text,position,scale,function, arguments,text_may_change=0,frame_size=(-4.5,4.5,-0.75,0.75)):
    
    position=LVector3(*position)
    button = DirectButton(text=text,
                    pos=position,
                    scale=scale,
                    frameSize=frame_size,
                    textMayChange=text_may_change)#(.9, 0, .75), text="Open"))
                                   #scale=.1, pad=(.2, .2),
                                   #rolloverSound=None, clickSound=None,
                                   #command=self.toggleusicBox)
    #position[0]+=0.1
    
    button.setPos(*position)
    
    if function!=None and arguments!=None:
        arguments=list(arguments)
        button.bind(DGG.B1PRESS,function,arguments)
        
    return button

def create_log_scroll_list():
    o=DirectScrolledList(pos=LVector3(0.5,-0.55),scale=(0.1,0.1,0.1))
    return o

def create_onscreentext(text="default",pos=(0.5,-0.5),align="right",scale=0.07):
    """ok so, all of direct gui is bad and badly documented. I frankly don't understand how the system works.
    I suppose it's very smartly built and modular.
    
    onscreen texts have lots of options specificed.
    
    there is some auto adjusting functions in Directguidlabel.
    but I'm not sure if I can set a margin?
    
    #... maybe directlabel will have a textnode and I can set the font to that?
    textNode.setFont(font)
    """
    
    if align=="right":
        align=TextNode.ARight
    elif align=="left":
        align=TextNode.ALeft
    else:
        raise TypeError
    o=OnscreenText(text=text, scale=scale,
    align=align, pos=pos,
    fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5))
    return o


            
class CyclingList:
    def __init__(self,variable_name,values,base_position):
       
        self.variable_name = variable_name
        self.values = values # if "numbers" change behavior?
        self.current_index = 0
        self.base_position = base_position
        self.build(base_position)
        
        self.elements = []
    
    def cycle(self,direction,*args):
        if direction=="up":
            self.current_index+=1
        else:
            self.current_index-=1
        
        if self.current_index<=-1:
            self.current_index=len(self.values)-1
        if self.current_index>=len(self.values):
            self.current_index=0
        
        self.clean()
        self.build(self.base_position)
        
    def clean(self):
        for x in self.elements:
            x.removeNode()
    
    def get_value(self):
        return self.values[self.current_index]
    
    def build(self,base_position):
        
        scale = (0.05, 0.05, 0.05)
        x,y,z=base_position
        display_variable_name = create_textline(
            self.variable_name , (x-0.3, 0.0, z))
        
        variable_value = self.values[self.current_index]
        
        # this could be search box too.
        # or accept e.g. number values.
        # hm. I think I already built both.
        
        display_variable_value = create_textline(
            variable_value, (x, 0.0, z))
        
        up_button = create_button(
            "up", (x+0.3, 0.0, z+0.05), scale,
             self.cycle, ("up",),frame_size = (-1.5,1.5,-0.75,0.75)
             )
        down_button = create_button(
            "down",(x+0.3, 0.0, z-0.05), scale,
            self.cycle, ("down",),frame_size = (-1.5,1.5,-0.75,0.75)
            )
        
        self.elements=[
        display_variable_name,
        display_variable_value,
        up_button,
        down_button]
    
    def removeNode(self):
        for x in self.elements:
            x.removeNode()


class Framehistogram:
    
    def __init__(self,pos,size=(0.5,0.2,0),barnumber=20,value_range=(0,10),moving=True):
        self.pos = pos
        self.size = size
        self.elements = []
        self.barnumber = barnumber
        self.value_range = value_range
        self.moving=moving
        
    def add_value(self,value):
        
        while len(self.elements) >= self.barnumber:
            x = self.elements.pop(0)
            x.removeNode()
            self.move_bars()
        
        framesize_x = (self.size[0]/self.barnumber)
        framesize_y = self.size[1]
        framesize = (0,framesize_x,0,framesize_y)
        x = (len(self.elements)-self.barnumber/2)*framesize_x
        pos = (self.pos[0]+x,self.pos[1],self.pos[2])
        F = DirectFrame(pos=pos,frameSize=framesize)
        
        value = value-self.value_range[0]
        yscale = value/self.value_range[1]-self.value_range[0]
        
        F.setScale(1,1,yscale)
        
        self.elements.append(F)
        
    def move_bars(self):
        for x in self.elements:
            pos=x.getPos()
            xdiff=self.size[0]/self.barnumber
            npos = (pos[0]-xdiff,pos[1],pos[2])
            x.setPos(npos)


class EntrySearch:
    """
    awysiwyg
    except the object that holds/controls this, needs to
    define an event handler and 
    register some function that *calls* the 'get' function and does
    something with the result.
    
    event_handler = DirectObject.DirectObject()
    event_handler.accept("enter",use_get_and_result)
    
    """
    def __init__(self,values,pos=(0,0,0.3),scale=0.07,):
        self.values=values
        self.mysearch_input=DirectEntry(pos=pos,scale=scale,focus=0)
        
    def removeNode(self):
        self.mysearch_input.removeNode()
        
    def get(self):
        my_text=self.mysearch_input.get()
        
        for x in self.values:
            if my_text in x:
                self.mysearch_input.setText("")
                break
            else:
                x = None
        
        return x

def amount_setter(big_container,big_container_cycle_function,display_amount,base_position,scale,cycle_args_up=("amount", "main", "up"),cycle_args_down=("amount", "main", "down")):
    """ok, so the problem with this thing, is that it makes some assumptions about 
    where it's used.
    
    There needs to be an "owner" object,
    it needs to have a cycle function that handles the button presses.
    and it needs to save the amount number that also should be passed
    in here..
    """
    
    
    amount_ob = create_textline(
        "amount:"+str(display_amount), base_position)
        
    up_pos=list(base_position)
    up_pos[0]+=0.1
    up_pos[2]+=0.05
    a_up = create_button(
        "+", up_pos, scale, 
        big_container_cycle_function, cycle_args_up,frame_size = (-1.5,1.5,-0.75,0.75))
    
    down_pos=list(base_position)
    down_pos[0]+=0.1
    down_pos[2]-=0.05
    a_down = create_button(
        "-", down_pos, scale,
         big_container_cycle_function, cycle_args_down,frame_size = (-1.5,1.5,-0.75,0.75))
    elements = [amount_ob, a_up, a_down]
    return  elements


class ValueObserverUpdater:
    def __init__(self,base_position=(-0.5,0,0.5),offset_vector=(0,0,-0.1),scale=0.05,style=None):
        self.UI_elements = []
        self.base_position = base_position
        self.offset_vector = offset_vector
        self.style = style
        self.old_values = None
        
    def clean(self):
        for x in self.UI_elements:
            methods = dir(x)
            if "destroy" in methods:
                x.destroy()
            elif "removeNode" in methods:
                x.removeNode() 
        self.UI_elements = []
    
    def build(self,values):
        c=0
        m=len(values)
        bp = self.base_position
        ov = self.offset_vector
        if type(values) == list:
            for x in values:
                pos = bp[0]+c*ov[0],bp[1]+c*ov[1],bp[2]+c*ov[2]
                node,nodepath=create_textline(str(value),pos)
                self.UI_elements.append(nodepath)
                
        if type(values) == dict:
            keylist = list(values.keys())
            keylist.sort()
            for key in keylist:
                value=values[key]
                my_text = f"{key}:{value}"
                pos = bp[0]+c*ov[0],bp[1]+c*ov[1],bp[2]+c*ov[2]
                node,nodepath=create_textline(my_text,pos)
                self.UI_elements.append(nodepath)
                

    def main(self,new_values):
        if new_values != self.old_values:
            self.clean()
            self.build(new_values)
            self.old_values = new_values
        

def create_style_collection():
    return my_style_collection

def create_textline(text,position,color=(0.8,0.8,0.8,1),outline_color=(0,0,0,1),outline_geom=(0.1,0.1),make_card=True,card_margin=(0.1,0.1,0.1,0.1),card_color=(0.2,0.2,0.2,0.5),panda_font=None):
    """I kind of want to accept style as a dict, and define keyword args"""
    textnode = TextNode(text)
    
    textnode.set_text(text)
    
    textnode.setTextColor(color)
    textnode.setCardAsMargin(*card_margin)
    textnode.setCardColor(*card_color)
    textnode.setCardDecal(True)
    if panda_font!=None:
        textnode.setFont(panda_font)
    textNodePath = aspect2d.attachNewNode(textnode)
    textNodePath.setScale(0.05)
    textNodePath.setPos(position)
    return textnode, textNodePath

def create_charge_bar(position=(0.0,0.0,0.5)):
    #like a tooltip, but scale it?
    
    #background=DirectFrame(pos=position,scale=(0.11,0.11,0.11),color=")
    charge_bar=DirectWaitBar(pos=position,scale=(0.1,0.1,0.1))
    charge_bar["range"]=1.0
    charge_bar["value"]=0.0
    charge_bar.setRange()
    charge_bar.setValue()
    
    return charge_bar

def make_bars(bars=None,test=False,position=None,scale=None,bar_colors=None):
        
    if position==None:
        position=(0,0,0)
        
    if bars==None and test==True:
        bars={"hunger":0.1,"life":0.9,"mana":0.5,"endurance":0.4}
        bar_colors={"life":(255,0,0,1),"mana":(0,0,255,1),"endurance":(0,255,0,1),"hunger":(255,255,0,1)}
        
    bar_dict={}
    bar_list=[]
    
    if bars !=None:
        c=0
        for x in bars:
            fp=(position[0],position[1],position[2]+c*0.05)
            bar=create_charge_bar(fp)
            bar.setScale(scale)
            bar["barColor"]=bar_colors[x]
            bar.setBarColor()
            bar_dict[x]=bar
            bar_list.append(bar)
            c+=1
            
    return bar_dict,bar_list

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

def key_event_listening(base):
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

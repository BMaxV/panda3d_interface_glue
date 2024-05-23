from direct.gui.DirectGui import DirectFrame
from direct.gui import DirectGuiGlobals as DGG
from direct.showbase import ShowBase
from panda_interface_glue import panda_interface_glue
#from direct.showbase.ShowBaseGlobal import render2


def setup_right_click(F,options,outputlist,config_options=None):
    """
    The way this is supposed to works is, you need a control object
    with a "outputlist" that the right click can write to
    
    then that object needs to grab the output and do whatever with it.
    I guess I could support binding things directly...
    
    I think this is cleaner and it fits with the rest of how I've
    organized my code. binding functions to click events is documented
    so if you want you can build that yourself.   
    
    So:
    
    class MyControl:
        def __init__(self):
            self.my_right_click_outputlist = []
            self.my_frame=DirectFrame(...) 
            setup_right_click(self.my_frame,["Hello","There"],self.my_right_click_outputlist)
    
    config_options should be a dict that fits with "custom button" from "glue"
    
    {"style":style,
    "x-offset":xoffset,
    "scale":scale,
    }
    
    use xoffset and scale to set something up that fits your purpose
    make a PR if the positioning isn't good enough for you.
    """
    F.bind(DGG.B3PRESS, build_stuffs, [F,options,outputlist,config_options])

def write_to_output_list(frame,stuff,outputlist,*args):
    outputlist.append((frame,stuff))

def empty(*args,**kwargs):
    return

def build_stuffs(F1,options,outputlist,config_options,*args):
    xoffset = 0
    my_style = {"frameSize":(-4.5,4.5,-0.5,1.3),}
    if config_options!=None:
        if "xoffset" in config_options:
            xoffset=config_options["xoffset"]
        if "style" in config_options:
            my_style.update(config_options["style"])
        
    right_click_frames = [F1]
    deconstruct_right_click_frames = []
    F1.inside = False
    if "rightclickcreated" in vars(F1):
        return
    else:
        F1.rightclickcreate=True
    c = 0
    m = len(options)
    while c < m:
        
        # get me the render2d instance?
        node = F1
        while "render2d/aspect2d" != str(node.parent):
            node = node.parent
        pos = F1.getPos(aspect2d)
        #frame_size = (-0.3, 0.3, -0.02, 0.02)
        
        pos1 = (pos[0]+0.3+xoffset, 0, pos[2]-0.1*c)
        my_option=options[c]
        #nf = panda_interface_glue.create_textline(my_option,pos)
        #print(my_style)
        nf = panda_interface_glue.create_custom_button(my_option,pos1,empty,[],style=my_style)
        nf.setScale(0.07)
        #nf = DirectFrame(pos=pos1, frameSize=frame_size,state=DGG.NORMAL)
        nf.setBin("gui-popup", 0)
        nf.inside = False
        deconstruct_right_click_frames.append(nf)
        right_click_frames.append(nf)
        c += 1
    
    for my_frame in right_click_frames:
        my_frame.bind(DGG.WITHIN, mark_inside, [my_frame])
        my_frame.bind(DGG.WITHOUT, check_deconstruct, [my_frame,right_click_frames, deconstruct_right_click_frames])
        
    c = 0
    while c < m:
        my_f = deconstruct_right_click_frames[c]
        my_f.bind(DGG.B1PRESS,write_then_deconstruction,[F1,options[c],outputlist,my_f,right_click_frames, deconstruct_right_click_frames,True])
        c+=1

def write_then_deconstruction(origin_frame,stuff,outputlist,frame,check,deconstruct,override=False,*args):
    write_to_output_list(origin_frame,stuff,outputlist)
    check_deconstruct(frame,check,deconstruct,override)

def check_deconstruct(frame,check,deconstruct,override=False,*args):
    frame.inside=False
    destroy_all = True
    for x in check:
        if x.inside:
            destroy_all = False
            break
    
    #print("destroy",destroy_all)
    #print("override",override)
    
    if override == True:
        destroy_all = True
    
    if destroy_all:
        for x in deconstruct:
            x.ignoreAll()
            x.removeNode()

def mark_inside(my_frame,*args):
    my_frame.inside = True
    
def mark_outside(my_frame,*args):
    my_frame.inside = False


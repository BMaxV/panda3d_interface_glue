from direct.showbase import ShowBase
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DGG
from panda_interface_glue import panda_interface_glue as pig
from panda3d.core import SamplerState

class Wrapper:
	def __init__(self):		
		self.b = ShowBase.ShowBase()
		
		# this is creating the background texture.
		tex = loader.loadTexture("gradient_square.png")
		tex.wrap_u = SamplerState.WM_clamp
		tex.wrap_v = SamplerState.WM_clamp
		tex.wrap_w = SamplerState.WM_clamp
		
		# this is setting up the font
		font=self.b.loader.loadFont('DelaGothicOne-Regular.ttf')
		font.setPixelsPerUnit(100) # increase for font sharpness
		
		foreground_color = (0.2,0.2,0.2,1)		
		outline_color = (1,1,1,1)
			
		font.clear()
		font.setFg(foreground_color)
		font.setOutline(outline_color,3,0.5)
		# first number controls the thickness of the border, 
		# second controls the fading, 0, no transparency, same as the other, fully transparent and you don't see anything.
		
		
		my_style={"font":font,
                        "frameColor":(0.8,0.8,0.8,1),
                        "frameSize":(-3,3,-1,2),
                        "borderUvWidth":(0.2, 0.2),# bigger number here means smaller border
                        "frameTexture":tex,
                        "relief":DGG.TEXTUREBORDER,
                        }
		
		# what you will actually use, text, position, function, arguments, style
		my_button = pig.create_custom_button("hello",(-0.5,0,-0.5),print,["hello there",],style=my_style)
		
        
def main():
	W = Wrapper()
	while True:
		W.b.taskMgr.step()
		dt = W.b.clock.dt

if __name__=="__main__":
	main()

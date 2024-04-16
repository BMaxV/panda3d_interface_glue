from direct.showbase import ShowBase
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DGG
from panda_interface_glue import panda_interface_glue as pig
from panda3d.core import SamplerState

class Wrapper:
	def __init__(self):     
		self.b = ShowBase.ShowBase()
		
		# this is using default filenames and default values.
		#pig.write_example_style()
		my_style = pig.load_style(self.b,"mystyle.xml")
		
		# what you will actually use, text, position, function, arguments, style
		my_button = pig.create_custom_button("hello",(-0.5,0,-0.5),print,["hello there",],style=my_style)
		
		my_button.setScale(0.4)
		my_button.textnodepath.setScale(0.4)
		
def main():
	W = Wrapper()
	while True:
		W.b.taskMgr.step()
		dt = W.b.clock.dt

if __name__=="__main__":
	main()

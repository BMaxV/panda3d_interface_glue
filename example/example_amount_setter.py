from direct.showbase import ShowBase
from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectGui import DGG
from panda_interface_glue import panda_interface_glue as pig
from panda3d.core import SamplerState

class Wrapper:
	def __init__(self):     
		self.b = ShowBase.ShowBase()
		
		# this is using default filenames and default values.
		
		my_button = pig.AmountSetter()
        
		
def main():
	W = Wrapper()
	while True:
		W.b.taskMgr.step()
		dt = W.b.clock.dt

if __name__=="__main__":
	main()

import random

from panda_interface_glue import panda_interface_glue as pig
from direct.showbase import ShowBase

# because of import shenanigans this doesn't run in the folder.
# idk... just save it somewhere else, install the module
# then it should work.

class Wrapper:
	def __init__(self):
		
		self.b = ShowBase.ShowBase()
		
		# look at the default arguments for more configuration
		self.score_hist = pig.Framehistogram((0,0,-0.5))
		self.score_hist.add_value(2)
		self.score_hist.add_value(3)
		self.score_hist.add_value(1)
		self.score_hist.add_value(0)
		self.score_hist.add_value(5)
		
		pig.create_button("add a value",(0,0,0),0.05,add_my_random_value,(self.score_hist,))

def add_my_random_value(my_hist,*args):
	r=random.random()*10
	my_hist.add_value(r)

def main():
	W = Wrapper()
	while True:
		W.b.taskMgr.step()

if __name__=="__main__":
	main()

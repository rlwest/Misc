#################### ham cheese production DM ask model ###################

# this builds on the production model
# two productions are added
# the first requests that the declarative memory module retrieves the condiment that the cutomer ordered
# which is stored in declarative memory
# the second production fires when this has happened


import ccm                    # all of the modeling is done within the ccm suite
log=ccm.log()                 # turn on logging (needed for some things, best to leave it on)

from ccm.lib import grid      # import gridworld to create the world
from ccm.lib.actr import *    # import act-r to create the agent

                              # create a subway sandwich bar
                              # note - do not put comments in the drawing of the map

mymap="""
#########
#       #
#       #
#########
"""

class MyCell(grid.Cell):
    def color(self):
        if self.wall: return 'black'
        else: return 'white'
    def load(self,char):      
        if char=='#': self.wall=True


class MyAgent(ACTR):
    focus=Buffer()
    body=grid.Body() 
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    
    def init():
        focus.set('order condiment')
    
    def order_condiment(focus='order condiment'):                                           
        x = raw_input("what condiment would you like on your sandwich? ")   # get input
        condiment = ('customer') + (' ') + x                                # construct chunk
        DM.add (condiment)
        focus.set('sandwich bread')
                
    def bread_bottom(focus='sandwich bread'):   
        print "I have a piece of bread"         
        focus.set('sandwich cheese')    

    def cheese(focus='sandwich cheese'):        
        print "I have put cheese on the bread"  
        focus.set('sandwich ham')

    def ham(focus='sandwich ham'):
        print "I have put  ham on the cheese"
        focus.set('sandwich condiment')

    def condiment(focus='sandwich condiment'):
        print "recalling the order"
        DM.request('customer ?')                # retrieve a chunk from DM into the DM buffer
        focus.set('customer condiment')         # ? means that slot can match any content

    def order(focus='customer condiment', DMbuffer='customer ?condiment'):  # match to DMbuffer as well
        print "I recall they wanted......."                                 # put slot 2 value in ?condiment
        print condiment             
        print "i have put the condiment on the sandwich"
        focus.set('sandwich bread_top')

    def bread_top(focus='sandwich bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('stop')    

    def stop_production(focus='stop'):
        self.stop()

subway=grid.World(MyCell,map=mymap)   # name the world
tim=MyAgent()                         # name the agent
subway.add(tim,x=3,y=1)               # add the agent to the world
##ccm.display(subway)                   # turn on a visualization of the world
subway.run()                          # turn on the world

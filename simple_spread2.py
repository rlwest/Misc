#################### ham cheese forgetting DM model ###################

# this model turns on the subsymbolic processing for DM, which causes forgetting


import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(ccm.Model):
    pass

#####
# create an act-r agent

class MyAgent(ACTR):
    focus=Buffer()

    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=0.05,threshold=1)     # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=0.0,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)       # turn on for DM subsymbolic processing


    dm_spread=DMSpreading(DM,focus)                  # turn on spreading activation for DM from focus
    dm_spread.strength=2                            # set strength of activation for buffers
    dm_spread.weight[focus]=1                       # set weight to adjust for how many slots in the buffer
                                                     # usually this is strength divided by number of slots

    def init():
        DM.add('isa:customer c:mustard')
        DM.add('isa:customer c:ketchup')
        focus.set('isa:sandwich i:bread')
        
    def bread_bottom(focus='isa:sandwich i:bread'):   
        print "I have a piece of bread"
        focus.set('isa:sandwich i:cheese')    

    def cheese(focus='isa:sandwich i:cheese'):        
        print "I have put cheese on the bread"  
        focus.set('isa:sandwich i:ham')

    def ham(focus='isa:sandwich i:ham'):
        print "I have put  ham on the cheese"
        focus.set('isa:customer i:condiment')         
                                        
    def condiment(focus='isa:customer i:condiment'):  # customer will spread activation to 'customer mustard'
        print "recalling the order"
        DM.request('isa:customer c:?')                # request gets boost from spreading activation 
        focus.set('isa:sandwich i:x') 

    def order(focus='isa:sandwich i:x', DMbuffer='isa:customer c:?condiment'):  
        print "I recall they wanted......."         
        print condiment             
        print "i have put the condiment on the sandwich"
        focus.set('isa:sandwich i:bread_top')

    def forgot(focus='isa:sandwich i:x', DMbuffer=None, DM='error:True'):
        print "I recall they wanted......."
        print "I forgot"
        focus.set('stop')

    def bread_top(focus='isa:sandwich i:bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('isa:stop')               

    def stop_production(focus='isa:stop'):
        self.stop()

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

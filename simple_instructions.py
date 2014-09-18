#################### ham cheese instruction model ###################

# this model uses the contents of DM to decide what to do next
# the productions are generic and capable of following any instructions from DM

import ccm      
log=ccm.log(html=True)   

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
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    pm_comp=PMCompile(keep='focus',request='DM.request',retrieve='DMbuffer')
    def init():                                             
        DM.add ('cue:start step:bread_bottom')                     
        DM.add ('cue:bread_bottom step:cheese')
        DM.add ('cue:cheese step:ham')
        DM.add ('cue:ham step:bread_top')
        DM.add ('cue:bread_top step:finished')
        DM.add ('cue:finished step:stop')
        focus.set('begin')
    
    def start_sandwich(focus='begin'):
        #print 'start_sandwich'  
        DM.request('cue:start step:?')    
        focus.set('remember')
   
    def remember_steps(focus='remember', DMbuffer='cue:?cue!finished step:?step',DM='busy:False'):
        #print 'remember_steps',cue,step   
        DM.request('cue:?step cue:?')   

    def finished (focus='remember', DMbuffer='cue:finished'):
        #print 'finished'   
        focus.set('begin')
        DMbuffer.clear()
        print "I have made a ham and cheese sandwich"              





tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run(5)                               # run the environment
ccm.finished()                             # stop the environment

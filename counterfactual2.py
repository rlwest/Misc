#################### ham cheese instruction model ###################

# this model uses the contents of DM to decide what to do next
# the productions are generic and capable of following any instructions from DM

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
    Ibuffer=Buffer()                            # create imaginal buffer
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    
    def init():                                             
        DM.add ('start in_car')          # gets in car           
        DM.add ('in_car glasses')        # then puts on glasses
        DM.add ('glasses red_light')     # then runs red light
        DM.add ('red_light dead')        # then kills someone
        DM.add ('dead stop')             # the end

        DM.add ('in_car cause')
        DM.add ('red_light cause')
        DM.add ('dead cause')
        focus.set('begin')
    
    def start_thinking(focus='begin'):
        print 'start'  
        DM.request('? stop')    
        focus.set('remember')
   
    def remember_steps(focus='remember', DMbuffer='?step ?cue!start',DM='busy:False'):
        print 'remember_steps = ',cue,step   
        DM.request('?step cause:?')
        Ibuffer.set('?step ?cue')
        focus.set('evaluate')

    def evaluate(focus='evaluate', Ibuffer='?step ?cue',DM='busy:False'):
        print 'check for causal relationship'
        DM.request('?step cause')
        focus.set('undo')

    def undo(focus='undo', Ibuffer='?step ?cue',DMbuffer='?action cause',DM='busy:False'):
        print step,' is significant'
        DM.request('? ?step')
        focus.set('remember')

    def no_undo(focus='undo', Ibuffer='?step ?cue',DM='error:True'):
        print step,' is not significant'
        DM.request('? ?step')
        focus.set('remember')

    def finished (focus='remember', DMbuffer='? start'):
        print 'finished'   
        focus.set('stop')
        DMbuffer.clear()
        print "I have traced the event backwards"              

    def stop_production(focus='stop'):
        self.stop()



tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

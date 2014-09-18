
                                      #################### SGOMS ###################

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):
    pass

class MyAgent(ACTR):
    Focusbuffer=Buffer()
    Contextbuffer=Buffer()
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer    
    
    def init():                                             
        DM.add ('isa:list                   cue:start         step:hamcheese')                     
        DM.add ('isa:list                   cue:hamcheese     step:cheese')
        DM.add ('isa:list                   cue:cheese        step:finished_list')

        DM.add ('planning_unit:hamcheese    cue:start         step:bread')                     
        DM.add ('planning_unit:hamcheese    cue:bread         step:cheese')
        DM.add ('planning_unit:hamcheese    cue:cheese        step:ham')
        DM.add ('planning_unit:hamcheese    cue:ham           step:bread')
        DM.add ('planning_unit:hamcheese    cue:bread         step:finished_planning_unit_unit')
        

        DM.add ('planning_unit:cheese       cue:start         step:bread')                     
        DM.add ('planning_unit:cheese       cue:bread         step:cheese')
        DM.add ('planning_unit:cheese       cue:cheese        step:bread')
        DM.add ('planning_unit:cheese       cue:bread         step:finished_planning_unit_unit')
        
        Contextbuffer.set('planning_unit:hamcheese') # context = planning unit
        Focusbuffer.set('cue:start')

########################## productions for executing a planning unit       


    def request_first_unit_task(Focusbuffer='cue:start',
                                Contextbuffer='planning_unit:?planning_unit'):
        DM.request('planning_unit:?planning_unit cue:start step:?') # request the first unit task for the planning unit from DM
        Focusbuffer.set('state:unit_task')
        print 'start planning_unit = ', planning_unit


        
    def retrieve_unit_task(Focusbuffer='state:unit_task',
                           DMbuffer='planning_unit:?planning_unit cue:?cue!finished step:?step', # retrieve unit task
                           DM='busy:False'):
        Focusbuffer.set('planning_unit:?planning_unit unit_task:?step task_goal:start')     # carry out the unit task
        print 'unit_task = ',step


        
    def next_unit_task(Focusbuffer='unit_task:?step task_goal:complete',# match on the unit task being "complete"
                       Contextbuffer='planning_unit:?planning_unit'): 
        DM.request('planning_unit:?planning_unit cue:?step step:?')     # request next unit task
        Focusbuffer.set('state:unit_task')                              # match to retrieve_unit_task production
        print 'finished unit task = ',step

        
############################ unit tasks - these can be used by any planning unit

########### this is the last unit task in all planning units

    def finished_planning_unit(Focusbuffer='unit_task:finished_planning_unit_unit task_goal:start'):
        print 'all done'      
        Focusbuffer.set('stop')

    def abort_planning_unit(Focusbuffer='unit_task:?unit_task task_goal:?task_goal',utility=-0.3):
        print 'aborted unit task= ',unit_task,'task goal= ',task_goal     
        Focusbuffer.set('stop')    

#### these are specific unit tasks

## bread bottom (used twice for top and bottom of sandwich
        
    def bread1(Focusbuffer='unit_task:bread task_goal:start'):
        print 'find the bread'      
        Focusbuffer.set('unit_task:bread task_goal:find')        
    def bread2(Focusbuffer='unit_task:bread task_goal:find'):
        print 'take it out of the bag'      
        Focusbuffer.set('unit_task:bread task_goal:take')       
    def bread3(Focusbuffer='unit_task:bread task_goal:take'):
        print 'add it to sandwich'      
        Focusbuffer.set('unit_task:bread task_goal:complete')
        
## cheese
        
    def cheese(Focusbuffer='unit_task:cheese task_goal:start'):
        print 'cheese'
        Focusbuffer.set('unit_task:cheese task_goal:complete')
        
## ham (not used for the cheese sandwich)
        
    #def ham(Focusbuffer='unit_task:ham task_goal:start'):
    #    print 'ham'
    #    Focusbuffer.set('unit_task:ham task_goal:complete')




tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

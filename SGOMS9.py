
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

        DM.add ('planning_unit:hamcheese    cue:start         step:bread_bottom')                     
        DM.add ('planning_unit:hamcheese    cue:bread_bottom  step:cheese')
        DM.add ('planning_unit:hamcheese    cue:cheese        step:ham')
        DM.add ('planning_unit:hamcheese    cue:ham           step:bread_top')
        DM.add ('planning_unit:hamcheese    cue:bread_top     step:finished_planning_unit_unit')
        

        DM.add ('planning_unit:cheese       cue:start         step:bread_bottom')                     
        DM.add ('planning_unit:cheese       cue:bread_bottom  step:cheese')
        DM.add ('planning_unit:cheese       cue:cheese        step:bread_top')
        DM.add ('planning_unit:cheese       cue:bread_top     step:finished_planning_unit_unit')
        
        Contextbuffer.set('planning_unit:hamcheese')
        Focusbuffer.set('planning_unit:hamcheese state:first_planning_unit')

########################## productions for executing a planning unit       

    def retrieve_planning_unit(Focusbuffer='planning_unit:?planning_unit state:first_planning_unit'):
        print 'start planning_unit = ', planning_unit
        DM.request('planning_unit:?planning_unit cue:start step:?') # request the first unit task for the planning unit from DM
        Focusbuffer.set('planning_unit:?planning_unit state:unit_task')
        
    def retrieve_unit_task(Focusbuffer='planning_unit:?planning_unit state:unit_task',
                           DMbuffer='cue:?cue!finished step:?step', # retrieve unit task
                           DM='busy:False'):
        print 'unit_task = ',step
        Focusbuffer.set('planning_unit:?planning_unit unit_task:?step task_goal:start action:go') # carry out the unit task

    def next_unit_task(Focusbuffer='planning_unit:?planning_unit unit_task:?step task_goal:complete'): # match on the unit task being "complete"
        print 'finished unit task = ',step
        DM.request('cue:?step step:?')     # request next unit task
        Focusbuffer.set('planning_unit:?planning_unit state:unit_task') # match to retrieve_unit_task production
        
    def finished_planning_unit(Focusbuffer='planning_unit:?planning_unit unit_task:?step task_goal:end'): # match on end of unit tasks
        print 'end of planning unit' 
        Focusbuffer.set('state:constraints') # next planning unit

        
############################ unit tasks - these can be used by any planning unit

## bread bottom
        
    def bread_bottom(Focusbuffer='planning_unit:?planning_unit unit_task:bread_bottom task_goal:start'):
        print 'find the bread'      
        Focusbuffer.set('planning_unit:?planning_unit unit_task:bread_bottom task_goal:find')        
    def bread_bottom2(Focusbuffer='planning_unit:?planning_unit unit_task:bread_bottom task_goal:find'):
        print 'take it out of the bag'      
        Focusbuffer.set('planning_unit:?planning_unit unit_task:bread_bottom task_goal:take')       
    def bread_bottom3(Focusbuffer='planning_unit:?planning_unit unit_task:bread_bottom task_goal:take'):
        print 'put it on the plate'      
        Focusbuffer.set('planning_unit:?planning_unit unit_task:bread_bottom task_goal:complete')
        
## cheese
        
    def cheese(Focusbuffer='planning_unit:?planning_unit unit_task:cheese task_goal:start'):
        print 'cheese'
        print planning_unit
        Focusbuffer.set('planning_unit:?planning_unit unit_task:cheese task_goal:complete')
        
## ham
        
    def ham(Focusbuffer='planning_unit:?planning_unit unit_task:ham task_goal:start'):
        print 'ham'
        print planning_unit
        Focusbuffer.set('planning_unit:?planning_unit unit_task:ham task_goal:complete')

## bread top                                            
        
    def bread_top(Focusbuffer='planning_unit:?planning_unit unit_task:bread_top task_goal:start'):
        print 'bread_top'
        print planning_unit
        Focusbuffer.set('planning_unit:?planning_unit unit_task:bread_top task_goal:end')




tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

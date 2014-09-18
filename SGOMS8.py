
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
        DM.add ('planning_unit:hamcheese    cue:start         step:bread_bottom')                     
        DM.add ('planning_unit:hamcheese    cue:bread_bottom  step:cheese')
        DM.add ('planning_unit:hamcheese    cue:cheese        step:ham')
        DM.add ('planning_unit:hamcheese    cue:ham           step:bread_top')
        DM.add ('planning_unit:hamcheese    cue:bread_top     step:finished_planning_unitning_unit')
        DM.add ('planning_unit:hamcheese    cue:finished      step:stop')

        DM.add ('planning_unit:cheese       cue:start         step:bread_bottom')                     
        DM.add ('planning_unit:cheese       cue:bread_bottom  step:cheese')
        DM.add ('planning_unit:cheese       cue:cheese        step:bread_top')
        DM.add ('planning_unit:cheese       cue:bread_top     step:finished_planning_unitning_unit')
        DM.add ('planning_unit:cheese       cue:finished      step:stop')
        
        DM.add ('constraint:jim planning_unit:hamcheese')
        DM.add ('constraint:tom planning_unit:cheese')
        
        Contextbuffer.set('constraint:jim')
        Focusbuffer.set('state:constraints')

    def check_constraints(Focusbuffer='state:constraints',
                          Contextbuffer='constraint:?constraint'): # constraints are in the buffer
        print 'the constraint is', constraint
        DM.request('constraint:?constraint planning_unit:?') # request a planning unit from DM that fits the constraints
        Focusbuffer.set('state:planning_unit')


    def retrieve_planning_unitning_unit(Focusbuffer='state:planning_unit', 
                               DMbuffer='constraint:?constraint planning_unit:?planning_unit',  # retrieve the planning unit
                               DM='busy:False'):
        print 'start planning_unit = ', planning_unit
        DM.request('planning_unit:?planning_unit cue:start step:?') # request the first unit task for the planning unit from DM
        Focusbuffer.set('state:unit_task')
        
    def retrieve_unit_task(Focusbuffer='state:unit_task',
                           DMbuffer='cue:?cue!finished step:?step', # retrieve unit task
                           DM='busy:False'):
        print 'unit_task = ',step
        Focusbuffer.set('unit_task:?step task_goal:start action:go') # carry out the unit task


    def next_unit_task(Focusbuffer='unit_task:?step task_goal:complete'): # match on the unit task being "complete"
        print 'finished planning_unit = ',step
        Focusbuffer.set('state:unit_task')
        DM.request('cue:?step step:?') # request next unit task
        
    def finished_unit_task(Focusbuffer='unit_task:?step task_goal:end'): # match on end of unit tasks
        print 'end' 
        Contextbuffer.set('constraint:tom') # change constraints
        Focusbuffer.set('state:constraints') # next planning unit

        
        
############################ unit tasks - these can be used by any planning unit

## bread bottom
        
    def bread_bottom(Focusbuffer='unit_task:bread_bottom task_goal:start'):
        print 'find the bread'      
        Focusbuffer.set('unit_task:bread_bottom task_goal:find')        
    def bread_bottom2(Focusbuffer='unit_task:bread_bottom task_goal:find'):
        print 'take it out of the bag'      
        Focusbuffer.set('unit_task:bread_bottom task_goal:take')       
    def bread_bottom3(Focusbuffer='unit_task:bread_bottom task_goal:take'):
        print 'put it on the plate'      
        Focusbuffer.set('unit_task:bread_bottom task_goal:complete')
        
## cheese
        
    def cheese(Focusbuffer='unit_task:cheese task_goal:start'):
        print 'cheese'      
        Focusbuffer.set('unit_task:cheese task_goal:complete')
        
## ham
        
    def ham(Focusbuffer='unit_task:ham task_goal:start'):
        print 'ham'      
        Focusbuffer.set('unit_task:ham task_goal:complete')

## bread top                                            
        
    def bread_top(Focusbuffer='unit_task:bread_top task_goal:start'):
        print 'bread_top'      
        Focusbuffer.set('unit_task:bread_top task_goal:end')




tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

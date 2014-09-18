
                                      #################### SGOMS ###################

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):
    bread=ccm.Model(isa='bread',location='on_counter')
    cheese=ccm.Model(isa='cheese',location='on_counter')
    ham=ccm.Model(isa='ham',location='on_counter')
    bread_top=ccm.Model(isa='bread_top',location='on_counter')

class MotorModule(ccm.Model):     
    def do_bread(self):           
        yield 2                   
        print "do the bread"
        self.parent.parent.bread.location='on_plate'    
    def do_cheese(self):     
        yield 2                   
        print "do the cheese"
        self.parent.parent.cheese.location='on_plate'   
    def do_ham(self):     
        yield 2
        print "do the ham"
        self.parent.parent.ham.location='on_plate'
    def do_bread_top(self):     
        yield 2
        print "do the bread on top"
        self.parent.parent.bread_top.location='on_plate'

class MyAgent(ACTR):
    Focusbuffer=Buffer()
    Contextbuffer=Buffer()
    DMbuffer=Buffer()   
    DM=Memory(DMbuffer)
    Motorbuffer=Buffer 
    Motor=MotorModule(Motorbuffer)
    
    
    def init():                                             
        DM.add ('isa:list                   cue:start         step:hamcheese')                     
        DM.add ('isa:list                   cue:hamcheese     step:cheese')
        DM.add ('isa:list                   cue:cheese        step:finished_list')

        DM.add ('planning_unit:hamcheese_sandwich    cue:start         step:bread_bottom')                     
        DM.add ('planning_unit:hamcheese_sandwich    cue:bread_bottom  step:cheese')
        DM.add ('planning_unit:hamcheese_sandwich    cue:cheese        step:ham')
        DM.add ('planning_unit:hamcheese_sandwich    cue:ham           step:bread_top')
        DM.add ('planning_unit:hamcheese_sandwich    cue:bread_top     step:finished_planning_unit_unit')
        

        DM.add ('planning_unit:ham_sandwich          cue:start         step:bread_bottom')                     
        DM.add ('planning_unit:ham_sandwich          cue:bread_bottom  step:ham')
        DM.add ('planning_unit:ham_sandwich          cue:ham           step:bread_top')
        DM.add ('planning_unit:ham_sandwich          cue:bread_top     step:finished_planning_unit_unit')
        
        Contextbuffer.set('status:ok planning_unit:hamcheese_sandwich') # context = planning unit
        Focusbuffer.set('cue:start')
        Motorbuffer.set('state:internal') # this keeps track of when the focus is on the environment


########################## productions for the failure of a unit task

############ this production triggers a new planning unit to cope with the failure
############ this would be used for a planning unit that must be done immediatly if another fails
        
    def cheese_failure(Focusbuffer='state:fail unit_task:?unit_task task_goal:?task_goal',
                       Contextbuffer='status:problem planning_unit:hamcheese'):
        Contextbuffer.set('status:ok planning_unit:ham_sandwich') # new planning unit
        #Focusbuffer.set('unit_task:bread_bottom task_goal:complete') #start in the middle
        Focusbuffer.set('cue:start') #start at the begining


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

# this is the last unit task in all planning units
    def finished_planning_unit(Focusbuffer='unit_task:finished_planning_unit_unit task_goal:start'):
        print 'all done'      
        Focusbuffer.set('stop')

# this fires if a unit task production fails to fire
    def abort_planning_unit(Focusbuffer='unit_task:?unit_task task_goal:?task_goal',
                            Motorbuffer='state:internal',utility=-0.5): # don't fire if waiting for a motor action to finish
        print 'aborted unit task= ',unit_task,'task goal= ',task_goal     
        Focusbuffer.set('state:fail unit_task:?unit_task task_goal:?task_goal')
        Contextbuffer.set('status:problem planning_unit:hamcheese')


#### these are specific unit tasks
#### (note - the same unit task cannot be repeated in a planning unit or an error can occur
####   but the same unit task can be used by different planning units)

## bread bottom 
        
    def bread1(Focusbuffer='unit_task:bread_bottom task_goal:start'):
        print 'find the bread'      
        Focusbuffer.set('unit_task:bread_bottom task_goal:find')        
    def bread2(Focusbuffer='unit_task:bread_bottom task_goal:find'):
        print 'take it out of the bag'      
        Focusbuffer.set('unit_task:bread_bottom task_goal:take')       
    def bread3(Focusbuffer='unit_task:bread_bottom task_goal:take'):
        print 'add it to sandwich'
        Motor.do_bread()
        Focusbuffer.set('unit_task:bread_bottom task_goal:put')
        Motorbuffer.set('state:external')
    def bread4(Focusbuffer='unit_task:bread_bottom task_goal:put', bread='location:on_plate'):
        print 'done'
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
        print 'bread on top'      
        Focusbuffer.set('unit_task:bread_top task_goal:complete')


tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

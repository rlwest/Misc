
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
        yield 1                   
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
    Visualbuffer=Buffer
    
    
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

        DM.add ('unit_task:bread location:on_counter')
        
        Contextbuffer.set('status:ok planning_unit:hamcheese_sandwich') # context = planning unit
        Focusbuffer.set('cue:start')
        Motorbuffer.set('state:internal') # this keeps track of when the focus is on the environment


########################## productions for the failure of a unit task

############ this production triggers a new planning unit to cope with the failure
############ this would be used for a planning unit that must be done immediatly if another fails
        
    def recovery_procedure(Focusbuffer='state:fail unit_task:?unit_task task_goal:?task_goal',
                           Contextbuffer='status:problem planning_unit:hamcheese'):
        Contextbuffer.set('status:ok planning_unit:ham_sandwich') # new planning unit
        Focusbuffer.set('cue:start') #start at the begining


########################## productions for executing a planning unit       

# unit task cycle productions

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



# producitions that fire when no unit task matches        

# this fires if a unit task production fails to fire
    def abort_planning_unit(Focusbuffer='unit_task:?unit_task task_goal:?task_goal',
                            Motorbuffer='state:not_waiting',############
                            Contextbuffer='planning_unit:?planning_unit',
                            utility=-0.5):
        print 'aborted unit task= ',unit_task,'task goal= ',task_goal     
        Focusbuffer.set('state:fail unit_task:?unit_task task_goal:?task_goal')
        Contextbuffer.set('status:problem planning_unit:hamcheese')
        DM.add('state:fail planning_unit:?planning_unit unit_task:?unit_task task_goal:?task_goal')
        #### add a report in DM

# this fires if the system is focused on monitering for a result
    def focus(Focusbuffer='unit_task:?unit_task task_goal:?task_goal',
                            Motorbuffer='state:waiting',################
                            utility=-0.5):
        print 'focus'   

# this stops looping based on a repeating problem
    def bread_flag2(Focusbuffer='unit_task:?unit_task task_goal:?task_goal',
                    DMbuffer='state:fail planning_unit:?planning_unit unit_task:?unit_task task_goal:?task_goal',
                    utility=1.5):
        print 'I remember an issue'
        print 'state:fail',' planning_unit:',planning_unit,' unit_task:',unit_task,' task_goal:',task_goal
        Focusbuffer.set('stop')


# this is actually the last unit task in all planning units
    def finished_planning_unit(Focusbuffer='unit_task:finished_planning_unit_unit task_goal:start'):
        print 'all done'      
        Focusbuffer.set('stop')


#### these are specific unit tasks
#### (note - the same unit task cannot be repeated in a planning unit or an error can occur
####   but the same unit task can be used by different planning units)

## bread bottom 
        
    def bread_start(Focusbuffer='unit_task:bread_bottom task_goal:start'):
        print 'start bread'
        DM.request('state:fail planning_unit:?planning_unit unit_task:bread_bottom task_goal:?task_goal')
        Focusbuffer.set('unit_task:bread_bottom task_goal:find_bread')

    def bread_find(Focusbuffer='unit_task:bread_bottom task_goal:find_bread',
                   bread='location:on_counter'): 
        print 'bread is in start place'
        Focusbuffer.set('unit_task:bread_bottom task_goal:move_finished')
        Motorbuffer.set('state:waiting')########
        Motor.do_bread()

    def bread_moved(Focusbuffer='unit_task:bread_bottom task_goal:move_finished',
                    bread='location:on_plate'): 
        print 'bread is in end place'
        Focusbuffer.set('unit_task:bread_bottom task_goal:complete')
        Motorbuffer.set('state:not_waiting')##############
        DM.add('unit_task:bread location:on_plate')

        
## cheese
        
    #def cheese(Focusbuffer='unit_task:cheese task_goal:start'):
    #    print 'cheese'
    #    Focusbuffer.set('unit_task:cheese task_goal:complete')
        
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

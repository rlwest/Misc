
                                      #################### SGOMS ###################
#This module allows you to comment out task units and switch to the second planning unit
#I have commented out the eval_cond which indicates that there is a runway incursion (pilot cannot stop in time to avoid it)
#by switching to the second planning unit the runway collision is avoided.

import ccm      
log=ccm.log()

from ccm.lib.actr import *

class MyEnvironment(ccm.Model):
    pass

class MyAgent(ACTR):
    Focusbuffer=Buffer()
    Contextbuffer=Buffer()
    DMbuffer=Buffer()                           #  a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)       #  DM connected to its buffer

    def init():                                             
        DM.add ('isa:list                   cue:start         step:landing')                     
        DM.add ('isa:list                   cue:landing       step:turn_final')
        DM.add ('isa:list                   cue:turn_final    step:finished_list')

        DM.add ('planning_unit:landing    cue:start         step:turn_final')
        DM.add ('recall runway_seven_nine')
        DM.add ('planning_unit:landing    cue:turn_final    step:eval_cond')
        DM.add ('planning_unit:landing    cue:eval_cond     step:dir_control')
        DM.add ('planning_unit:landing    cue:dir_control   step:glidescope')
        DM.add ('planning_unit:landing    cue:glidescope    step:touchdown') 
        DM.add ('planning_unit:landing    cue:touchdown     step:finished_planning_unit_unit')
        #DM.add ('planning_unit:landing    cue:finished_planning_unit_unit     step:end')
        

        DM.add ('planning_unit:short_runway       cue:start         step:turn_final')                     
        DM.add ('planning_unit:short_runway       cue:turn_final    step:eval_cond_incursion')
        DM.add ('planning_unit:short_runway       cue:eval_cond_incursion     step:dir_control')
        DM.add ('planning_unit:short_runway       cue:dir_control   step:glidescope')
        DM.add ('planning_unit:short_runway       cue:glidescope    step:touch_and_go')
        DM.add ('planning_unit:short_runway       cue:touch_and_go  step:finished_planning_unit_unit')
        #DM.add ('planning_unit:short_runway       cue:finished_planning_unit_unit  step:end')
        
        Contextbuffer.set('status:ok planning_unit:landing') # context = planning unit
        Focusbuffer.set('cue:start')
        

########################## productions for the failure of a unit task

############ this production triggers a new planning unit to cope with the failure
############ this would be used for a planning unit that must be done immediatly if another fails
        
    def landing_failure(Focusbuffer='state:fail unit_task:?unit_task task_goal:?task_goal',
                Contextbuffer='status:problem planning_unit:landing'):
        Contextbuffer.set('status:ok planning_unit:short_runway') # new planning unit
        #Focusbuffer.set('unit_task:turn_final task_goal:complete') #start in the middle
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

########### this is the last unit task in all planning units

    def finished_planning_unit(Focusbuffer='unit_task:finished_planning_unit_unit task_goal:start'):
        print 'all done'      
        Focusbuffer.set('stop')

########### this fires if a unit task production fails to fire

    def abort_planning_unit(Focusbuffer='unit_task:?unit_task task_goal:?task_goal',utility=-0.5):
        print 'aborted unit task= ',unit_task,'task goal= ',task_goal     
        Focusbuffer.set('state:fail unit_task:?unit_task task_goal:?task_goal')
        Contextbuffer.set('status:problem planning_unit:landing')

#### these are specific unit tasks (the same unit task cannot be repeated in a planning unit or an error can occur)
############################ unit tasks
## turn final
    def forgot(Focusbuffer='unit_task:turn_final task_goal:start', DMbuffer=None, DM='error:True'):
        print 'I am trying to recall the first step on the landing checklist....... '
        print 'Oh, yes, I have to begin to turn final now'
        Focusbuffer.set('unit_task:turn_final task_goal:start')
    def turn_final(Focusbuffer='unit_task:turn_final task_goal:start'):
        print 'turn final'
        Focusbuffer.set('unit_task:turn_final task_goal:rudder')        
    def turn_final2(Focusbuffer='unit_task:turn_final task_goal:rudder'):
        print 'left rudder'      
        Focusbuffer.set('unit_task:turn_final task_goal:Heading1')
    def turn_final3(Focusbuffer='unit_task:turn_final task_goal:Heading1'):  
        print 'recalling the runway'
        DM.request('recall ?')            
        Focusbuffer.set('unit_task:turn_final task_goal:heading2')
    def turn_final4(Focusbuffer='unit_task:turn_final task_goal:heading2'):  
        print 'I recall runway instructions.......Landing runway seven nine'        
        Focusbuffer.set('unit_task:turn_final task_goal:complete')
        
    '''def forgot1(Focusbuffer='unit_task:turn_final task_goal:heading2', DMbuffer=None, DM='error:True'): # DMbuffer=none means the buffer is empty # DM='error:True' means the search was unsucessful                                  
        print 'I am trying to recall runway instructions....... '
        print 'I forgot the runway instructions'
        Focusbuffer.set('unit_task:turn_final task_goal:ATC_request')
    def request_runway(Focusbuffer='unit_task:turn_final task_goal:ATC_request'):
        print 'ATC please confirm runway instructions'
        print 'ATC confirming runway seven nine'
        Focusbuffer.set('unit_task:turn_final task_goal:heading3')
    def turn_final5(Focusbuffer='unit_task:turn_final task_goal:heading3'):
        print 'Thanks, I am now on the correct runway heading'      
        Focusbuffer.set('unit_task:turn_final task_goal:complete')'''
        
## eval_cond  This commented out, as in this case a switch must be made to the new planning unit at this point...
        
    #def forgot2(Focusbuffer='unit_task:eval_cond task_goal:start', DMbuffer=None, DM='error:True'):            
        #print 'I am trying to recall next step on the landing checklist....... '
        #print 'Oh, yes, I have to evaluate the weather and runway conditions'
        #Focusbuffer.set('unit_task:eval_cond task_goal:start')       
    #def eval_cond1(Focusbuffer='unit_task:eval_cond task_goal:start'):
        #print 'wind conditions being evaluated'      
        #Focusbuffer.set('unit_task:eval_cond task_goal:runway_con')
    #def eval_cond2(Focusbuffer='unit_task:eval_cond task_goal:runway_con'):
        #print 'runway conditions evaluated'      
        #Focusbuffer.set('unit_task:eval_cond task_goal:runway_obstruct')
    #def eval_cond3(Focusbuffer='unit_task:eval_cond task_goal:runway_obstruct'):
        #print 'runway clear for landing'
        #Focusbuffer.set('unit_task:eval_cond task_goal:complete')

##eval_cond_incursion

    def eval_cond_incursion1(Focusbuffer='unit_task:eval_cond_incursion task_goal:start'):
        print 'wind conditions being evaluated'      
        Focusbuffer.set('unit_task:eval_cond_incursion task_goal:runway_con')
    def eval_cond_incursion2(Focusbuffer='unit_task:eval_cond_incursion task_goal:runway_con'):
        print 'runway conditions evaluated'      
        Focusbuffer.set('unit_task:eval_cond_incursion task_goal:runway_obstruct')
    def eval_cond_incursion3(Focusbuffer='unit_task:eval_cond_incursion task_goal:runway_obstruct'):
        print 'runway not clear for landing'
        Focusbuffer.set('unit_task:eval_cond_incursion task_goal:complete')
        

## dir_control
        
    def forgot3(Focusbuffer='unit_task:dir_control task_goal:start', DMbuffer=None, DM='error:True'):            
        print 'I am trying to recall next step on the landing checklist....... '
        print 'Oh, yes, I have to control my heading'
        Focusbuffer.set('unit_task:dir_control task_goal:start')       
    def dir_control1(Focusbuffer='unit_task:dir_control task_goal:start'):
        print 'control direction of plane'      
        Focusbuffer.set('unit_task:dir_control task_goal:check_compass')
    def dir_control2(Focusbuffer='unit_task:dir_control task_goal:check_compass'):
        print 'observe compass heading' 
        Focusbuffer.set('unit_task:dir_control task_goal:crosswind_check')
    def dir_control3(Focusbuffer='unit_task:dir_control task_goal:crosswind_check'):
        print 'heading adjusted for crosswind'      
        Focusbuffer.set('unit_task:dir_control task_goal:complete')
        
## glidescope
        
    def forgot4(Focusbuffer='unit_task:glidescope task_goal:start', DMbuffer=None, DM='error:True'):            
        print 'I am trying to recall next step on the landing checklist....... '
        print 'Oh, yes, I have to adjust my glidescope'
        Focusbuffer.set('unit_task:glidescope task_goal:start')    
    def glidescope1(Focusbuffer='unit_task:glidescope task_goal:start'):
        print 'adjust glidescope'      
        Focusbuffer.set('unit_task:glidescope task_goal:check_airspeed')
    def glidescope2(Focusbuffer='unit_task:glidescope task_goal:check_airspeed'):
        print 'airspeed reduced to 50 knots'      
        Focusbuffer.set('unit_task:glidescope task_goal:check_altimeter')
    def glidescope3(Focusbuffer='unit_task:glidescope task_goal:check_altimeter'):
        print 'altitude reduced'
        Focusbuffer.set('unit_task:glidescope task_goal:complete')
        

        
## touchdown
        
    def forgot5(Focusbuffer='unit_task:touchdown task_goal:start', DMbuffer=None, DM='error:True'):            
        print 'I am trying to recall next step on the landing checklist....... '
        print 'Oh, yes, I have to prepare for touchdown'
        Focusbuffer.set('unit_task:glidescope task_goal:check_airspeed')    
    def touchdown1(Focusbuffer='unit_task:touchdown task_goal:start'):
        print 'Altitude reduced for touchdown'      
        Focusbuffer.set('unit_task:touchdown task_goal:first_third')
    def touchdown2(Focusbuffer='unit_task:touchdown task_goal:first_third'):
        print 'landed in first third of runway'      
        Focusbuffer.set('unit_task:touchdown task_goal:brakes')
    def touchdown3(Focusbuffer='unit_task:touchdown task_goal:brakes'):
        print 'Brakes applied'      
        Focusbuffer.set('unit_task:touchdown task_goal:ATC_com')
    def touchdown4(Focusbuffer='unit_task:touchdown task_goal:ATC_com'):
        print 'ATC informed of landing and intention'
        Focusbuffer.set('unit_task:touchdown task_goal:complete')

## Touch and go abort landing

    def touch_go1(Focusbuffer='unit_task:touch_and_go task_goal:start'):
        print 'Insufficient braking distance for safe touchdown'      
        Focusbuffer.set('unit_task:touch_and_go task_goal:first_third')
    def touch_go2(Focusbuffer='unit_task:touch_and_go task_goal:first_third'):
        print 'ATC informed of touch and go decision'      
        Focusbuffer.set('unit_task:touch_and_go task_goal:brakes')
    def touch_go3(Focusbuffer='unit_task:touch_and_go task_goal:brakes'):
        print 'touch in middle third of runway'      
        Focusbuffer.set('unit_task:touch_and_go task_goal:ATC_com')
    def touch_go4(Focusbuffer='unit_task:touch_and_go task_goal:ATC_com'):
        print 'Aircraft re-entering airspace'
        Focusbuffer.set('unit_task:touch_and_go task_goal:complete')
        



pilot=MyAgent()                              # the agent
airfield=MyEnvironment()                       # the environment
airfield.agent=pilot                           # the agent in the environment
ccm.log_everything(airfield)                   # print out of what happens in the environment
log=ccm.log(html=True)

airfield.run()                               # runs the environment
ccm.finished()                             # stops the environment

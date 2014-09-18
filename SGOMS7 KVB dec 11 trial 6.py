
                                      #################### SGOMS: Cessna Left Circuit ###################

import ccm      
log=ccm.log()   

from ccm.lib.actr import *
log=ccm.log(html=True)

class cockpit(ccm.Model):        # items in the environment look and act like chunks
    cockpit_item1=ccm.Model(isa='altimeter',location='in_cockpit',salience=0.3)
    cockpit_item2=ccm.Model(isa='compass',location='in_cockpit',salience=0.3)
    cockpit_item3=ccm.Model(isa='airspeed_ind',location='in_cockpit',salience=0.3)
    cockpit_item4=ccm.Model(isa='ATC_instructions',location='in_cockpit',salience=0.1)#  I have not incorporated salience yet...

class pilot(ACTR):
    Focusbuffer=Buffer()
    Contextbuffer=Buffer()
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)

    DM=Memory(DMbuffer,latency=0.0,threshold=0.0)     # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=0.5,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=0.0,limit=None)       # turn on for DM subsymbolic processing
   
    
    def init():                                             
        DM.add ('planning_unit:landing    cue:start         step:turn_final')
        DM.add ('recall runway_seven_nine')
        DM.add ('planning_unit:landing    cue:turn_final    step:eval_cond')
        DM.add ('planning_unit:landing    cue:eval_cond     step:dir_control')
        DM.add ('planning_unit:landing    cue:dir_control   step:glidescope')
        DM.add ('planning_unit:landing    cue:glidescope    step:touchdown')
        DM.add ('planning_unit:landing    cue:touchdown     step:finished_planning_unitning_unit')
        DM.add ('planning_unit:landing    cue:finished      step:stop')
        
        DM.add ('constraint:multimodal_stimuli planning_unit:landing')
        DM.add ('constraint:ATC planning_unit:stop')
        
        Contextbuffer.set('constraint:multimodal_stimuli')
        Focusbuffer.set('state:constraints')

    def check_constraints(Focusbuffer='state:constraints',
                          Contextbuffer='constraint:?constraint'): # constraints are in the buffer
        print 'the constraint is', constraint
        DM.request('constraint:?constraint planning_unit:?') # request a planning unit from DM that fits the constraints
        Focusbuffer.set('state:planning_unit')


    '''def retrieve_planning_unitning_unit_forget(Focusbuffer='state:planning_unit', 
        if DMbuffer=None, # check buffer contents
        DM='error:True'): #check if DM search was successful
        print 'Having trouble starting this part of the landing'
        reset dm_n=DMNoise(DM,noise=0.0,baseNoise=0.0):
        Focusbuffer.set('state:unit_task')
            else DMbuffer='constraint:?constraint planning_unit:?planning_unit', DM='busy:False'):# retrieve the planning unit
        DM.request('planning_unit:?planning_unit cue:start step:?') # request the first unit task for the planning unit from DM
        Focusbuffer.set('state:unit_task')'''

    def retrieve_planning_unitning_unit(Focusbuffer='state:planning_unit', 
                               DMbuffer='constraint:?constraint planning_unit:?planning_unit', # retrieve the planning unit
                               DM='busy:False'):
        print 'start planning_unit = ', planning_unit
        DM.request('planning_unit:?planning_unit cue:start step:?') # request the first unit task for the planning unit from DM
        Focusbuffer.set('state:unit_task')

        
    def retrieve_unit_task(Focusbuffer='state:unit_task',
                           DMbuffer='cue:?cue!finished step:?step', # retrieve unit task
                           DM='busy:False'):
        print 'start planning_unit = ',step
        Focusbuffer.set('unit_task:?step task_goal:start action:go') # carry out the unit task

    def next_unit_task(Focusbuffer='unit_task:?step task_goal:complete'): # match on the unit task being "complete"
        print 'finished planning_unit = ',step
        Focusbuffer.set('state:unit_task')
        DM.request('cue:?step step:?') # request next unit task
     
    def finished_unit_task(Focusbuffer='unit_task:?step task_goal:end'): # match on end of unit tasks
        print 'end' 
        Contextbuffer.set('constraint:ATC') # change constraints
        Focusbuffer.set('state:constraints') # next planning unit

        
        
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
    def turn_final4(Focusbuffer='unit_task:turn_final task_goal:heading2', DMbuffer='recall ?runway'):  
        print 'I recall runway instructions.......'        
        print runway             
        print 'Landing runway seven nine'
        Focusbuffer.set('unit_task:turn_final task_goal:complete')
    def forgot1(Focusbuffer='unit_task:turn_final task_goal:heading2', DMbuffer=None, DM='error:True'): # DMbuffer=none means the buffer is empty # DM='error:True' means the search was unsucessful                                  
        print 'I am trying to recall runway instructions....... '
        print 'I forgot the runway instructions'
        Focusbuffer.set('unit_task:turn_final task_goal:ATC_request')
    def request_runway(Focusbuffer='unit_task:turn_final task_goal:ATC_request'):
        print 'ATC please confirm runway instructions'
        print 'ATC confirming runway seven nine'
        Focusbuffer.set('unit_task:turn_final task_goal:heading3')
    def turn_final5(Focusbuffer='unit_task:turn_final task_goal:heading3'):
        print 'Thanks, I am now on the correct runway heading'      
        Focusbuffer.set('unit_task:turn_final task_goal:complete')
        
## eval_cond
        
    def forgot2(Focusbuffer='unit_task:eval_cond task_goal:start', DMbuffer=None, DM='error:True'):            
        print 'I am trying to recall next step on the landing checklist....... '
        print 'Oh, yes, I have to evaluate the weather and runway conditions'
        Focusbuffer.set('unit_task:eval_cond task_goal:start')       
    def eval_cond1(Focusbuffer='unit_task:eval_cond task_goal:start'):
        print 'wind conditions being evaluated'      
        Focusbuffer.set('unit_task:eval_cond task_goal:runway_con')
    def eval_cond2(Focusbuffer='unit_task:eval_cond task_goal:runway_con'):
        print 'runway conditions evaluated'      
        Focusbuffer.set('unit_task:eval_cond task_goal:runway_obstruct')
    def eval_cond3(Focusbuffer='unit_task:eval_cond task_goal:runway_obstruct'):
        print 'runway clear for landing'
        Focusbuffer.set('unit_task:eval_cond task_goal:complete')

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
        Focusbuffer.set('unit_task:touchdown task_goal:end')


tim=pilot()                                # name the agent
env=cockpit()                         # name the environment
env.agent=tim                           # put the agent in the environment
ccm.log_everything(env)                 # print out what happens in the environment

env.run()                               # run the environment
ccm.finished()                             # stop the environment

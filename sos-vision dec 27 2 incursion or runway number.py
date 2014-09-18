##################RUNWAY INCURSION SCENARIO#################################
#in this scenario a runway incursion has occured (something on the runway that means a regular landing should be averted
#the pilot attributes salience or importance to two competing landing procedures 1) evaluating the runway for incursions
# and 2) remembering the runway they are to land on.
#if the pilot cannot remember the runway they must direct time attention to this activity, which reduces the time and attention
#that can be spent on evaluating the runway.
# by changing the salience below you can observe the pilot either correctly aborting the standard landing, or watch him/her
#face an imminent collision with the runway incursion.

## this models compares the effect of the salience (or attention paid by the pilot in this case) of two competing landing checklist features
## each feature receives an attention factor in accordance with the salience it is accorded
## the salience setting on the item searched for determines how fast it is found- which also can be seen as where the pilot chooses to direct his/her attention

import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class In_cockpit(ccm.Model):
  procedure1=ccm.Model(isa='pilot_procedure',location='landing_phase',feature1='notice_incursion',salience=0.5) # you can change the salience and see which productions fire
  procedure2=ccm.Model(isa='pilot_procedure',location='landing_phase',feature1='recall_runway',salience=0.5)

class MyAgent(ACTR): 
  focus_buffer=Buffer()
  code_buffer=Buffer()
  visual_buffer=Buffer()
  vision_module=SOSVision(visual_buffer,delay=0) # delay=0 means the results of the visual search are
                                                 # placed in the visual buffer right after the request
                                                 # but the request takes 50 msec and the retieval takes 50 msec
                                                 # so actually it takes 100 msec to get the results at minimum
  
 ################ procedural production system ######################
  
  def init():
    focus_buffer.set('procedure')

  def landing(focus_buffer='procedure'):
    vision_module.request('isa:pilot_procedure location:landing_phase')
    focus_buffer.set('follow_procedure')
    print 'I am now in the landing phase of my circuit'

  def procedure1(focus_buffer='follow_procedure',visual_buffer='isa:pilot_procedure location:landing_phase feature1:?feature1'):
    print'I am following procedure'
    focus_buffer.set('check ?feature1')
    visual_buffer.clear
    
  def check_yes(focus_buffer='check notice_incursion'):
    focus_buffer.set('switch_planning_unit')
    visual_buffer.clear
    print'I see a runway incursion- switch to short runway landing procedures'

  def switch(focus_buffer='switch_planning_unit'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print'I have switched to short runway landing procedures' # when this is more salient in the environment this production will fire more often- and the incursion will be averted
    
  def check_no(focus_buffer='check recall_runway'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print'I did not check for runway incursions- collision imminent!'   # when salience for notice incursion is reduced to .1 then this production fires approx 6 out of 10 times
    
  '''def not_seen(focus_buffer='procedure',visual_buffer=None):
    focus_buffer.set('check')
    visual_buffer.clear
    print'incursion imminent!'''

    
pilot=MyAgent()
env=In_cockpit()
env.agent=pilot 
ccm.log_everything(env)

env.run()
ccm.finished()
   














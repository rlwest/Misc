## this model looks for an item in a location based on a search feature
## then it checks the object for a second feature
## the salience setting on the item searched for determines how fast it is found

from ccm.lib.actr import *
from ccm.env.objects import *

class SockEnvironment(ObjectEnvironment):
  sock1=Object(isa='sock',location='in_drawer',feature1='red_stripe',salience=0.5)
  sock2=Object(isa='sock',location='in_drawer',feature1='blue_stripe',salience=0.5)

class brain_contents:
  focus_buffer=Buffer()
  code_buffer=Buffer()
  visual_buffer=Buffer()
  procedural_prodsys=Procedural(prefix='p',delay=.05)
  vision_module=SOSVision(visual_buffer,delay=0)
  
 ################ procedural production system ######################
   
  def p_find(focus_buffer='look'):
    vision_module.request('isa:sock location:in_drawer')
    focus_buffer.set('get_sock')
    print('I am looking for a sock')

  def p_found(focus_buffer='get_sock',visual_buffer='isa:sock location:in_drawer feature1:?feature1'):
    print('I found a sock')
    focus_buffer.set('check ?feature1')
    visual_buffer.clear
    
  def p_check_yes(focus_buffer='check red_stripe'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print('it has a red stripe')

  def p_check_no(focus_buffer='check blue_stripe'):
    focus_buffer.set('look')
    visual_buffer.clear
    print('it has a blue stripe')
    
  def p_not_found(focus_buffer='get_sock',visual_buffer=None):
    focus_buffer.set('look')
    visual_buffer.clear
    print('where is that sock?')

    
model=ACTR(brain_contents)          
model.focus_buffer.set('look')
env=SockEnvironment()
env.agent=model 

env.run()
   














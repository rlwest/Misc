## this model looks for an item in a location
## the salience setting on the item searched for determines how fast it is found

## seems same as a and b

from ccm.lib.actr import *
from ccm.env.objects import *

class SockEnvironment(ObjectEnvironment):
  sock1=Object(isa='sock',location='in_drawer',feature1='red_stripe',salience=0.1)
  sock2=Object(isa='sock',location='in_drawer',feature1='blue_stripe',salience=0.1)

class brain_contents:
  focus_buffer=Buffer()
  code_buffer=Buffer()
  visual_buffer=Buffer()
  procedural_prodsys=Procedural(prefix='p',delay=.05)
  vision_module=SOSVision(visual_buffer,delay=0)
  DMbuffer=Buffer()                                    
  DM=Memory(DMbuffer)

  def init():                                             
    DM.add ('search_criterion1:red_stripe')   


 ################ procedural production system ######################
   
  def p_find(focus_buffer='isa:?object location:?loc action:look'):
    vision_module.request('isa:?object location:?loc')
    focus_buffer.set('isa:?object location:?loc action:get')
    print 'I am looking for a sock'

  def p_found(focus_buffer='isa:?object location:?loc action:get',visual_buffer='isa:?object location:?loc feature1:?feature1'):
    print 'I found a sock'
    focus_buffer.set('isa:?object location:?loc feature1:?feature1 action:check')
    visual_buffer.clear
    
  def p_check_yes(focus_buffer='isa:?object location:?loc feature1:?feature1 action:check'):
    DM.request('search_criterion1:?feature1')   
    focus_buffer.set('stop')
    visual_buffer.clear
    print 'it has a red stripe'

  def p_check_no(focus_buffer='isa:?object location:?loc feature1:?feature1 action:check'):
    DM.request('search_criterion1:!?feature1')   
    focus_buffer.set('isa:?object location:?loc action:look')
    visual_buffer.clear
    print 'it has a blue stripe'
    
  def p_not_found(focus_buffer='isa:?object location:?loc action:get',visual_buffer=None):
    focus_buffer.set('isa:?object location:?loc action:look')
    visual_buffer.clear
    print 'where is that sock?'

    
model=ACTR(brain_contents)          
model.focus_buffer.set('isa:sock location:in_drawer action:look')
env=SockEnvironment()
env.agent=model 

env.run()
   














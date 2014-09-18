## this model looks for an item in a location
## the salience setting on the item searched for determines how fast it is found

from ccm.lib.actr import *
from ccm.env.objects import *

class SockEnvironment(ObjectEnvironment):
  sock1=Object(isa='sock',location='in_drawer',salience=0.1)

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
    print 'I am looking for a sock'

  def p_found(focus_buffer='get_sock',visual_buffer='isa:sock location:in_drawer'):
    print 'I found a sock'
    print 'I am putting on the sock'
    focus_buffer.set('stop')
    visual_buffer.clear

  def p_not_found(focus_buffer='get_sock',visual_buffer=None):
    focus_buffer.set('look')
    visual_buffer.clear
    print 'where is that sock?'

    
model=ACTR(brain_contents)          
model.focus_buffer.set('look')
env=SockEnvironment()
env.agent=model 

env.run()
   














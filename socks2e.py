## this is a model of top down search for an object in a location
## as in act-r pm it assumes you search for a particular thing and then further check its features to confirm it is the right object
## the salience setting on the item searched for determines how fast it is found (the number of distractors also affects this)

## same as d, d has comments on the productions

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
  DMbuffer=Buffer()                                    
  DM=Memory(DMbuffer)
  imaginalbuffer=Buffer()


 ################ procedural production system ######################
   
  def p_find(focus_buffer='chunktype:vsearch isa:?something location:?loc action:look'):
    vision_module.request('isa:?something location:?loc')
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:get')
    print 'I am looking for * * *'
    print something

  def p_found(focus_buffer='chunktype:vsearch isa:?something location:?loc action:get',visual_buffer='isa:?something location:?loc feature1:?feature1'):
    print 'I found - - - '
    print something
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc feature1:?feature1 action:check')
    visual_buffer.clear
    
  def p_check_yes(focus_buffer='chunktype:vsearch isa:?something location:?loc feature1:?feature1 action:check',imaginalbuffer='feature1:?feature1'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print 'it has ^ ^ ^'
    print feature1

  def p_check_no(focus_buffer='chunktype:vsearch isa:?something location:?loc feature1:?feature1 action:check',imaginalbuffer='feature1:!?feature1'):
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:look')
    visual_buffer.clear
    print 'it has a @ @ @'
    print feature1
    
  def p_not_found(focus_buffer='chunktype:vsearch isa:?something location:?loc action:get',visual_buffer=None):
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:look')
    visual_buffer.clear
    print 'where is that % % %'
    print something

    
model=ACTR(brain_contents)          
model.focus_buffer.set('chunktype:vsearch isa:sock location:in_drawer action:look')
model.imaginalbuffer.set('isa:sock feature1:red_stripe')
env=SockEnvironment()
env.agent=model 

env.run()
   














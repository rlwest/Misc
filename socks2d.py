## this model looks for an item in a location
## the salience setting on the item searched for determines how fast it is found

## this model is generalized to look for whatever is in the focus buffer
## so it can just be dumped into any model

from ccm.lib.actr import *
from ccm.env.objects import *

class SockEnvironment(ObjectEnvironment):
  sock1=Object(isa='sock',location='in_drawer',feature1='red_stripe',salience=0.1)
  sock2=Object(isa='sock',location='in_drawer',feature1='blue_stripe',salience=0.8)

class brain_contents:
  focus_buffer=Buffer()
  code_buffer=Buffer()
  visual_buffer=Buffer()
  procedural_prodsys=Procedural(prefix='p',delay=.05)
  vision_module=SOSVision(visual_buffer,delay=0)
  DMbuffer=Buffer()                                    
  DM=Memory(DMbuffer)
  imaginalbuffer=Buffer()

  def init():                                             
    DM.add ('search_criterion1:red_stripe')   


 ################ procedural production system ######################

    
    ## when the action is 'look' get the object and location from focus buffer
    ## reqest that from the visual buffer
  def p_find(focus_buffer='isa:?object location:?loc action:look'):
    vision_module.request('isa:?object location:?loc')
    focus_buffer.set('isa:?object location:?loc action:get')
    print 'I am looking for * * *'
    print object

    ## good trick - 1st, object and location are defined from the focus buffer,
    ## 2nd, they are used to see if the visual buffer matches
    ## also, if it matches then feature1 is defined by the visual buffer
    ## feature1 then gets added to the focus buffer
  def p_found(focus_buffer='isa:?object location:?loc action:get',visual_buffer='isa:?object location:?loc feature1:?feature1'):
    print 'I found - - - '
    print object
    focus_buffer.set('isa:?object location:?loc feature1:?feature1 action:check')
    visual_buffer.clear
    
    ## same trick - used to compare feature1 in focus to a feature in imaginal
    ## fires with a match
  def p_check_yes(focus_buffer='isa:?object location:?loc feature1:?feature1 action:check',imaginalbuffer='?feature1'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print 'it has ^ ^ ^'
    print feature1

    ## same trick - used to compare feature1 in focus to a feature in imaginal
    ## fires with a not match
  def p_check_no(focus_buffer='isa:?object location:?loc feature1:?feature1 action:check',imaginalbuffer='!?feature1'): 
    focus_buffer.set('isa:?object location:?loc action:look')
    visual_buffer.clear
    print 'it has a @ @ @'
    print feature1
    
  def p_not_found(focus_buffer='isa:?object location:?loc action:get',visual_buffer=None):
    focus_buffer.set('isa:?object location:?loc action:look')
    visual_buffer.clear
    print 'where is that % % %'
    print object

    
model=ACTR(brain_contents)          
model.focus_buffer.set('isa:sock location:in_drawer action:look')
model.imaginalbuffer.set('red_stripe')
env=SockEnvironment()
env.agent=model 

env.run()
   














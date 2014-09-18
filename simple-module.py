
##  spider socks search

## topdown

## this is a model of top down search for an object in a location
## as in act-r pm it assumes you search for a particular set of features (a sock shape)
## then further check its features to confirm it is the right object (a sock with a red strip)
## the salience setting on the item searched for determines how fast it is found
## the number of distractors also affects this (a sock with a blue stip)
## in this case the effect of other distractors (underware)
## is represented by lowering the salience of the search objects (socks)
## the location and the search features are put in the visual_search_buffer
## all the features of the object are stored in the imaginal_buffer


## bottom up

## this model also has a bottom up visual attention module
## this is a simple production system
## that operates in parallel with the procedural memory production system
## when the vision module is not busy with top down intstuctions from the procedural system
## the attention module randomly searches the environment
## this allows the model to find a small spider that is running around in the drawer
## to create more random opertunities for random search there is a distracted production
## this represents less than perfect concentration by the procedural system


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  


class Sock_drawer(ccm.Model):
  sock1=ccm.Model(isa='sock',location='in_drawer',feature1='red_stripe',salience=0.5)
  sock2=ccm.Model(isa='sock',location='in_drawer',feature1='blue_stripe',salience=0.5)
  spider=ccm.Model(isa='spider',location='in_drawer',salience=0.9)


############### bottom up visual production system #######################
class MyVisualSearchModule(ccm.ProductionSystem):
    production_time=0.05
    
    #def v_initiate_search(vision_module='busy:False'):
        #vision_module.request('')
        #print "bottom up looking"
        # look around if the visual search system is not busy
    def caution(focus='risk:high'):
        print "Oh no!!!"
  
class MyAgent(ACTR): 
  focus=Buffer()
  visual_search_buffer=Buffer()
  vision_module=SOSVision(visual_search_buffer,delay=0)
  DMbuffer=Buffer()                                    
  DM=Memory(DMbuffer)
  imaginalbuffer=Buffer()

  visual_search_prodsys=MyVisualSearchModule()


    def init():
        focus.set('sandwich bread')

    def bread_bottom(focus='sandwich bread'):     # if focus buffer has this chunk then....
        print "I have a piece of bread"           # print
        focus.set('sandwich cheese')              # change chunk in focus buffer

    def cheese(focus='sandwich cheese'):          # the rest of the productions are the same
        print "I have put cheese on the bread"    # but carry out different actions
        focus.set('sandwich ham')

    def ham(focus='sandwich ham'):
        print "I have put  ham on the cheese"
        focus.set('sandwich bread_top')

    def bread_top(focus='sandwich bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('stop')   

    def stop_production(focus='stop'):
        self.stop()                        # stop the agent

############### top down procedural search productions ######################
   
  def find(focus_buffer='chunktype:vsearch isa:?something location:?loc action:look'):
    vision_module.request('isa:?something location:?loc')
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:get')
    print 'I am looking for'
    print something

  def found(focus_buffer='chunktype:vsearch isa:?something location:?loc action:get',
              visual_search_buffer='isa:?something location:?loc feature1:?feature1'):
    print 'I found'
    print something
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc feature1:?feature1 action:check')
    visual_search_buffer.clear
    
  def check_yes(focus_buffer='chunktype:vsearch isa:?something location:?loc feature1:?feature1 action:check',
                  imaginalbuffer='feature1:?feature1'):
    focus_buffer.set('stop') # stop the top down search
    visual_search_buffer.clear
    print 'it has'
    print feature1
    print 'found it'

  def check_no(focus_buffer='chunktype:vsearch isa:?something location:?loc feature1:?feature1 action:check',
                 imaginalbuffer='feature1:!?feature1'):
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:look')
    visual_search_buffer.clear
    print 'it has'
    print feature1
    
  def not_found(focus_buffer='chunktype:vsearch isa:?something location:?loc action:get',
                  visual_search_buffer=None):
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:look')
    visual_search_buffer.clear
    print 'did not find'
    print something

############### bottom up procedural search productions ######################

  def different_found(focus_buffer='chunktype:vsearch isa:?something location:?loc action:get',
                        visual_search_buffer='isa:?differenthing'):
    focus_buffer.set('chunktype:vsearch isa:?something location:?loc action:look')
    visual_search_buffer.clear
    print 'I found'
    print differenthing
    # continues the top down search

############### distraction procedural productions ######################

  def not_looking(focus_buffer='chunktype:vsearch isa:?something location:?loc action:look'):
    print 'not focused'


tim=MyAgent()
env=Sock_drawer()
env.agent=tim 
ccm.log_everything(env)

env.run(1)
ccm.finished()














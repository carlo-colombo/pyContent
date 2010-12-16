import unittest
import logging

import pdb

from model.Content import Content,PathNotFoundException

#import unittest.TestCase as t

class ContentModelTest(unittest.TestCase):
    def content_creation_test(self):
        c=Content(name="dsas")
        c.put()
        
    def content_difficult_name_test(self):
        c=Content(name="D d")
        self.assertEquals(c.name,"d-d")
        
    def content_difficult_name_2_test(self):
        c=Content(name="test")
        c.name="D d"
        self.assertEquals(c.name,"d-d")
        
    def dinamic_property_test(self):
        c=Content(name="test",title="Content title")
        c.put()
        self.assertEquals(c.title,"Content title")
        
    def content_parent_test(self):
        p=Content(name="parent")
        p.put()
        c=Content(name="children",parent=p)
        self.assertEquals(c.parent().name,"parent")
        
    def content_children_test(self):
        p=Content(name="parent")
        p.put()
        c1=Content(name="children1",parent=p)
        c2=Content(name="children2",parent=p)
        c1.put()
        c2.put()
        children=[c.key() for c in p.children]
        self.assertEquals(len(children),2)
        self.assertTrue(c1.key() in children and c2.key() in children)
        c1.delete()
        c2.delete()
        p.delete()
        
        
    def handle_test(self):
        p=Content(name="parent")
        p.put()
        c=Content(name="children",parent=p)
        self.assertEquals(c.handle,"/parent/children")

    def _set_up_ancestor_stuff(self):
        gp=Content(name="grandpa_ancestor")
        gp.put()
        p=Content(name="parent_ancestor",parent=gp)
        p.put()
        c=Content(name="child_ancestor",parent=p)
        c.put()
        return gp,p,c

    def ancestor_test(self):
        gp,p,c = self._set_up_ancestor_stuff()
        self.assertEquals(c.ancestor(1).key() ,gp.key())
        
    def ancestor_gt_level_test(self):
        gp,p,c = self._set_up_ancestor_stuff()
        self.assertRaises(PathNotFoundException,c.ancestor,100)
        
    def ancestor_lt_zero_level_test(self):
        gp,p,c = self._set_up_ancestor_stuff()
        self.assertRaises(PathNotFoundException,gp.ancestor,-1)
    
    def ancestor_zero_level_test(self):
        gp,p,c = self._set_up_ancestor_stuff()
        self.assertRaises(PathNotFoundException,c.ancestor,0)
        
    def level_root_content_test(self):
        c=Content(name="content")
        c.put()
        self.assertEquals(c.level,1)
        
    def level_test(self):
        p=Content(name="parent")
        p.put()
        c=Content(name="child",parent=p)
        c.put()
        self.assertEquals(c.level,2)
        
    def duplicate_name_first_duplicate_test(self):
        Content(name="content").put()
        c=Content(name="content").put()
        self.assertEquals(c.name,"content0")
        
    def duplicate_name_nth_duplicate_test(self):
        Content(name="content3").put()
        c=Content(name="content3").put()
        self.assertEquals(c.name,"content4")
        
    def duplicate_name_nth_duplicate_more_digit_test(self):
        Content(name="content13").put()
        c=Content(name="content13").put()
        self.assertEquals(c.name,"content14")
        
    def duplicate_name_after_creation_test(self):
        Content(name="content").put()
        oc=Content(name="other-content")
        oc.put()
        self.assertEquals(oc.name,"other-content")
        oc.name="content"
        oc.put
        self.assertEquals(oc.name,"content0")

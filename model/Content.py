import logging
import re
from google.appengine.ext import db
from Repository import Repository

class Content(db.Expando):
    name__ = db.StringProperty(required=True,name="name")
    creationDate=db.DateTimeProperty(required=True)

    def __init__(self, parent=None, key_name=None, _app=None, repository=None, **kwds):
        #rimuovere dipendenza da ContentUtils
        kwds['name']=ContentUtils.sanitize(kwds["name"])
        kwds['creationDate']=db.DateTimeProperty.now()
        if repository:
            if isinstance(repository, Repository):
                parent=repository
            else:
                raise NotValidRepositoryException("repository class is %s, it should be %s"%(type(repository),Repository.__class__))
        db.Expando.__init__(self,parent=parent, key_name=key_name, _app=_app, **kwds)
        
    def __getitem__(self,key):
        #q=Content.Query()
        r=Content.all().ancestor(self.key()).filter('__key__ !=',self.key()).filter('name = ',key).fetch(1)
        if not r:
            raise KeyError
        return r[0]
        
    def setName(self,name):
        self.name__=ContentUtils.sanitize(name)
        
    def getName(self):
        return self.name__
        
    def getHandle(self):
        if self.parent():
            return self.parent().getHandle()+"/"+self.getName()
        else:
            return "/"+self.getName()
            
    def getChildren(self):
        q=db.Query()
        return q.ancestor(self.key()).filter('__key__ !=',self.key())
        
    def ancestor(self,level):
        if self.level==level:
            return self
        elif level > self.level:
            raise PathNotFoundException()
        elif level <= 0:
            raise PathNotFoundException()
        else:
            return self.parent().ancestor(level)
        #check magnolia/jcr code
        '''if level==1: 
            return self
        elif self.parent():
            return self.parent().ancestor(level-1)
        '''
        #raise MethodNotYetImplemented()

    def getLevel(self):
        if not self.parent() or isinstance(self.parent(),Repository):
            return 1
        else:
            return self.parent().getLevel() + 1
        
    name=property(fget=getName,fset=setName)
    handle=property(fget=getHandle)
    children=property(fget=getChildren)
    level=property(fget=getLevel)
    
    '''
    def sanitize(self,name):
        sanitized_name=ContentUtils.sanitize(name)
        if (self.parent() and sanitized_name in [c.name for c in self.parent().children]):
            m=re.match(r'([-a-z]*)(\d*)$',sanitized_name)
            if m.group(2):
                index=int(m.group(2))+1
            else:
                index=0
            return self.sanitize("%s%s" % (m.group(1),index))
        return sanitized_name
       '''
    
class ContentUtils(object):
    @staticmethod
    def sanitize(text):
        return text.lower().replace(" ","-")
    
class DuplicateContentNameException(Exception):
    """Duplicate named content at the same level"""

class MethodNotYetImplementedException(Exception):
    """This method is not yet implemented"""
    
class PathNotFoundException(Exception):
    """Path not found"""
    
class NotValidRepositoryException(Exception):
    """Not valid istance of Repository (or subclass)"""

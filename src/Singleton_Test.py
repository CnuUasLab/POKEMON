class Singleton(type):
    def __init__(cls,name,bases,dic):
        super(Singleton,cls).__init__(name,bases,dic)
        cls.instance=None
    def __call__(cls,*args,**kw):
        if cls.instance is None:
            print "creating NEW instance"
            cls.instance=super(Singleton,cls).__call__(*args,**kw)
        else:
            print "using EXISTING instance"
        return cls.instance

class Object(object):
    __metaclass__ = Singleton
    def __init__(self, arg=None):
        print "creating instance with arg: ", arg

c = Object("parameter")
x = Object("something")
d = Object("another One")
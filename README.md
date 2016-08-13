<h1>Introspect</h1>
<p> This is script that is is useful to draw the inheritance diagram of a module. This helps in understanding the codebase at the start.
It uses python introspective features to draw the class diagram. Rememeber that this is not a perfect class diagram it does not 
show any compositional features</p>

Import the script and just call the function introspect with first argument with module object for which you want to see class
diagram,second argument where the diagram is stored
```python
import introspect
introspect(module,filename)
```
``` python
class A(object):
    def __init__(self,boo):
    def a(self):
        pass
    def b(self):
        pass
class B(object):
    def __init__(self,boo):
        pass
    def c(self):
        pass
    def d(self):
        pass
class c(object):
    def __init__(self,boo):
        pass
    def e(self):
        pass
    def f(self):
        pass
class D(A,B):
    def __init__(self,boo):
        pass
    def g(self):
        pass
    def b(self):
        pass
```
<p>
The class diagram generated for the above code is </p>
![Alt text](/img/testfile.png?raw=true "inheritance diagram")






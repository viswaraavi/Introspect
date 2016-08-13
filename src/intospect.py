import inspect
from graphviz import Digraph



class node:
    # definition of node class that are used to build graph
    def __init__(self,parent,child,name,attributes=set(),functions=set()):
        self.name=name
        self.parent=parent
        self.child=child
        self.attributes=attributes
        self.functions=functions

def parser(module):
    module_mem=inspect.getmembers(module,inspect.isclass)
    for class_name,class_ref in module_mem:
        construct_graph(class_name, class_ref)


#dictionary that helps to map class names to node
node_hash={}
#Basic graph object that holds the tree
graph={}

def construct_graph(class_name, ref_class):
    #The main function that is used to construct the inheritance tree
    class_bases=ref_class.__bases__
    if(not class_bases):
        return 
    for ref_class_parent in class_bases:
        
        if ref_class not in graph:
            graph[ref_class]=node(name=ref_class, parent=[], child=[])
        if ref_class_parent not in graph:
            graph[ref_class_parent]=node(name=ref_class_parent,parent=[],child=[])

        if ref_class_parent.__name__ in node_hash:
            node_hash[ref_class.__name__] = graph[ref_class]
            graph[ref_class].parent.append(graph[ref_class_parent])
            graph[ref_class_parent].child.append(graph[ref_class])
            
        else:
            node_hash[ref_class_parent.__name__]=graph[ref_class_parent]
            node_hash[ref_class.__name__]=graph[ref_class]
            graph[ref_class].parent.append(graph[ref_class_parent])
            graph[ref_class_parent].child.append(graph[ref_class])
            construct_graph(ref_class_parent.__name__, ref_class_parent)



def get_attributes(class_ref):
    #The function that returns the attribute of the class
    attributes=inspect.getmembers(class_ref, lambda a:not(inspect.isroutine(a)))
    return set([a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])

def get_functions(class_ref):
    #The function that helps return the functions of the class
    attributes=inspect.getmembers(class_ref, lambda a:inspect.isroutine(a))
    return set([a[0] for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))])

dot = Digraph(comment='The Inheritance graph')    

def bfs_for_attr(graph, start):
    #runs the bfs algorithm constructed on the graph computng the attributes and functions that are needed
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            attr_childs=[set(dir(child.name)) for child in graph[vertex].child]
            for attr,node in zip(attr_childs,graph[vertex].child):
                node.attributes=get_attributes(node.name)-get_attributes(vertex)
                node.functions=get_functions(node.name)-get_functions(vertex)   
            queue.extend(set([temp.name for temp in graph[vertex].child]) - visited)
           


def generate_label(attributes,functions):
    label_string="attributes:\n"
    for attr in attributes:
        label_string=label_string+attr+"\n"
    label_string=label_string+"functions:\n"   
    for func in functions:
        label_string=label_string+func+"\n"

    return label_string


def graph_construct(dot,graph):
    for node in graph:
        node=node_hash[node.__name__]
        label=generate_label(node.attributes,node.functions)
        dot.node(node.name.__name__ ,label)
        for child_node in node.child:
            dot.edge(node.name.__name__,child_node.name.__name__)



def introspect(module_ref, filename):
    parser(module_ref)
    bfs_for_attr(graph, type(module_ref).__bases__[0])
    graph_construct(dot,graph)
    dot.render(filename=filename,view=True)



    
            
    
                
        
        
    
    
        

class HTMLNode: 
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ''

        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)


    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node is none")
        if self.tag is None:
            return self.value
        
        props_str = ""
        if self.props:
                for prop, value in self.props.items():
                    props_str += f' {prop}="{value}"'    
    
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is none")
        if self.children is None:
            raise ValueError("missing children")
            
        props_str = ""
        if self.props:
            for prop, value in self.props.items():
                props_str += f' {prop}="{value}"' 
            
        node_str = ""
        for child in self.children: 
            node_str += child.to_html()
        
        return f"<{self.tag}{props_str}>{node_str}</{self.tag}>"

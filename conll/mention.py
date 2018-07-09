import hashlib


class Mention:
    def __init__(self, doc_name, sent_num, start, end, words):
        self.doc_name = doc_name
        self.sent_num = sent_num
        self.start = start
        self.end = end
        self.words = words
        self.gold_parse_is_set = False
        self.gold_parse = None
        self.sys_parse = None
        self.min_spans = None
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.min_spans:
                return self.doc_name == other.doc_name and self.sent_num == other.sent_num \
                       and self.min_spans==other.min_spans
            else:
                return self.doc_name == other.doc_name and self.sent_num == other.sent_num \
                   and self.start == other.start and self.end == other.end 
        return NotImplemented
    
    def __neq__(self, other):
        if isinstance(other, self.__class__):
            return self.__eq__(other)
        
        return NotImplemented
    
    def __str__(self):
        return str("DOC: " +self.doc_name+ ", sentence number: " + str(self.sent_num) 
                   + ", ("+str(self.start)+", " + str(self.end)+")" +
                   (str(self.gold_parse) if self.gold_parse else "") + ' ' + ' '.join(self.words))

    def __hash__(self):
        if self.min_spans:
            return self.sent_num * 1000000 + hash(frozenset(self.min_spans))
        else:
            return self.sent_num * 1000000 + hash(frozenset((self.start, self.end)))

    def get_span(self):
        if self.min_spans:
            ordered_words=[e[0] for e in sorted(self.min_spans, key=lambda e: e[1])]
            return ' '.join(ordered_words)
        else:
            return ' '.join(self.words)
         
            
    def set_gold_parse(self, tree):
        self.gold_parse = tree
        self.gold_parse_is_set = True

    def are_nested(self, other):
        if isinstance(other, self.__class__):
            if self.__eq__(other):
                return -1

            if self.min_spans:
                #self is nested in other
                if self.doc_name == other.doc_name and self.sent_num == other.sent_num \
                       and self.min_spans <= other.min_spans:
                    return 0
                #other is nested in self
                elif self.doc_name == other.doc_name and self.sent_num == other.sent_num \
                       and self.min_spans >= other.min_spans:
                    return 1
                #they are not nested
                return -1
            else:
                #self is nested in other
                if self.sent_num == other.sent_num and \
                   self.start >= other.start and self.end <= other.end:
                    return 0
                #other is nested in self
                elif self.sent_num == other.sent_num and \
                   other.start >= self.start and other.end <= self.end:
                    return 1
                else:
                    return -1
       
        return NotImplemented

class TreeNode:
    def __init__(self, tag, index, isTerminal):
        self.tag = tag
        self.index = index
        self.isTerminal = isTerminal
        self.children = []
        
    def __str__(self, level=0):
        ret = "\t"*level+self.tag+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def get_terminals(self, terminals):
        if self.isTerminal:
            terminals.append(self.tag)
        else:
            for child in self.children:
                child.get_terminals(terminals)

    def refined_get_children(self):    
        children = []
        for child in self.children:
            if not child.isTerminal and child.children and len(child.children)==1 and child.children[0].isTerminal:
                children.append(child.children[0])
            else:
                children.append(child)
        return children

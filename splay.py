from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Search
    def search(self,key:int):
        splay(self, key)

    # Insert Method 1
    def insert(self,key:int):
        splay(self, key)
        root = self.root
        node = Node(key=key, leftchild=None, rightchild=None, parent=None)
        if root == None:
            self.root = node
            return
        if root.key < key:
            # root is IOP
            self.root = node
            node.leftchild = root
            root.parent = node
            root_right_child: Node = root.rightchild
            node.rightchild = root_right_child
            if root_right_child:
                root_right_child.parent = node
            root.rightchild = None
        else:
            # root is IOS
            self.root = node
            node.rightchild = root
            root.parent = node
            root_left_child: Node = root.leftchild
            node.leftchild = root_left_child
            if root_left_child:
                root_left_child.parent = node
            root.leftchild = None

    # Delete Method 1
    def delete(self,key:int):
        splay(self, key)
        root = self.root
        if root.leftchild == None and root.rightchild == None:
            self.root = None
        elif root.leftchild == None:
            # Only has right subtree
            self.root = root.rightchild
            root.rightchild.parent = None
        elif root.rightchild == None:
            # Only has left subtree
            self.root = root.leftchild
            root.leftchild.parent = None
        else:
            # Neither subtree is empty
            right_subtree: SplayTree = SplayTree(root=root.rightchild)
            splay(right_subtree, key)
            new_root: Node = right_subtree.root
            left_subtree: Node = root.leftchild
            new_root.leftchild = left_subtree
            if left_subtree:
                left_subtree.parent = new_root
            new_root.parent = None
            self.root = new_root

# Perform splay on x
def splay(splay_tree:SplayTree, x:int):
    if splay_tree.root == None or splay_tree.root.key == x:
        return
    cur = splay_tree.root
    while cur:
        if cur.key == x:
            break
        elif x < cur.key:
            if cur.leftchild:
                cur = cur.leftchild
            else:
                break
        else:
            if cur.rightchild:
                cur = cur.rightchild
            else:
                break
    parent: Node = cur.parent
    grandparent: Node = None
    if parent:
        grandparent: Node = parent.parent
    while splay_tree.root != cur:
        if grandparent == None:
            # parent is the root
            if parent.leftchild == cur:
                cur = zig_right(splay_tree, cur)
            else:
                cur = zig_left(splay_tree, cur)
        else:
            if grandparent.leftchild == parent:
                if parent.leftchild == cur:
                    cur = zigzig_right(splay_tree, cur)
                else:
                    cur = zigzag_left(splay_tree, cur)
            else:
                if parent.rightchild == cur:
                    cur = zigzig_left(splay_tree, cur)
                else:
                    cur = zigzag_right(splay_tree, cur)
        parent = cur.parent
        if parent:
            grandparent = parent.parent
        else:
            grandparent = None

# Perform right zig on node
def zig_right(splay_tree:SplayTree, node:Node) -> Node:
    return right_rotate(splay_tree, node.parent)

# Perform left zig on node
def zig_left(splay_tree:SplayTree, node:Node) -> Node:
    return left_rotate(splay_tree, node.parent)

# Perform right zig-zig on node
def zigzig_right(splay_tree:SplayTree, node:Node) -> Node:
    parent: Node = node.parent
    new_parent = right_rotate(splay_tree, parent.parent)
    return right_rotate(splay_tree, new_parent)

# Perform left zig-zig on node
def zigzig_left(splay_tree:SplayTree, node:Node) -> Node:
    parent: Node = node.parent
    new_parent = left_rotate(splay_tree, parent.parent)
    return left_rotate(splay_tree, new_parent)

# Perform left zig-zag on node
def zigzag_left(splay_tree:SplayTree, node:Node) -> Node:
    node = left_rotate(splay_tree, node.parent)
    return right_rotate(splay_tree, node.parent)

# Perform right zig-zag on node
def zigzag_right(splay_tree:SplayTree, node:Node) -> Node:
    node = right_rotate(splay_tree, node.parent)
    return left_rotate(splay_tree, node.parent)

# Performs a left rotation on node
def left_rotate(splay_tree:SplayTree, node:Node) -> Node:
    node_parent: Node = node.parent
    right_child: Node = node.rightchild
    right_left_subtree: Node = right_child.leftchild
    right_child.leftchild = node
    right_child.parent = node.parent
    node.parent = right_child
    node.rightchild = right_left_subtree
    if right_left_subtree:
        right_left_subtree.parent = node
    if splay_tree.root == node:
        splay_tree.root = right_child
    if node_parent:
        if node_parent.leftchild and node_parent.leftchild.parent != node_parent:
            node_parent.leftchild = right_child
        else:
            node_parent.rightchild = right_child
    return right_child

# Performs a right rotation on node
def right_rotate(splay_tree:SplayTree, node:Node) -> Node:
    node_parent: Node = node.parent
    left_child: Node = node.leftchild
    left_right_subtree: Node = left_child.rightchild
    left_child.rightchild = node
    left_child.parent = node.parent
    node.parent = left_child
    node.leftchild = left_right_subtree
    if left_right_subtree:
        left_right_subtree.parent = node
    if splay_tree.root == node:
        splay_tree.root = left_child
    if node_parent:
        if node_parent.leftchild and node_parent.leftchild.parent != node_parent:
            node_parent.leftchild = left_child
        else:
            node_parent.rightchild = left_child
    return left_child
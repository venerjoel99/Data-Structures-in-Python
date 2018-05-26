import math

#Abstract Node class(no next pointer)
class Node:
	def __init__(self, val):
		self.__val = val

	def setValue(self, new_val):
		self.__val = new_val

	def getValue(self):
		return self.__val

	def __str__(self):
		return str(self.__val)

	def __gt__(self, other):
		return self.__val > other.getValue()

	def __ge__(self, other):
		return self.__val >= other.getValue()

	def __eq__(self, other):
		if other==None:
			return self is None
		return self.__val==other.getValue()

	def __lt__(self, other):
		return self.__val < other.getValue()

	def __le__(self, other):
		return self.__val <= other.getValue()

	def __ne__(self, other):
		if other==None:
			return self is not None
		return self.__val != other.getValue()

	__repr__ = __str__

#Binary Tree Node
class TreeNode(Node):
	def __init__(self, val):
		Node.__init__(self, val)
		self.__left = None
		self.__right = None

        def setLeft(self, new_node):
                self.__left = new_node

        def getLeft(self):
                return self.__left

        def setRight(self, new_node):
                self.__right = new_node

        def getRight(self):
                return self.__right

#Linked List Node
class LLNode(Node):
	def __init__(self, val):
		Node.__init__(self, val)
		self.__next = None

	def getNext(self):
                return self.__next

        def setNext(self, new_node):
                self.__next = new_node

#Doubly Linked List Node
class DLLNode(LLNode):
	def __init__(self, val):
		LLNode.__init__(self, val)
		self.__prev = None

	def getPrevious(self):
		return self.__prev

	def setPrevious(self, new_node):
		self.__prev = new_node

#Circular Linked List
class CLL:
	def __init__(self):
		self.__size = 0
		self.__head = None
		self.__tail = None
		self.__current = None
		self.__prev = None

	def isEmpty(self):
		return self.__size==0 and self.__head is None \
		and self.__tail is None

	def size(self):
		return self.__size

	def add(self, val):
		new_node = LLNode(val)
		if self.isEmpty():
			self.__head = new_node
			self.__tail = new_node
			self.__current = new_node
			new_node.setNext(new_node)
		else:
			self.__tail.setNext(new_node)
			new_node.setNext(self.__head)
			self.__tail = new_node
		self.__size += 1

	def getCurrent(self):
		if not self.isEmpty():
			return self.__current.getValue()

	def movePointer(self):
		if not self.isEmpty():
			self.__prev = self.__current
			self.__current = self.__current.getNext()

	def removeCurrent(self):
		if self.__size == 1:
			self.__head = None
			self.__tail = None
			self.__current = None
			self.__prev = None
		else:
			if self.__prev is None:
				self.__tail.setNext(self.__current.getNext())
			else:
				self.__prev.setNext(self.__current.getNext())
			if self.__current is self.__head:
				self.__head = self.__head.getNext()
			elif self.__current is self.__tail:
				self.__tail = self.__prev
			temp = self.__current
			self.__current = self.__current.getNext()
			temp.setNext(None)
		self.__size -= 1

	def __str__(self):
		if self.isEmpty():
			return "Empty List"
		temp = self.__head
		elements = []
		while len(elements) < self.__size:
			elements.append(str(temp.getValue()))
			temp = temp.getNext()
		return ','.join(elements)

	__repr__ = __str__

#Queue Data Structure
class Queue:
	def __init__(self):
		self.__count = 0
		self.__head = None
		self.__tail = None

	def isEmpty(self):
		return self.__count==0 and self.__head==None

	def size(self):
		return self.__count

	def enqueue(self, item):
		new_node = LLNode(item)
		if self.isEmpty():
			self.__head = new_node
			self.__tail = new_node
		else:
			self.__tail.setNext(new_node)
			self.__tail = new_node
		self.__count += 1

	def dequeue(self):
		if self.isEmpty():
			return 'Queue is empty'
		value = self.__head.getValue()
		self.__head = self.__head.getNext()
		if self.__count==1:
			self.__tail = None
			self.__head = None
		self.__count -= 1
		return value

	def __str__(self):
		temp = self.__head
		result = []
		while temp is not None:
			result.append(str(temp))
			temp = temp.getNext()
		return ','.join(result)

	__repr__ = __str__

#Ordered Binary Tree
class OBT:
	def __init__(self):
		self.__root = None
		self.__midpoints = {}

	def isEmpty(self):
		return self.__root == None

	def clear(self):
		self.__root = None

	def add(self, value, current = None, reArrange = False):
		if self.isEmpty():
			self.__root = TreeNode(value)
		elif current==None:
			self.add(value, current=self.__root, reArrange = reArrange)
		elif value <= current.getValue():
			if current.getLeft()==None:
				current.setLeft(TreeNode(value))
			else:
				self.add(value, current=current.getLeft(), reArrange = reArrange)
		else:
			if current.getRight()==None:
				current.setRight(TreeNode(value))
			else:
				self.add(value, current=current.getRight(), reArrange = reArrange)
		if reArrange:
			self.reArrange()

	def __search(self, value):
		prev = None
		direction = None
		current = self.__root
		while current:
			if value == current.getValue():
				return prev, current, direction
			elif value < current.getValue():
				prev = current
				current = current.getLeft()
				direction = TreeNode.setLeft
			elif value > current.getValue():
				prev = current
				current = current.getRight()
				direction = TreeNode.setRight
		return (prev, current, direction)

	def remove(self, value, mergeLeft = True, reArrange=True):
		prev_node, node, direction  = self.__search(value)
		if node is None:
			return
		right = node.getRight()
		left = node.getLeft()
		current, other = (right, left) if mergeLeft else (left, right)
		child, set = (TreeNode.getLeft, TreeNode.setLeft) if mergeLeft else (TreeNode.getRight, TreeNode.setRight)
		if current != None:
			leaf = current
			while child(leaf):
				leaf = child(leaf)
			set(leaf, other)
		else:
			current = other
		if prev_node == None:
			self.__root = current
		else:
			direction(prev_node, current)
		if reArrange:
			self.reArrange()
		return node.getValue()

	def find(self, value):
		return self.__search(value)[1].getValue()

	def exists(self, value):
		return bool(self.__search(value)[1])


	def dfs(self, mode='in', result = [], current = None):
		if self.isEmpty():
			return result
		if current is None:
			return self.dfs(mode=mode, current = self.__root)
		else:
			left_node, right_node = current.getLeft(), current.getRight()
			left = [] if not left_node else self.dfs(mode = mode, current=left_node)
			right = [] if not right_node else self.dfs(mode = mode, current=right_node) 
			if mode=='in':
				return left + [current] + right
			elif mode=='pre':
				return [current] + left + right
			elif mode=='post':
				return left + right + [current]

	def bfs(self):
		if self.isEmpty():
			return 'Empty tree'
		level, leaves  = 1, 2
		q = Queue()
		q.enqueue(self.__root)
		nodes = []
		lev_str = [str(self.__root.getValue())]
		while not q.isEmpty():
			current = q.dequeue()
			left, right = (current.getLeft(), current.getRight()) if current else (None, None) 
			q.enqueue(left)
			q.enqueue(right)
			left_str, right_str = str(left), str(right)
			nodes.append(left)
			nodes.append(right)
			leaves -= 2
			if nodes == [None] * 2**level:
				break
			elif leaves == 0:
				lev_str.append(','.join([str(node) for node in nodes]))
				nodes = []
				level += 1
				leaves = 2**level
		max_len = len(lev_str[-1])
		result = ''
		for i in range(len(lev_str)):
			result += 'Level ' + str(i) + ': ' + lev_str[i].center(max_len) + '\n'
		return result

	def __midpointCalc(self, length):
		if length == 0:
			return 0
		elif length in self.__midpoints:
			return self.__midpoints[length]
        	exact_log = math.log(length, 2)
        	trunc_log = int(exact_log)
        	low_bound = 2**trunc_log
        	upper_bound = 2**(trunc_log + 1)
        	if length - low_bound < upper_bound - length:
                	mid_index = int(2**(trunc_log-1)) + length - int(2**trunc_log)
        	else:
                	mid_index = int(2**trunc_log) - 1
        	self.__midpoints[length] = mid_index
		return mid_index

	def reArrange(self, lst=None):
		if lst==None:
			new_lst = self.dfs()
			self.__root = self.reArrange(lst=new_lst)
		elif len(lst)==0:
			return None
		else:
			midpoint = self.__midpointCalc(len(lst))
			root = lst[midpoint]
			root.setLeft(self.reArrange(lst=lst[:midpoint]))
			root.setRight(self.reArrange(lst=lst[midpoint+1:]))
			return root

	def __str__(self):
		return ','.join([str(node) for node in self.dfs()])


	def __repr__(self):
		print(self.bfs())
		return str(self)

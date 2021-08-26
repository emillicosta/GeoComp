# Python program to demonstrate 
# circular linked list traversal 

# Structure for a Node 
class Node: 
	
	# Constructor to create a new node 
	def __init__(self, data): 
		self.data = data 
		self.next = None
		self.prev = None

class CircularLinkedList: 
	
	# Constructor to create a empty circular linked list 
	def __init__(self): 
		self.head = None

	# Function to insert a node at the beginning of a 
	# circular linked list 
	def push(self, data): 
		ptr1 = Node(data) 
		temp = self.head 
		
		ptr1.next = self.head 

		# If linked list is not None then set the next of 
		# last node 
		if self.head is not None: 
			ultimo = self.head.prev
			ultimo.next = ptr1
			self.head.prev = ptr1

			ptr1.next = self.head
			ptr1.prev = ultimo

		else: 
			ptr1.next = ptr1 # For the first node 
			ptr1.prev = ptr1

			self.head = ptr1 

	# Function to print nodes in a given circular linked list 
	def printList(self): 
		temp = self.head 
		if self.head is not None: 
			while(True): 
				print(temp.data) 
				temp = temp.next
				if (temp == self.head): 
					break




"""Linked nodes in both direction"""

from typing import Optional, Any


class DoublyLinkedNode:
    """Represents doubly linked list of nodes from a doubly linked list"""

    def __init__(self,
                 next_node: "DoublyLinkedNode" = None,
                 previous_node: "DoublyLinkedNode" = None,
                 value: Any = None) -> None:
        self.next_node: Optional[DoublyLinkedNode] = next_node
        self.previous_node: Optional[DoublyLinkedNode] = previous_node
        self.value: Any = value

    def append(self, value: Any) -> "DoublyLinkedNode":
        """
        Append a new node with the given value

        Parameters
        ----------
        value : any
            The value if the new node

        Returns
        -------
        new_node:
            The created node

        """
        next_node = DoublyLinkedNode(self.next_node, self, value)
        self.next_node = next_node
        return next_node

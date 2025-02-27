# Import List type hint from typing module (similar to Java's java.util.List)
from typing import List
# Import Box class from the same package (. means current package, like Java's relative import)
from .box import Box

class OrderPicker:
    @staticmethod  # Similar to Java's static method
    def filter_and_sort_boxes(boxes: List[Box]) -> List[Box]:
        # Python's filter and lambda (similar to Java's Stream filter)
        cardboard_boxes = filter(lambda box: box.material.lower() == "cardboard", boxes)
        
        # Convert to list and sort (similar to Java's Stream sorted())
        # Note: Python's sort is more concise than Java's Comparator
        return sorted(cardboard_boxes, key=lambda box: box.weight)

    # Alternative more Pythonic way using list comprehension
    @staticmethod
    def filter_and_sort_boxes_pythonic(boxes: List[Box]) -> List[Box]:
        return sorted(
            [box for box in boxes if box.material.lower() == "cardboard"],
            key=lambda box: box.weight
        ) 
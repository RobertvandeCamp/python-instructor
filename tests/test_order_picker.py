# Import Box class from exercises package (absolute import, similar to Java's fully qualified import)
# Note: 'exercises' is found because we set PYTHONPATH=src
from src.exercises.box import Box
from src.exercises.order_picker import OrderPicker

def test_filter_and_sort_boxes():
    # Create test boxes
    boxes = [
        Box(length=10, width=10, height=10, weight=5, 
            material="Cardboard", name="Light Box", number=1),
        Box(length=20, width=20, height=20, weight=10, 
            material="Plastic", name="Medium Box", number=2),
        Box(length=15, width=15, height=15, weight=7, 
            material="Cardboard", name="Another Box", number=3),
    ]

    # Test both methods
    result = OrderPicker.filter_and_sort_boxes(boxes)
    result_pythonic = OrderPicker.filter_and_sort_boxes_pythonic(boxes)

    # Assertions
    assert len(result) == 2  # Only cardboard boxes
    assert result[0].weight < result[1].weight  # Sorted by weight
    assert result == result_pythonic  # Both methods should give same result
    assert all(box.material.lower() == "cardboard" for box in result) 
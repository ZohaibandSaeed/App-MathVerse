import os
from mathverse import MathBoard

def test_board_initialization():
    board = MathBoard("Test")
    assert board.title == "Test"
    assert len(board.steps) == 0

def test_add_step_and_render(tmp_path):
    board = MathBoard("Algebra Test")
    board.add_step("2x + 4 = 10", "Original equation")
    board.add_step("2x = 6", "Subtract 4 from both sides")
    board.add_step("x = 3", "Divide by 2")
    
    # Render to a temporary file
    output_file = tmp_path / "test_output.png"
    result_path = board.render(str(output_file))
    
    assert os.path.exists(result_path)
    assert len(board.steps) == 3
    assert board.steps[0]["equation"] == "$2x + 4 = 10$"

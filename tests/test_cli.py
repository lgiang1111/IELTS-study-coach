# tests/test_cli.py
import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock
from cli import parse_scores, main

def test_parse_scores_valid():
    assert parse_scores("6.0,6.5,5.5,6.0") == [6.0, 6.5, 5.5, 6.0]
    assert parse_scores(" 7.0 , 7.0 , 7.0 , 7.0 ") == [7.0, 7.0, 7.0, 7.0]

def test_parse_scores_invalid_length():
    with pytest.raises(Exception):
        parse_scores("6.0,6.5,5.5")
        
    with pytest.raises(Exception):
        parse_scores("6.0,6.5,5.5,6.0,6.0")

def test_parse_scores_invalid_value():
    with pytest.raises(Exception):
        parse_scores("6.0,six,5.5,6.0")
        
    with pytest.raises(Exception):
        parse_scores("6.0,10.5,5.5,6.0")  # Score out of bounds (0-9)

@patch("cli.execute_study_plan_flow")
@patch("cli.render_schedule_table")
@patch("cli.show_trace_panel")
@patch("cli.console.input")
def test_cli_parameter_mode(mock_console_input, mock_show_trace, mock_render_table, mock_execute_flow):
    # Setup mock responses
    mock_execute_flow.return_value = {
        "coach_response": "Here is your study plan.",
        "reviewer_response": "APPROVED: Looks good.",
        "approved": True
    }
    mock_console_input.side_effect = ["", "1"]
    
    # Mock sys.argv to simulate parameter mode
    test_args = ["cli.py", "--initial", "6.0,6.0,6.0,6.0", "--target", "7.0,7.0,7.0,7.0", "--days", "30"]
    with patch.object(sys, "argv", test_args):
        # Run main - should not raise any error
        main()
        
    mock_execute_flow.assert_called_once()
    mock_render_table.assert_called_once()
    mock_show_trace.assert_called_once()

@patch("cli.execute_study_plan_flow")
@patch("cli.console.input")
def test_cli_interactive_mode_exit(mock_console_input, mock_execute_flow):
    # Mock sys.argv to simulate interactive mode (no arguments)
    test_args = ["cli.py"]
    
    # We want console.input to return "" first (for API key prompt), then "exit" to end the loop
    mock_console_input.side_effect = ["", "exit"]
    
    with patch.object(sys, "argv", test_args):
        main()
        
    # execute_study_plan_flow should not be called since we exited immediately
    mock_execute_flow.assert_not_called()

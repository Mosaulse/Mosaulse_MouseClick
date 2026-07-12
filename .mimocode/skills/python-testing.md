# Python Testing Skill

## Overview

This skill provides guidance for writing and running Python tests using pytest.

## When to Use

- Writing new unit tests
- Debugging test failures
- Improving test coverage
- Mocking external dependencies

## Testing Best Practices

### 1. Test Structure

```python
# test_example.py
import pytest
from models.example import ExampleClass

class TestExampleClass:
    def test_method_success(self):
        # Arrange
        instance = ExampleClass()
        
        # Act
        result = instance.method()
        
        # Assert
        assert result == expected

    def test_method_failure(self):
        with pytest.raises(ExpectedException):
            instance.method_with_error()
```

### 2. Mocking External Dependencies

```python
from unittest.mock import Mock, patch

# Mock keyboard library
@patch('keyboard.add_hotkey')
def test_hotkey_registration(mock_add_hotkey):
    # Test hotkey registration
    mock_add_hotkey.assert_called_once()

# Mock win10toast
@patch('win10toast.ToastNotifier')
def test_notification(mock_toast):
    # Test notification
    mock_toast.show_toast.assert_called_once()
```

### 3. Fixtures

```python
# conftest.py
import pytest

@pytest.fixture
def sample_settings():
    return {
        "interval": 500,
        "hotkey": "F6",
        "is_dark": False,
        "button": "left"
    }

@pytest.fixture
def temp_settings_file(tmp_path):
    settings_file = tmp_path / "settings.json"
    settings_file.write_text("{}")
    return settings_file
```

### 4. Test Coverage

```bash
# Run with coverage
pytest --cov=Scripts --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Common Test Patterns

### Testing PyQt5 Components

```python
from PyQt5.QtWidgets import QApplication
import pytest

@pytest.fixture
def app():
    return QApplication([])

def test_button_click(app):
    from views.components.styled_button import StyledButton
    button = StyledButton("Test")
    button.click()
    # Assert button state changed
```

### Testing Thread Safety

```python
import threading
import time

def test_click_thread():
    from models.clicker_model import ClickThread
    
    thread = ClickThread(interval=100)
    thread.start()
    
    time.sleep(0.5)
    thread.stop()
    thread.join(timeout=1.0)
    
    assert not thread.running
```

## Commands

- Run all tests: `pytest Scripts/tests/ -v`
- Run specific test: `pytest Scripts/tests/test_example.py::test_name -v`
- Run with coverage: `pytest --cov=Scripts`
- Generate coverage report: `pytest --cov=Scripts --cov-report=html`

## Debugging Tips

1. Use `pytest -s` to see print statements
2. Use `pytest --tb=long` for detailed tracebacks
3. Use `pytest -k "test_name"` to run specific tests
4. Use `pytest --lf` to run last failed tests

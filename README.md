# Extending Todo-Backend with Tags

This guide will help you extend your Todo-Backend API to include tags for todos and provide the ability to retrieve todos by specific tags.

## 1. Update Data Structure

Modify your todo data structure to include a 'tags' field for each todo item. You can use a dictionary to represent todos, where each todo item is a dictionary containing 'title', 'order', 'completed', and 'tags' fields. Example:

```python
TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False, 'tags': ['work']},
    1: {'title': '?????', 'order': 2, 'completed': False, 'tags': ['miscellaneous']},
    2: {'title': 'profit!', 'order': 3, 'completed': False, 'tags': ['work', 'social']},
}

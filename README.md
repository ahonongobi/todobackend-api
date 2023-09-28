# Extending Todo-Backend with Tags

I explain how I extended the Todo-Backend API to include tags for todos and added the ability to retrieve todos by specific tags. Below are the steps I followed to do it.

## 1. Updating the Data Structure

I started by modifying our existing todo data structure to include a 'tags' field for each todo item. This way, we can associate one or more tags with each todo item. Here's how the updated `TODOS` data structure looks:

```python
TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False, 'tags': ['work']},
    1: {'title': '?????', 'order': 2, 'completed': False, 'tags': ['miscellaneous']},
    2: {'title': 'profit!', 'order': 3, 'completed': False, 'tags': ['work', 'social']},
}

## 2. Updating the Create Todo Function

To support tags during todo creation, we've modified the `create_todo` function. It now accepts tags in the JSON request data and updates the 'tags' field accordingly. We've also added validation to ensure that tags are provided as a list of strings. Here's the updated code snippet:

```python
# Inside create_todo function
tags = data.get('tags', [])
if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
    return web.json_response({'error': '"tags" must be a list of strings'})
data['tags'] = tags


## 2. Updating the Create Todo Function

To support tags during todo creation, I have modified the `create_todo` function. It now accepts tags in the JSON request data and updates the 'tags' field accordingly. I have also added validation to ensure that tags are provided as a list of strings. Here's the updated code snippet:

```python
# Inside create_todo function
tags = data.get('tags', [])
if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
    return web.json_response({'error': '"tags" must be a list of strings'})
data['tags'] = tags

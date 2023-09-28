# Aiohttp Todo-Backend Project

This is a Todo-Backend project built with aiohttp.

## Informations 

Before you get started, ensure you have the following installed on your system:

- Python (version 3.7 or later)
- pip (Python package manager)
- aiohttp and aiohttp_cors Python packages
- You may use (python -m venv venv and  source venv/bin/activate) 
- For my database i choose MySQL, so execute pip install aiomysql

You can install aiohttp, aiommysql and aiohttp_cors using pip:

```bash
pip install aiohttp aiohttp_cors

```
or 
```bash
pip install -r requirements.txt

```

```bash
pip install aiomysql
```
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
```

## 2. Updating the Create Todo Function

To support tags during todo creation, I have modified the `create_todo` function. It now accepts tags in the JSON request data and updates the 'tags' field accordingly. I have also added validation to ensure that tags are provided as a list of strings. Here's the updated code snippet:

```python
# Inside create_todo function
tags = data.get('tags', [])
if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
    return web.json_response({'error': '"tags" must be a list of strings'})
data['tags'] = tags
```

### 3. Adding an Endpoint to Get Todos by Tag

```markdown
## 3. Adding an Endpoint to Get Todos by Tag

I've created a new endpoint to retrieve todos by a specific tag. This endpoint is named `get_todos_by_tag`. It filters todos based on the tag parameter provided in the URL. Here's the code for the endpoint:

```python
def get_todos_by_tag(request):
    tag = request.match_info['tag']
    todos_with_tag = [{'id': key, **todo} for key, todo in TODOS.items() if tag in todo.get('tags', [])]
    if not todos_with_tag:
        return web.json_response({'error': f'No todos found with the tag "{tag}"'}, status=404)
    return web.json_response(todos_with_tag)

```

## 4. Updating the CORS Configuration

To ensure proper handling of cross-origin requests for the new endpoint that retrieves todos by tag, I've added the following line to our CORS (Cross-Origin Resource Sharing) configuration:

```python
cors.add(app.router.add_get('/todos/tag/{tag}', get_todos_by_tag, name='todos_by_tag'))

# These lines import the necessary modules and libraries for building a web API 
# using aiohttp and configuring Cross-Origin Resource Sharing (CORS) using aiohttp_cors.
import logging
from aiohttp import web
import aiohttp_cors

# This dictionary, TODOS, represents a collection of todo items. 
# Each todo item is represented as a dictionary with keys for 'title', 'order', and 'completed'.

TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False, 'tags':['work']},
    1: {'title': '?????', 'order': 2, 'completed': False, 'tags': ['miscellaneous']},
    2: {'title': 'profit!', 'order': 3, 'completed': False, 'tags': ['work','social']}
}

# This function, get_all_todos, is a request handler that returns a JSON response 
# containing a list of all todo items. It converts the TODOS dictionary into a list of dictionaries, adding an 'id' key to each item.
def get_all_todos(request):
    return web.json_response([
        {'id': key, **todo} for key, todo in TODOS.items()
    ])

# This function, remove_all_todos, is a request handler that clears all todo items by emptying 
# the TODOS dictionary and returns a successful response with HTTP status code 204 (No Content).

def remove_all_todos(request):
    TODOS.clear()
    return web.Response(status=204)

# This function, get_one_todo, retrieves a single todo item by its ID from the TODOS dictionary.
# It first extracts the ID from the request's URL parameters.
# If the ID is not found in the TODOS dictionary, it returns a JSON response with an error message and a 404 status code. Otherwise, it returns the specified todo item as a JSON response.
def get_one_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response({'id': id, **TODOS[id]})

# This asynchronous function, create_todo, is used to create a new todo item
async def create_todo(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    # add for tags part. I did it here in create todo
    tags = data.get('tags', [])
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        return web.json_response({'error': '"tags" must be a list of strings'})

    data['completed'] = bool(data.get('completed', False))
    data['tags'] = tags  # Set the tags field based on the input.

    new_id = max(TODOS.keys(), default=0) + 1
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))

    TODOS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )
# update todo
async def update_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])
# remove todo
def remove_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'})

    del TODOS[id]

    return web.Response(status=204)
# Add an Endpoint to Get Todos by Tag
def get_todos_by_tag(request):
    tag = request.match_info['tag']
    todos_with_tag = [{'id': key, **todo} for key, todo in TODOS.items() if tag in todo.get('tags', [])]

    return web.json_response(todos_with_tag)

#These lines configure CORS (Cross-Origin Resource Sharing) settings for the aiohttp 
# application. It sets up CORS to allow cross-origin requests for various routes defined in the application.

app = web.Application()

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
})

cors.add(app.router.add_get('/todos/', get_all_todos, name='all_todos'))
cors.add(app.router.add_delete('/todos/', remove_all_todos, name='remove_todos'))
cors.add(app.router.add_post('/todos/', create_todo, name='create_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo'))
cors.add(app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo'))
# route to retrive todo by tag. for exemple /todos/tag/work
cors.add(app.router.add_get('/todos/tag/{tag}', get_todos_by_tag, name='todos_by_tag'))
# This code sets up basic logging and runs the aiohttp web application on port 8081.

logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=8081)


import logging
from aiohttp import web
import aiohttp_cors

TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False, 'tags': []},
    1: {'title': '?????', 'order': 2, 'completed': False, 'tags': []},
    2: {'title': 'profit!', 'order': 3, 'completed': False, 'tags': []}
}

TAGS = {
    0: {'title': 'work'},
    1: {'title': 'social'},
    2: {'title': 'miscellaneous'}
}

def get_all_todos(request):
    return web.json_response([
        {'id': key, **todo} for key, todo in TODOS.items()
    ])

def remove_all_todos(request):
    TODOS.clear()
    return web.Response(status=204)

def get_one_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response({'id': id, **TODOS[id]})

async def create_todo(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    data['tags'] = []
    new_id = max(TODOS.keys(), default=0) + 1
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))

    TODOS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )

async def update_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])

def remove_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'})

    del TODOS[id]

    return web.Response(status=204)

def get_all_tags(request):
    return web.json_response([
        {'id': key, **tag} for key, tag in TAGS.items()
    ])

# Handler for creating a new tag
async def create_tag(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    new_id = max(TAGS.keys(), default=0) + 1
    data['id'] = new_id

    # Include the URL in the response
    data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

    TAGS[new_id] = data

    return web.json_response(data, status=201)


#
async def get_tag(request):
    tag_id = int(request.match_info['id'])
    
    if tag_id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)
    
    return web.json_response({'id': tag_id, **TAGS[tag_id]})
#
async def update_tag(request):
    tag_id = int(request.match_info['id'])
    
    if tag_id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)
    
    data = await request.json()
    TAGS[tag_id]['title'] = data.get('title', TAGS[tag_id]['title'])

    # Include the updated URL in the response
    TAGS[tag_id]['url'] = str(request.url)

    return web.json_response(TAGS[tag_id])

# Handler for deleting all tags
def remove_all_tags(request):
    TAGS.clear()
    return web.Response(status=204)
# delete specific tags

async def delete_tag(request):
    tag_id = int(request.match_info['id'])
    
    if tag_id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)
    
    del TAGS[tag_id]
    
    return web.Response(status=204)
# associating a tag with a todo

async def associate_tag_with_todo(request):
    todo_id = int(request.match_info['id'])

    if todo_id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()

    if 'tag_id' not in data:
        return web.json_response({'error': '"tag_id" is a required field'}, status=400)
    tag_id = data['tag_id']

    if tag_id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    # Associate the tag with the todo by appending the tag_id to the tags array
    if tag_id not in TODOS[todo_id]['tags']:
        TODOS[todo_id]['tags'].append(tag_id)

    # Return the updated todo
    updated_todo = {
        'id': todo_id,
        **TODOS[todo_id]
    }

    return web.json_response(updated_todo)

# getting the tag list associated with a todo

def get_tags_for_todo(request):
    todo_id = int(request.match_info['id'])

    if todo_id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    todo = TODOS[todo_id]
    tag_ids = todo.get('tags', [])

    tags_for_todo = [{'id': tag_id, **TAGS[tag_id], 'todos': []} for tag_id in tag_ids if tag_id in TAGS]

    for tag in tags_for_todo:
        tag['todos'] = [{'id': todo_id, **TODOS[todo_id]}]

    return web.json_response(tags_for_todo)

#
async def get_todos_for_tag(request):
    tag_id = int(request.match_info['tag_id'])

    if tag_id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    todos_for_tag = [{'id': key, **todo} for key, todo in TODOS.items() if tag_id in todo['tags']]

    response = {
        'tag_id': tag_id,
        'todos': todos_for_tag
    }

    return web.json_response(response)



# Handler for getting an empty array after deleting all tags
def get_empty_array(request):
    return web.json_response([])

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

# Add routes for tags
cors.add(app.router.add_get('/tags/', get_all_tags, name='all_tags'))
cors.add(app.router.add_post('/tags/', create_tag, name='create_tag'))
cors.add(app.router.add_delete('/tags/', remove_all_tags, name='remove_tags'))
cors.add(app.router.add_get('/after_delete', get_empty_array))
cors.add(app.router.add_get('/tags/{id:\d+}', get_tag, name='one_tag'))
cors.add(app.router.add_patch('/tags/{id:\d+}', update_tag, name='update_tag'))
cors.add(app.router.add_delete('/tags/{id:\d+}', delete_tag, name='delete_tag'))
cors.add(app.router.add_post('/todos/{id:\d+}/tags/', associate_tag_with_todo, name='associate_tag_with_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}/tags/', get_tags_for_todo, name='get_tags_for_todo'))
cors.add(app.router.add_get('/tags/{tag_id:\d+}/todos/', get_todos_for_tag, name='get_todos_for_tag'))

logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=8080)

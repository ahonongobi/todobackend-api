# These lines import the necessary modules and libraries for building a web API
# using aiohttp and configuring Cross-Origin Resource Sharing (CORS) using aiohttp_cors. And using aiomysql for mysql as i choose mysql for my project (pip install aiomysql)
import logging
from aiohttp import web
import aiohttp_cors
import aiomysql

# connect to database mysql


async def create_pool():
    pool = await aiomysql.create_pool(
        host="localhost",
        port=3306,
        user="root",
        password="",
        db="todos_app",
        autocommit=True,
    )
    return pool


# This dictionary, TODOS, represents a collection of todo items.
# Each todo item is represented as a dictionary with keys for 'title', 'order', and 'completed'.

TODOS = {
    0: {"title": "build an API", "order": 1, "completed": False, "tags": ["work"]},
    1: {"title": "?????", "order": 2, "completed": False, "tags": ["miscellaneous"]},
    2: {"title": "profit!", "order": 3, "completed": False, "tags": ["work", "social"]},
}


async def get_all_todos(request):
    pool = await create_pool()  # Await the create_pool coroutine here
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM todos")
            result = await cur.fetchall()
            return web.json_response(result)


# This function, get_all_todos, is a request handler that returns a JSON response
# containing a list of all todo items. It converts the TODOS dictionary into a list of dictionaries, adding an 'id' key to each item.
# def get_all_todos(request):
#    return web.json_response([
#        {'id': key, **todo} for key, todo in TODOS.items()
#    ])

# Define the function to remove all todos
async def remove_all_todos(request):

    pool = await create_pool()

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM todos")
        return web.Response(status=204)


# Define the function to get a single todo by ID
async def get_one_todo(request):
    id = int(request.match_info["id"])

    # Connect to the database
    pool = await create_pool()

    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # Fetch the todo from the database based on its ID
            await cur.execute("SELECT * FROM todos WHERE id = %s", (id,))
            todo = await cur.fetchone()

            # If no todo is found, return a 404 error
            if not todo:
                return web.json_response({"error": "Todo not found"}, status=404)

            # Return the retrieved todo as JSON response
            return web.json_response(todo)


# This asynchronous function, create_todo, is used to create a new todo item
# Define the function to create a new todo
async def create_todo(request):
    try:
        data = await request.json()
    except ValueError:
        return web.json_response(
            {"error": "Invalid JSON format in request body"}, status=400
        )

    if "title" not in data:
        return web.json_response({"error": '"title" is a required field'}, status=400)
    title = data["title"]
    if not isinstance(title, str) or not len(title):
        return web.json_response(
            {"error": '"title" must be a string with at least one character'},
            status=400,
        )

    # Ensure the 'tags' field is a list of strings
    tags = data.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        return web.json_response(
            {"error": '"tags" must be a list of strings'}, status=400
        )

    # Connect to the database
    pool = await create_pool()

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Insert the new todo into the database
            insert_query = "INSERT INTO todos (title,`order`, completed, tags) VALUES (%s, %s, %s, %s)"
            values = (
                title,
                data.get("order", 1),
                data.get("completed", False),
                ",".join(tags),
            )
            await cur.execute(insert_query, values)
            await conn.commit()

            # Retrieve the ID of the newly inserted todo
            new_id = cur.lastrowid

    # Construct the URL for the new todo
    url = str(request.url.join(request.app.router["one_todo"].url_for(id=str(new_id))))

    # Return a successful response with HTTP status code 303 (See Other)
    return web.Response(headers={"Location": url}, status=303)


# Define the function to update a todo
async def update_todo(request):
    id = int(request.match_info["id"])

    # Connect to the database
    pool = await create_pool()

    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # Check if the todo with the given ID exists in the database
            await cur.execute("SELECT * FROM todos WHERE id = %s", (id,))
            todo = await cur.fetchone()

            # If the todo doesn't exist, return a 404 error
            if not todo:
                return web.json_response({"error": "Todo not found"}, status=404)

            # Update the todo with the data from the request
            data = await request.json()
            update_query = "UPDATE todos SET title = %s, `order` = %s, completed = %s, tags = %s WHERE id = %s"
            await cur.execute(
                update_query,
                (data["title"], data["order"], data["completed"], data["tags"], id),
            )
            await conn.commit()

            # Fetch the updated todo
            await cur.execute("SELECT * FROM todos WHERE id = %s", (id,))
            updated_todo = await cur.fetchone()

    # Return the updated todo as a JSON response
    return web.json_response(updated_todo)


# remove todo
async def remove_todo(request):
    id = int(request.match_info["id"])

    # Connect to the database
    pool = await create_pool()

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Check if the todo exists
            await cur.execute("SELECT id FROM todos WHERE id = %s", (id,))
            existing_todo = await cur.fetchone()

            if not existing_todo:
                return web.json_response({"error": "Todo not found"}, status=404)

            # Delete the todo from the database
            await cur.execute("DELETE FROM todos WHERE id = %s", (id,))
            await conn.commit()

    # Return a successful response with HTTP status code 204 (No Content)
    return web.Response(status=204)


# Add an Endpoint to Get Todos by Tag
async def get_todos_by_tag(request):
    tag = request.match_info["tag"]

    # Connect to the database
    pool = await create_pool()

    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # Query the database to retrieve todos with the specified tag
            await cur.execute("SELECT * FROM todos WHERE FIND_IN_SET(%s, tags)", (tag,))
            todos_with_tag = await cur.fetchall()

    # Return a JSON response with the list of todos with the specified tag
    return web.json_response(todos_with_tag)


# These lines configure CORS (Cross-Origin Resource Sharing) settings for the aiohttp
# application. It sets up CORS to allow cross-origin requests for various routes defined in the application.

app = web.Application()

# Configure default CORS settings.
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*",
        )
    },
)

cors.add(app.router.add_get("/todos/", get_all_todos, name="all_todos"))
cors.add(app.router.add_delete("/todos/", remove_all_todos, name="remove_todos"))
cors.add(app.router.add_post("/todos/", create_todo, name="create_todo"))
cors.add(app.router.add_get("/todos/{id:\d+}", get_one_todo, name="one_todo"))
cors.add(app.router.add_patch("/todos/{id:\d+}", update_todo, name="update_todo"))
cors.add(app.router.add_delete("/todos/{id:\d+}", remove_todo, name="remove_todo"))
# route to retrive todo by tag. for exemple /todos/tag/work
cors.add(app.router.add_get("/todos/tag/{tag}", get_todos_by_tag, name="todos_by_tag"))
# This code sets up basic logging and runs the aiohttp web application on port 8081.

logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=8083)

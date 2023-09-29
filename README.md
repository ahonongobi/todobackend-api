# todobackend-aiohttp

## Whats the exercice says ?


Extend the Todo-Backend sample project (aiohttp or Koa):

    Add tags (e.g. 'work', 'social', 'miscellaneous'...) so we can add one or more tag to todos (many-to-many relationship between todos and tags). We should be able to add tags and find todos linked to specific tag(s) directly from your REST API.
    Add database persistence such that todos and tags are not lost upon server restart. You are free to choose any database system you want (make sure you are using an asyncio-based DB driver/interface with Python).
    Your API should comply with our specs (source code). A yaml file can be downloaded from the email and deployed on Swagger Editor (https://editor.swagger.io/) to test your API. Your submission must pass all tests on local http://todospecs.thing.zone/?http://localhost:8080 as the server does http://todospecs.thing.zone/?http://todo.thing.zone.



Yet another [todo backend](http://todobackend.com) written in Python 3.5 with aiohttp. Original code [from alec.thoughts import \*](http://justanr.github.io/getting-start-with-aiohttpweb-a-todo-tutorial).

## Usage

```
python3 aiotodo.py
```
```python

 pip install -r requirements.txt

 ```

## Tests

You can run validate the application with http://www.todobackend.com/specs/.

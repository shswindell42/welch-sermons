path = "data/lessons"

def get_sermon(title):
    file_path = f"{path}/{title}.txt"
    with open(file_path, 'r') as fp:
        content = fp.read()

    return {
        "title": title,
        "content": content
    }

def query(query):
    return [
        {
            "title": "1st-peter",
            "meta": "This is the first test"
        },
        {
            "title": "be-converted",
            "meta": "Some sample text"
        },
        {
            "title": "church-discipline",
            "meta": "This is what was embedded"
        }
    ]
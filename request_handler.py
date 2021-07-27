import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts.request import get_all_posts, delete_post
from users import get_all_users, create_user


class HandleRequests(BaseHTTPRequestHandler):
    '''note that is needed'''

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        if "?" in resource:

            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value)

        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        '''do_OPTIONS'''
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        self._set_headers(200)

        response = {}

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed
            if resource == "posts":
                if id is not None:
                    response = f"{get_made_up_function_single(id)}"
                else:
                    response = f"{get_all_posts()}"
            if resource == "users":
                response = f"{get_all_users()}"

        # elif len(parsed) == 3:
        #     ( resource, key, value ) = parsed

        #     if key == "madeUpListEmail" and resource == "madeUpList":
        #         response = get_made_up_function(value)

        #     elif key == "madeUpListEmail2" and resource == "madeUpList":
        #         response = get_made_up_function(value)

        self.wfile.write(response.encode())

    def do_POST(self):
        '''Post method'''
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource_from_url, _) = self.parse_url(self.path)

        new_item = None

        if resource_from_url == "register":
            new_item = create_user(post_body)

        # elif resource_from_url == "madeUpList2":
        #     new_item = create_made_up_function(post_body)
        self.wfile.write(f"{new_item}".encode())

    def do_DELETE(self):
        '''Delete method'''
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)

        # elif resource == "madeUpList2":
        #     delete_made_up_function2(id)

        self.wfile.write("".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        # if resource == "madeUpList":
        #     success = update_made_up_function(id, post_body)
        # elif resource == "madeUpList2":
        #     success = update_made_up_function2(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())


def main():
    '''main'''
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

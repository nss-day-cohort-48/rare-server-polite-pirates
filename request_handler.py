from comments.request import create_comment, get_all_comments
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from posts.request import get_all_posts, get_single_post, delete_post, create_post, update_post
from users import get_all_users, create_user, login_user
from categories import get_all_categories, create_category, update_category, delete_category
from tags import get_all_tags, get_single_tag, create_tag, delete_tag


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
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"

            elif resource == "users":
                response = f"{get_all_users()}"
            
            elif resource == "comments":
                response = f"{get_all_comments()}"

            elif resource == "categories":
                response = f"{get_all_categories()}"
            
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            

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

        elif resource_from_url == "categories":
            new_item = create_category(post_body)

        elif resource_from_url == "tags":
            new_item = create_tag(post_body)

        elif resource_from_url == "posts":
            new_item = create_post(post_body)
        

        elif resource_from_url == "comments":
            new_item = create_comment(post_body)

        elif resource_from_url == "login":
            new_item = login_user(post_body)
            
        self.wfile.write(f"{new_item}".encode())

    def do_DELETE(self):
        '''Delete method'''
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)

        elif resource == "categories":
            delete_category(id)

        elif resource == "tags":
            delete_tag(id)

        self.wfile.write("".encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "posts":
            success = update_post(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)

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

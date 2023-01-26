from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

from jinja2 import Environment, PackageLoader, select_autoescape

import repo


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        status = 200  # меняется в дальнейшем
        posts = []
        if self.path == '/':
            posts = repo.get_posts()
            template_name = 'index.html'
        elif self.path == '/add_post':
            template_name = 'add_post.html'
        else:
            template_name = 'not_found.html'
            status = 404

        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # используется шаблонизатор jinja2
        env = Environment(
            loader=PackageLoader('main'), autoescape=select_autoescape()
        )
        template = env.get_template(template_name)
        response_body = bytes(template.render(posts=posts), encoding='utf-8')

        self.wfile.write(response_body)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        if self.path == '/add_post':
            title = form.getvalue('title')
            author = form.getvalue('author')
            content = form.getvalue('content')
            repo.add_post(title=title, author=author, content=content)
            self.do_GET()


def runserver(server_class=HTTPServer, handler_class=HttpProcessor):
    server_address = ('0.0.0.0', 80)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


if __name__ == '__main__':
    repo.create_posts_table()
    runserver()

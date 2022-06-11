import http.server
import socketserver
# import ssl 

PORT = 8081
Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.socket = ssl.wrap_socket (httpd.socket,
#         keyfile="sslKeys/key.pem",
#         certfile='sslKeys/privateKey.key', server_side=True)
#     httpd.serve_forever()




with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
# twistd -no web --path ./ -c ./sslKeys/cert.pem -k ./sslKeys/key.pem
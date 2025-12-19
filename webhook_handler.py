import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# 要执行的脚本路径
SCRIPT_PATH = "/root/update_blog.sh"
# Python 服务监听的地址和端口
HOST_NAME = "127.0.0.1" # 监听本地回环地址，更安全
PORT_NUMBER = 18080

class SimpleRefreshHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/refresh':
            # 1. 响应客户端
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            
            # 2. 执行脚本
            try:
                # 使用 shell=True 执行脚本，注意安全风险，但在此处符合需求
                result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True, check=True, shell=True)
                response_text = f"Script {SCRIPT_PATH} executed successfully.\nOutput:\n{result.stdout}\nError (if any):\n{result.stderr}"
            except subprocess.CalledProcessError as e:
                response_text = f"Error executing script {SCRIPT_PATH}. Return code: {e.returncode}\nOutput:\n{e.stdout}\nError:\n{e.stderr}"
            except FileNotFoundError:
                response_text = f"Error: Script file not found at {SCRIPT_PATH}"
            except Exception as e:
                response_text = f"An unexpected error occurred: {e}"

            # 3. 将执行结果写入响应 (可选，但推荐用于调试)
            self.wfile.write(response_text.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, PORT_NUMBER), SimpleRefreshHandler)
    print(f"Server started http://{HOST_NAME}:{PORT_NUMBER}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

import asyncio
import json
from .command_handler import CommandHandler
from .services import AuthService

class AsyncServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.command_handler = CommandHandler()
        self.auth_service = AuthService()
    
    async def start(self):
        # 初始化管理员用户
        await self.auth_service.init_admin_user()
        
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        # 获取服务器实际监听的IP地址和端口
        server_address = self.server.sockets[0].getsockname() if self.server.sockets else (self.host, self.port)
        actual_host = server_address[0]
        actual_port = server_address[1]
        print(f"Server started on {actual_host}:{actual_port}")
        print(f"Listening for incoming connections...")
        async with self.server:
            await self.server.serve_forever()
    
    async def handle_client(self, reader, writer):
        client_addr = writer.get_extra_info('peername')
        print(f"Client connected: {client_addr}")
        
        try:
            while True:
                # 异步接收数据
                data = await reader.read(4096)
                if not data:
                    break
                
                try:
                    # 解析客户端消息
                    message = json.loads(data.decode())
                    command = message.get("command")
                    data = message.get("data", {})
                    session_id = message.get("session_id")
                    
                    print(f"Received command: {command} from {client_addr}")
                    
                    # 处理命令
                    response = await self.command_handler.handle_command(command, data, session_id)
                    
                    # 添加响应的客户端信息
                    response["client_id"] = message.get("client_id")
                    response["timestamp"] = message.get("timestamp")
                    
                    # 异步发送响应
                    writer.write(json.dumps(response).encode())
                    await writer.drain()
                    
                except json.JSONDecodeError as e:
                    # 处理JSON解析错误
                    error_response = {
                        "status": "error",
                        "message": f"Invalid JSON format: {e}",
                        "command": "unknown"
                    }
                    writer.write(json.dumps(error_response).encode())
                    await writer.drain()
                except Exception as e:
                    # 处理其他错误
                    error_response = {
                        "status": "error",
                        "message": f"Internal server error: {e}",
                        "command": "unknown"
                    }
                    writer.write(json.dumps(error_response).encode())
                    await writer.drain()
                    print(f"Error handling client {client_addr}: {e}")
        
        except Exception as e:
            print(f"Unexpected error with client {client_addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"Client disconnected: {client_addr}")
    
    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Server stopped")
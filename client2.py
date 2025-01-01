import threading
import socket
import sys


class Send(threading.Thread):
    '''Lắng nghe đầu vào từ dòng lệnh để gửi tin nhắn tới máy chủ'''

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        """Lấy dữ liệu từ dòng lệnh và gửi tin nhắn"""
        while True:
            message = input(f'{self.name}: ')
            # Nếu nhập "Quit", thoát chương trình
            if message == 'Quit':
                self.sock.sendall(f'Server: {self.name} đã rời khỏi phòng chat'.encode('utf-8'))
                break
            # Ngược lại, gửi tin nhắn đến server
            else:
                self.sock.sendall(f'{self.name}: {message}'.encode('utf-8'))
        print('\nĐang thoát...')
        self.sock.close()
        sys.exit(0)


class Receive(threading.Thread):
    '''Lắng nghe tin nhắn từ server và hiển thị lên terminal'''

    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        """Nhận dữ liệu từ server"""
        while True:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    print(f'\r{message}\n{self.name}: ', end='')
                else:
                    print('\nMất kết nối tới server!')
                    print('\nĐang thoát...')
                    self.sock.close()
                    sys.exit(0)
            except OSError:
                print("Đã mất kết nối tới server.")
                sys.exit(0)


class Client:
    '''Quản lý kết nối và chức năng gửi/nhận tin nhắn'''

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None

    def start(self):
        """Kết nối tới server và khởi động các thread gửi/nhận"""
        print(f'Đang kết nối tới {self.host}:{self.port}...')
        try:
            self.sock.connect((self.host, self.port))
        except Exception as e:
            print(f'Không thể kết nối tới server: {e}')
            sys.exit(1)

        print(f'Kết nối thành công tới {self.host}:{self.port}!')
        print()
        self.name = input('Tên của bạn: ').strip()
        print()
        print(f'Chào mừng {self.name}! Chuẩn bị gửi và nhận tin nhắn...\n')

        # Tạo các thread gửi và nhận
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)

        # Chạy cả hai thread
        send.start()
        receive.start()

        # Gửi thông báo tham gia phòng chat đến server
        self.sock.sendall(f'Server: {self.name} đã tham gia phòng chat. Hãy gửi lời chào!'.encode('utf-8'))

        print("\rSẵn sàng! Nhập 'Quit' để rời khỏi phòng chat.\n")
        print(f'{self.name}: ', end='')


def main(host, port):
    """Khởi chạy ứng dụng chat chỉ với terminal"""
    client = Client(host, port)
    client.start()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Chatroom Client (No GUI)")
    parser.add_argument('host', help='Địa chỉ IP của server')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='Cổng TCP (mặc định là 1060)')
    args = parser.parse_args()

    main(args.host, args.p)

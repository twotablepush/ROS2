# 목표
# spin 또는 circle서비스를 호출하는 서비스 클라이언트 노드 생성
# 비동기 호출 방식(call_async)사용하여 서비스를 호출
# 서비스의 사용 가능 유무 확인

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty

class EmptyServiceClient(Node):
    def __init__(self):
        super().__init__('empty_service_client')
        self.client = self.create_client(Empty, 'spin')  # 또는 'circle'

        # 클라이언트의 타입 및 이름과 일치하는 서비스를 사용할 수 있는지 1초에 한 번 확인
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')

        # 서비스 요청을 위한 요청 객체 생성
        self.req = Empty.Request()

    def send_request(self):
        self.future = self.client.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    empty_client = EmptyServiceClient()
    empty_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(empty_client, timeout_sec=0.1)
        if empty_client.future.done():
            try:
                response = empty_client.future.result()
            except Exception as e:
                empty_client.get_logger().info('service call failed %r' % (e,))
            else:
                empty_client.get_logger().info('service call completed')
            break

        # 서비스 서버의 response를 기다리면서 추가적인 동작 수행 가능
        empty_client.get_logger().info('additional work...!')

    empty_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
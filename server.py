import socket
import time

from multiprocessing import Pool, cpu_count, Manager
from multiprocessing.pool import ThreadPool


# 从队列中拿出数据，发给所有连接上的客户端
def send_data(dict_proxy, queue_proxy):
    while True:
        # 从队列中拿出消息，发送给所有连接上来的客户端
        data = queue_proxy.get()
        print(data.decode())
        for conn in dict_proxy.values():
            conn.send(data)


def worker_thread(connection, user, remote_address, list_proxy, dict_proxy, queue_proxy):
    while True:
        try:
            recv_data = connection.recv(1024)
            if recv_data:
                data = "{user}&{user}:\n{data}".format(user=user, data=recv_data.decode())
                # 把消息添加到到队列中
                queue_proxy.put(data.encode())
            else:
                raise Exception
        except:
            # 从字典中删掉退出的客户端
            dict_proxy.pop(remote_address)
            list_proxy.remove(user)
            data = "{user}&用户 {user} 退出".format(user=user)
            # 把退出消息添加到队列中
            queue_proxy.put(data.encode())
            connection.close()
            break


def worker_process(server, dict_proxy, queue_proxy, list_proxy):
    # 分配2倍CPU个数的线程
    thread_pool = ThreadPool(cpu_count() * 2)
    thread_pool.apply_async(send_data, args=(dict_proxy, queue_proxy))

    # 返还客户端的信息
    error_message_username = "连接服务器失败，用户名已存在, 请重试"
    login_success = "连接服务器成功~"

    # 发送数据
    while True:
        # 接收客户端连接，生成对等套接字
        connection, remote_address = server.accept()
        usr = connection.recv(1024).decode()
        if usr not in list_proxy:
            list_proxy.append(usr)
            connection.send((login_success + "&" + "|".join(list_proxy)).encode())

            # 接收数据
            dict_proxy[remote_address] = connection
            data = "{user}&用户 {user} 登录".format(user=usr)
            time.sleep(1.5)
            queue_proxy.put(data.encode())
            thread_pool.apply_async(worker_thread, args=(connection, usr, remote_address, list_proxy, dict_proxy, queue_proxy))
        else:
            connection.send(error_message_username.encode())
            connection.close()


if __name__ == '__main__':

    server = socket.socket()
    server.bind(('127.0.0.1', 8088))
    # 最多供1000客户端连接
    server.listen(1000)

    mgr = Manager()
    # 进程安全字典，用来保存连接上来的客户端，
    dict_proxy = mgr.dict()
    # 进程安全队列，把客户端发过来的消息通过队列传递
    queue_proxy = mgr.Queue()
    list_proxy = mgr.list()
    n = cpu_count()  # cpu核数
    process_pool = Pool(n)
    # 充分利用CPU，为每一个CPU分配一个进程
    for i in range(n):
        # 把server服务端放到进程里面
        process_pool.apply_async(worker_process, args=(server, dict_proxy, queue_proxy, list_proxy))

    # 停止提交数据
    process_pool.close()
    # 阻塞，等待子进程运行完毕才继续运行主进程
    process_pool.join()


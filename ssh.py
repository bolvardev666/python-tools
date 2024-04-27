import asyncio, asyncssh, json


class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    async def exe_cmd(self, cmd):
        async with asyncssh.connect(host=self.host,
                                    port=self.port,
                                    username=self.username,
                                    password=self.password) as conn:
            res = await conn.run(cmd, check=True)
            print(res.stdout, end='')

    async def sftp_send(self, src_file, dst_file):
        async with asyncssh.connect(host=self.host,
                                    port=self.port,
                                    username=self.username,
                                    password=self.password) as conn:
            async with conn.start_sftp_client() as sftp:
                await sftp.put(src_file, dst_file)

    async def sftp_read(self, src_file, dst_file):
        """
        :param src_file: 服务器上的文件
        :param dst_file: 本机的路径
        :return: 没
        """
        async with asyncssh.connect(host=self.host,
                                    port=self.port,
                                    username=self.username,
                                    password=self.password) as conn:
            async with conn.start_sftp_client() as sftp:
                await sftp.get(src_file, dst_file)


def load_json():
    """
    从json中读取主机连接信息
    :return: json object
    """
    with open('hosts.json', 'r', encoding='utf-8') as f:
        return json.load(f)


async def main():
    hosts = load_json()
    for host in hosts:
        client = SSHClient(
            host=hosts[host]["host"],
            port=hosts[host]["port"],
            username=hosts[host]["username"],
            password=hosts[host]["password"]
        )
        print("-------------------------------------------------------> %s" % host)
        # await client.exe_cmd("cat /etc/os-release")
        await client.sftp_read('/root/aaaaa', 'C:\\Users\\bolva\\PycharmProjects\\demo\\ssh', )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except OSError as e:
        print("超时: %s" % e)

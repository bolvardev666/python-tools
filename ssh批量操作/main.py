import asyncio, asyncssh, json


class SSHClient:
    def __init__(self, ssh_ip, ssh_port, ssh_user, ssh_password, method_name, method_args):
        self.ssh_ip = ssh_ip
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.method_name = method_name
        self.method_args = method_args
        self.conn = None

    async def connect(self):
        async with asyncssh.connect(host=self.ssh_ip,
                                    port=self.ssh_port,
                                    username=self.ssh_user,
                                    password=self.ssh_password
                                    ) as conn:
            self.conn = conn

    async def exe_cmd(self):
        res = await self.conn.run(self.method_args, check=True)
        # print(res.stdout, end='')
        return res.returncode

    async def sftp_download(self):
        async with self.conn.start_sftp_client() as sftp:
            await sftp.get(self.method_args[0], self.method_args[1])

    async def sftp_upload(self):
        async with self.conn.start_sftp_client() as sftp:
            await sftp.put(self.method_args[0], self.method_args[1])


async def main():
    with open('hosts.json', 'r', encoding='utf-8') as f:
        hosts = json.load(f)
    for host in hosts:
        if hasattr(SSHClient, hosts[host]["method_name"]):
            method = getattr(SSHClient, hosts[host]["method_name"])
            client = SSHClient(
                ssh_ip=hosts[host]["host"],
                ssh_port=hosts[host]["port"],
                ssh_user=hosts[host]["username"],
                ssh_password=hosts[host]["password"],
                method_name=hosts[host]["method_name"],
                method_args=hosts[host]["method_args"]
            )
            await client.connect()
            res = await method(client)
            print(res)

        else:
            print("method not found")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except OSError as e:
        print(f"ssh连接似乎存在问题\n{e}")

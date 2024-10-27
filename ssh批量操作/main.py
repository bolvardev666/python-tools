import asyncio, asyncssh, json
from os.path import split

from click import argument


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
        try:
            self.conn = await asyncssh.connect(host=self.ssh_ip,
                                        port=self.ssh_port,
                                        username=self.ssh_user,
                                        password=self.ssh_password,
                                        known_hosts=None
                                        )
        except asyncssh.Error as e:
            print(f"连接失败\n{e}")
    async def exe_cmd(self):
        res = await self.conn.run(self.method_args, check=True)
        # print(res.stdout, end='')
        return res.returncode

    async def exe_cmd_ret(self):
        res = await self.conn.run(self.method_args, check=True)
        return res.stdout

    async def sftp_download(self):
        """
        下载文件
        :return: 状态码
        """
        tmp_args = self.method_args.split(" ")
        print(tmp_args)
        async with self.conn.start_sftp_client() as sftp:
            await sftp.get(tmp_args[0], tmp_args[1])

    async def sftp_upload(self,src=None,dst=None):
        if src is not None and dst is not None:
            tmp_args = [src,dst]
        else:
            tmp_args = self.method_args.split(" ")

        async with self.conn.start_sftp_client() as sftp:
            await sftp.put(tmp_args[0], tmp_args[1])

    async def exe_script(self):
        tmp_args = self.method_args.split(" ")
        await self.sftp_upload(tmp_args[0], tmp_args[1])
        if len(tmp_args) == 3:
            res = await self.conn.run(f"bash {tmp_args[1]} {tmp_args[2]}", check=True)
        else:
            res = await self.conn.run(f"bash {tmp_args[1]}", check=True)
        return res.returncode

    async def exe_script_ret(self):
        tmp_args = self.method_args.split(" ")
        await self.sftp_upload(tmp_args[0], tmp_args[1])
        if len(tmp_args) == 3:
            res = await self.conn.run(f"bash {tmp_args[1]} {tmp_args[2]}", check=True)
        else:
            res = await self.conn.run(f"bash {tmp_args[1]}", check=True)
        return res.stdout


    async def close(self):
        if self.conn:
            self.conn.close()
            print(f"关闭连接{self.ssh_ip}")

async def main():
    with open('hosts.json', 'r', encoding='utf-8') as f:
        hosts = json.load(f)
    for host in hosts:
        if hosts[host].get("running") is False:
            continue    # 当存在runing = false是跳过这个主机

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
            await client.close()
            print(res)

        else:
            print("method not found")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except OSError as e:
        print(f"ssh连接似乎存在问题\n{e}")

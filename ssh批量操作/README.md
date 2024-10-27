# 程序使用说明


#### 1. 本程序是用于批量操作服务器的脚本，支持批量执行命令、批量上传文件、批量下载文件、批量执行脚本等功能。
#### 2.所以操作都在hosts.json文件中配置，具体配置说明如下：
``` json
{
  "主机1": {      // 主机名，可以随便取
    "host": "192.168.3.102", // 主机ip
    "port": 22, // 主机端口
    "username": "root", // 主机用户名
    "password": "1", // 主机密码
    "method_name": "exe_cmd",   // 执行的方法名，目前支持的方法有：exe_cmd、exe_cmd_ret、sftp_upload、sftp_download、exe_script
    "method_args": "ip r" // 方法的参数，根据不同的方法，参数不同
  },
    "主机2": {
      "host": "192.168.3.105",
      "port": 22,
      "username": "root",
      "password": "1",
      "method_name": "exe_cmd_ret",
      "method_args": "ip r"
    }
}
```
### 3.method_name：
- exe_cmd：执行命令，不返回结果
  - method_args：需要执行的命令,str
- exe_cmd_ret：执行命令，返回结果
  - method_args：需要执行的命令,str
- sftp_upload：上传文件
  - method_args：上传的文件路径，arg1 本地文件路径，arg2 远程文件路径
- sftp_upload：下载文件
  - method_args：下载的文件路径，arg1 远程文件路径，arg2 本地文件路径
- exe_script：执行脚本，不返回结果
  - method_args：需要执行的脚本路径，ar1 脚本本地路径, arg2 脚本远程路径, arg3 脚本参数(可选)
- exe_script_ret：执行脚本，返回结果
  - - method_args：需要执行的脚本路径，ar1 脚本本地路径, arg2 脚本远程路径, arg3 脚本参数(可选)


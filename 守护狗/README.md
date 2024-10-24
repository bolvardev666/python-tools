# 说明

## python

- 1.python会在首次运行时添加一个,每{cron_time}执行一次
  - 同时创建一个./.flag文件,下次启动检查有它就不再创建计划任务
- 2.读取json中服务名称,服务[ start | stop | check ] 方式来检查服务

## json
文件名称固定conf.json
- 通过**os.system(check)**检查,返回值是0就表示服务没问题
- 不为0就执行stop -> start
- 理论上有较小的概率出现一直起不来的情况,需要手动检查
```json
{
  '服务名': {
    'start': '启动shell命令',
    'stop': '关闭shell命令',
    'check': '检查shell命令'
  }
}
```
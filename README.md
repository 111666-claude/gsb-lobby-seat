# lobby-seat

房间座位：固定座位数的房间，处理入座、排队补位、准备状态、开局判定与房主转移。
只用 Python 标准库。

```
python3 -m lobby.cli --sample seat
python3 -m lobby.cli --sample queue
python3 -m lobby.cli --sample start
python3 -m lobby.cli --sample ready
python3 -m lobby.cli --sample host
python3 -m lobby.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **座位分配**：入座时占用编号最小的空座，座位号必须在 `0` 到 `seats-1` 之间；
  重复入座返回原来的座位，不占新座。
- **排队补位**：座位满了进等待队列（先到先得）；有人离开释放座位时，
  队首等待者立刻补进这个座位，等待队列相应出队。
- **准备状态**：只有已入座的人能设置准备；玩家离开座位或补位到新座位时，
  准备状态一律重置为未准备。
- **开局判定**：所有座位都有人且在场玩家全部准备时才返回 True，
  否则返回 False 且不改动房间状态。
- **房主**：房主是座位号最小的在场玩家；房间空时没有房主。
- **不变量**：同一个玩家最多占一个座位；在场人数不超过 `seats`；
  同一串入座、离开、准备序列重复执行结果相同。
- **查询代价**：座位查询 O(1)，`scanned` 不随房间人数线性增长。
- **规模**：10 万人的房间，每秒 10 万次查询，查询 O(1)，内存 O(人数)。

## 输出契约（不改格式）

```
seat=..
waiting=.. promoted=..
start=..
host=..
scanned=..
```

## 目录

```
lobby/core.py   座位、补位、准备与房主
lobby/cli.py    命令行入口
tests/          unittest 用例
```

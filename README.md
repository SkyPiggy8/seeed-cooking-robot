# reBot Cooking Agent

这是我们给 Seeed「胡闹厨房」黑客松准备的机械臂做饭项目。

硬件上主要用 reBot Arm B601-DM、Orbbec Gemini 2 RGB-D 相机和 Jetson / reComputer。软件这边先不追求一步到位，而是先把一条最小链路跑通：看见桌面上的物体，算出大概位置，规划一个抓取点，然后通过安全封装过的技能让机械臂去抓、放、倒、搅。

现在仓库里有两条路线：

1. Python 主线：目标检测、深度定位、手眼转换、抓取规划、技能调度这一套框架。
2. LeRobot 保底路线：时间不够时，先遥操作录一段机械臂动作，现场按录制结果复现。

目前 Python 主线主要还是 mock / dry-run，适合先确认代码结构和流程。真实相机、真实机械臂 SDK、模型权重这些还没有完全接进来。

## 现在能跑什么

当前可以在没有真实硬件的电脑上跑通这些东西：

- mock RGB-D 相机数据；
- mock 物体检测结果；
- 从检测框和深度图估算 3D 位置；
- 把相机坐标转换到机械臂基座坐标；
- 生成 top-down 抓取点；
- 用 dry-run 方式打印机械臂动作；
- 执行 YAML 菜谱。

已经放进来的菜谱有两个：

- `recipes/tomato_egg.yaml`：番茄炒蛋半自动流程；
- `recipes/simple_burger.yaml`：汉堡摆盘流程。

另外 `grasp_targets/` 里整理了一些比较适合夹爪测试的物体，比如番茄、汉堡、调料瓶、鸡蛋碗等。这个文件夹主要是给现场摆物体和调抓取点时看的。

## 项目结构

```text
seeed_studio/
├── configs/                  # 相机、检测、机械臂和工作区配置
├── docs/                     # 管线、安全和里程碑记录
├── grasp_targets/            # 适合夹取的物体清单
├── lerobot/                  # 遥操作录制相关文件
├── recipes/                  # YAML 菜谱
├── scripts/                  # 测试和演示脚本
└── src/rebot_cooking_agent/  # Python 主代码
```

## 安装

Python 建议用 3.10 以上。Windows 下可以这样装：

```powershell
cd C:\Users\zhuyu\Desktop\seeed_studio

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

只跑 mock 流程的话，不需要相机、不需要模型权重，也不需要接机械臂。

LeRobot 那条路线要单独准备环境。现场机器上可以先试一下：

```bash
conda activate lerobot
lerobot-teleoperate --help
lerobot-record --help
```

如果这两个命令都能出来帮助信息，再去看 `lerobot/训练脚本.txt` 里的具体命令。那里面记录了我们试过的遥操作、Orbbec 相机和录制参数。

## 运行

单独测试抓取和放置：

```powershell
python scripts\test_pick_place.py --object burger --target plate
```

跑汉堡摆盘：

```powershell
python scripts\run_cooking_demo.py --recipe recipes\simple_burger.yaml
```

跑番茄炒蛋：

```powershell
python scripts\run_cooking_demo.py --recipe recipes\tomato_egg.yaml
```

这些命令默认都是 dry-run，只会打印动作，不会真的动机械臂。后面接真实硬件时，必须先确认工作区、安全高度、急停和夹爪状态，再考虑加 `--execute`。

## LeRobot 录制方案

`lerobot/` 是我们为了比赛现场准备的备用方案。想法很简单：如果视觉抓取来不及调稳定，就先用 leader arm 带着 follower arm 走一遍，把动作录下来；演示时再复现这段动作。

目前这个目录里有：

- `calibration/`：leader 和 follower 的校准文件；
- `seeed_rebot_b601_dm/do1`、`do2`、`do3`：已经整理过的数据目录；
- `训练脚本.txt`：现场调试时留下来的命令。

这部分现在还没有接进 Python 技能系统。也就是说，`scripts/run_cooking_demo.py` 跑的是 Python mock 菜谱，`lerobot/` 跑的是遥操作录制，两边还没有做成一个统一入口。后面如果还有时间，可以补一个 `scripts/replay_lerobot_demo.py` 之类的脚本，把录制动作变成一键回放。

## 安全边界

这个项目里上层只应该调用技能，比如 `pick("tomato")`、`place("plate")`、`stir("pan")`。不要从规划层直接写电机电流、关节速度、CAN 帧或者未经检查的轨迹。

真实运动前至少要检查：

- 目标点是否在 workspace 里；
- Z 高度是否高于桌面安全高度；
- 是否接近热锅、刀具或其它危险区域；
- 急停是否触发；
- 关节和夹爪状态是否正常。

比赛现场优先稳定，不追求速度。热锅、刀具、明火相关动作先用冷锅或摆盘动作替代。

## 分工和贡献

这个项目是几个人一起赶出来的，代码、硬件调试和现场方案基本是边试边补。

- @朱煜：主要整理 Python 项目结构、菜谱执行流程、README 和 GitHub 发布内容，也负责把 mock 流程先跑通。
- @席浩东：主要参与 reBot Arm、LeRobot 遥操作和录制流程的调试，整理了现场可以用的录制命令和校准文件。
- @邹绍凯：主要参与厨房物体、夹取目标和演示流程设计，帮忙确认哪些物体更适合现场抓取和摆盘。

## 后面要补的东西

现在还没完成的主要是这些：

- reBot Arm 真实 SDK 还没有接到 `RebotArmController`；
- Orbbec Gemini 2 现在还没有替换掉 mock camera；
- YOLO / YOLO-OBB 还没有真正加载模型；
- 手眼标定现在还是示例变换，需要换成实测标定结果；
- `pour` 和 `stir` 现在只有接口，还没有真实轨迹；
- LeRobot 录制数据还没有做成一键回放脚本；
- README 后面还要补演示视频、PPT 和现场照片。

## 推到 GitHub

如果 GitHub 上还没建仓库，先去网页上新建一个空仓库。不要勾选自动生成 README、`.gitignore` 或 license，因为这个本地目录里已经有文件了。

第一次推送可以这样做：

```powershell
cd C:\Users\zhuyu\Desktop\seeed_studio

git init
git add .
git commit -m "Initial cooking robot demo"
git branch -M main
git remote add origin https://github.com/SkyPiggy8/<你的仓库名>.git
git push -u origin main
```

如果后面继续改：

```powershell
git status
git add .
git commit -m "Update demo docs"
git push
```

推之前看一眼有没有误提交大文件。模型权重、很大的录制数据、视频文件最好不要直接塞进 git，GitHub 单文件超过 100 MB 会直接拒绝。

# reBot Cooking Agent：胡闹厨房黑客松项目

这个仓库是 Seeed「胡闹厨房」黑客松的机械臂烹饪项目。目标是用 reBot Arm B601-DM、Orbbec Gemini 2 RGB-D 相机和一套受安全限制的技能库，做出可以现场演示的抓取、放置、倒入、搅拌流程。

当前主线先跑通 mock 版本：相机、检测、深度定位、手眼转换、抓取规划和机器人控制都可以在没有真实硬件的环境下 dry-run。时间不够时，仓库里也放了 LeRobot 的遥操作录制方案，用来先录一遍机械臂动作，再按录制结果复现。

## 当前已经完成

- 最小 Python 项目结构已经搭好，核心模块都可以 import。
- `RGBDCamera`、`ObjectDetector`、`PoseEstimator`、`HandEyeTransform`、`GraspPlanner` 都有 mock 路径。
- `RebotArmController` 支持 dry-run，不会直接控制真实电机。
- `pick`、`place`、`pick_and_place`、`pour`、`stir` 技能接口已经接好。
- `RecipeExecutor` 可以执行 YAML 菜谱。
- 已有两条菜谱：
  - `recipes/tomato_egg.yaml`：番茄炒蛋半自动流程。
  - `recipes/simple_burger.yaml`：汉堡摆盘流程。
- `grasp_targets/` 里整理了适合夹爪测试的物体清单。
- `lerobot/` 里放了遥操作、录制和校准相关文件，作为现场保底方案。

## 目录结构

```text
seeed_studio/
├── configs/                          # 相机、检测、机械臂和工作区配置
├── docs/                             # 管线、安全和里程碑说明
├── grasp_targets/                    # 适合机械臂夹取的物体清单
├── lerobot/                          # LeRobot 遥操作和录制方案
│   ├── calibration/                  # 机械臂和遥操作端校准文件
│   ├── seeed_rebot_b601_dm/          # 已录制的数据集目录
│   └── 训练脚本.txt                  # 现场调试用命令记录
├── recipes/                          # YAML 菜谱
├── scripts/                          # 测试和演示脚本
└── src/rebot_cooking_agent/          # Python 主代码
```

## 安装

建议 Python 3.10 或更高版本。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

如果只是跑 mock 流程，不需要接相机、不需要模型权重，也不需要真实机械臂。

LeRobot 录制方案需要单独准备 LeRobot 环境和机械臂驱动。`lerobot/训练脚本.txt` 里的命令默认已经有可用的 `lerobot` 环境、串口权限、CAN 适配器和相机驱动。现场机器上可以先检查：

```bash
conda activate lerobot
lerobot-teleoperate --help
lerobot-record --help
```

如果这两个命令不存在，先安装 LeRobot 和 reBot / Seeed 对应的硬件支持包，再回到本仓库运行录制命令。

## 快速运行

测试单物体抓取和放置：

```powershell
python scripts\test_pick_place.py --object burger --target plate
```

运行汉堡摆盘菜谱：

```powershell
python scripts\run_cooking_demo.py --recipe recipes\simple_burger.yaml
```

运行番茄炒蛋菜谱：

```powershell
python scripts\run_cooking_demo.py --recipe recipes\tomato_egg.yaml
```

默认都是 dry-run。只有在真实硬件已经接好、安全边界确认过之后，才考虑加 `--execute`。

## LeRobot 录制和复现方案

`lerobot/` 是现场时间不够时的备用路线。思路是：先用 leader arm 遥操作 follower arm，把一段动作录下来；演示时再按录制数据复现动作。这样可以绕开还没完全稳定的检测、抓取规划和菜谱规划。

现在目录里有：

- `lerobot/calibration/robots/seeed_b601_dm_follower/follower1.json`
- `lerobot/calibration/teleoperators/rebot_arm_102_leader/rebot_arm_102_leader.json`
- `lerobot/seeed_rebot_b601_dm/do1`
- `lerobot/seeed_rebot_b601_dm/do2`
- `lerobot/seeed_rebot_b601_dm/do3`
- `lerobot/训练脚本.txt`

常用命令记录在 `lerobot/训练脚本.txt`。其中主要用到：

```bash
lerobot-teleoperate
lerobot-record
```

注意：这一块目前还没有封装进 `src/rebot_cooking_agent` 的技能系统里。也就是说，Python 主线可以 dry-run 菜谱，LeRobot 这边可以做遥操作和录制，但两边还没有合成一个一键运行的回放脚本。

## 安全原则

1. 上层规划只能调用技能，不能直接控制电机。
2. 真实运动前必须检查 workspace、安全高度、危险区域和急停状态。
3. 所有硬件调用必须保留 dry-run 或 mock 入口。
4. 热锅、刀具、明火相关动作先不做真实自动化。
5. 比赛现场优先稳定，不追求速度。

## 还没有完成的事情

- 真实 reBot Arm Python SDK 还没有接入主线 `RebotArmController`。
- Orbbec Gemini 2 的真实相机读取还没有替换 mock camera。
- YOLO / YOLO-OBB 模型还没有真正加载，当前检测是固定 mock 结果。
- 手眼标定现在还是示例变换，需要换成真实标定文件。
- `pour` 和 `stir` 目前只保留接口，还没有真实倾倒和搅拌轨迹。
- `lerobot/` 的录制数据还没有接成一键回放脚本。
- 安全检查还有待接入真实关节限位、急停状态和危险区域传感。
- README 里还没有放最终演示视频、PPT 和现场照片。

## 推到 GitHub

第一次推送：

```powershell
git init
git add .
git commit -m "Initial cooking robot demo scaffold"
git branch -M main
git remote add origin git@github.com:<你的GitHub用户名>/<你的仓库名>.git
git push -u origin main
```

如果你用 HTTPS 地址：

```powershell
git remote add origin https://github.com/<你的GitHub用户名>/<你的仓库名>.git
git push -u origin main
```

以后更新代码：

```powershell
git status
git add .
git commit -m "Update cooking demo docs and recipes"
git push
```



# AGENTS.md：Codex / AI Agent 项目规则

本文件是给 Codex、OpenClaw、Claude Code 或其他 AI 编程 Agent 阅读的项目规则。请严格遵守。

---

## 1. 项目背景

本项目用于 Seeed「胡闹厨房」黑客松。硬件包括：

- reBot Arm B601-DM 机械臂
- Orbbec Gemini 2 RGB-D 相机
- reComputer Robotics J4012 / Jetson Orin NX 边缘计算平台
- 厨房场景物体：番茄、鸡蛋、碗、盘子、锅、铲子、调料、主食等

目标是通过：

```text
目标检测 + 深度定位 + 手眼标定 + 抓取规划 + Agent 技能调度
```

实现机械臂自主/半自主完成烹饪 Demo。

---

## 2. 最重要原则

Agent 只能调度技能，不能直接控制电机。

允许：

```python
pick("tomato")
place("bowl")
pour("egg_bowl", "pan")
stir("pan", seconds=5)
move_home()
```

禁止：

```python
set_motor_current(...)
set_joint_velocity(...)
write_raw_can_frame(...)
直接生成未检查的关节轨迹
绕过 safety.py 控制机械臂
```

---

## 3. 开发优先级

请按以下顺序开发，不要跳步：

1. Mock 模式下跑通项目结构。
2. 相机接口 `perception/camera.py`。
3. 目标检测接口 `perception/detector.py`。
4. 深度定位与坐标转换 `pose_estimator.py`、`handeye_transform.py`。
5. 机械臂封装 `robot/rebot_arm.py`，必须支持 dry-run。
6. 安全检查 `robot/safety.py`。
7. 技能库 `skills/pick.py`、`skills/place.py`、`skills/pour.py`、`skills/stir.py`。
8. YAML 菜谱执行器 `agent/recipe_executor.py`。
9. 简单 Agent 任务规划 `agent/planner.py`。
10. Demo 脚本 `scripts/run_cooking_demo.py`。

---

## 4. 代码风格要求

- Python 版本：建议 3.10+
- 所有核心函数必须写 type hints。
- 所有真实硬件调用必须有 `dry_run=True` 或 mock fallback。
- 所有脚本必须支持 `--dry-run`。
- 所有坐标必须显式标注 frame，例如：`camera_color_optical_frame`、`robot_base`。
- 不要把模型权重、数据集、密钥提交到 GitHub。
- 不要把本地绝对路径写死在代码里。
- 配置写进 `configs/*.yaml`，不要硬编码。

---

## 5. 安全要求

每次运动前必须检查：

- 目标点是否在 workspace 内。
- Z 高度是否高于桌面安全高度。
- 是否超过机械臂关节限制。
- 是否可能靠近热源、刀具或危险区域。
- 是否处于 emergency stop 状态。

实现时必须保留以下函数接口：

```python
def validate_pose(pose: Pose3D) -> bool: ...
def validate_workspace(point: Point3D) -> bool: ...
def emergency_stop() -> None: ...
```

---

## 6. 推荐模块接口

### perception/detector.py

```python
@dataclass
class Detection:
    label: str
    confidence: float
    bbox_xyxy: tuple[int, int, int, int]
    mask: Optional[Any] = None
    angle_rad: Optional[float] = None

class ObjectDetector:
    def detect(self, image: np.ndarray) -> list[Detection]: ...
```

### perception/pose_estimator.py

```python
@dataclass
class ObjectPose:
    label: str
    position_camera: Point3D
    yaw_camera: float | None
    confidence: float

class PoseEstimator:
    def estimate(self, detection: Detection, depth_image: np.ndarray, intrinsics: CameraIntrinsics) -> ObjectPose: ...
```

### robot/rebot_arm.py

```python
class RebotArmController:
    def move_home(self) -> None: ...
    def move_to_pose(self, pose: Pose3D, speed: float = 0.2) -> None: ...
    def open_gripper(self) -> None: ...
    def close_gripper(self) -> None: ...
    def stop(self) -> None: ...
```

### skills

```python
def pick(object_name: str) -> SkillResult: ...
def place(target_name: str) -> SkillResult: ...
def pick_and_place(object_name: str, target_name: str) -> SkillResult: ...
def pour(source_name: str, target_name: str) -> SkillResult: ...
def stir(target_name: str, seconds: float) -> SkillResult: ...
```

---

## 7. Agent 行为约束

Agent 输出必须是结构化计划，不要输出自由文本动作：

```json
{
  "task": "tomato_egg",
  "steps": [
    {"skill": "detect", "object": "tomato"},
    {"skill": "pick", "object": "tomato"},
    {"skill": "place", "target": "pan"}
  ]
}
```

如果目标不存在，Agent 必须：

1. 请求重新检测。
2. 尝试备用目标名。
3. 失败后停止并给出明确错误。

不要无限重试。

---

## 8. 当前 Codex 第一阶段任务

请先完成以下内容：

```text
Task 1:
实现项目的最小可运行 Python scaffold。
要求：
- 所有模块可 import。
- 所有 dataclass 定义完整。
- robot controller 支持 mock/dry-run。
- test_pick_place.py 能在无硬件环境下跑通。
- 配置从 YAML 读取。
- 输出清晰日志。
```

完成后，再继续：

```text
Task 2:
接入真实 reBot Arm Python SDK 和 Orbbec Gemini 2 相机。
要求保留 mock 模式。
```

---

## 9. 不要做的事

- 不要一开始就实现 VLA 或模仿学习。
- 不要删除 mock 模式。
- 不要把安全检查写成空函数。
- 不要把 Agent 直接接到底层电机控制。
- 不要让 Demo 依赖网络 API 才能运行。
- 不要在比赛最后阶段大改架构。


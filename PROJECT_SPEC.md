# PROJECT_SPEC：reBot Cooking Agent 系统设计

## 1. 一句话方案

用 RGB-D 相机看清桌面物体，再把物体位置换算到机械臂坐标系里。上层只调用安全封装过的技能，比如抓取、放下、倒入和搅拌，不直接碰底层电机控制。

## 2. 系统 Pipeline

```text
User Task / Recipe YAML
        ↓
Agent Planner
        ↓
Skill Router
        ↓
Perception: RGB-D + YOLO
        ↓
3D Pose Estimation
        ↓
Hand-Eye Transform
        ↓
Grasp Planner
        ↓
Safety Validator
        ↓
reBot Arm Controller
        ↓
Cooking Execution
```

## 3. 坐标系

建议至少维护以下坐标系：

- `camera_color_optical_frame`：相机彩色光学坐标系
- `camera_depth_optical_frame`：深度坐标系
- `robot_base`：机械臂基座坐标系
- `tool0`：机械臂末端执行器坐标系
- `gripper`：夹爪中心坐标系
- `workspace`：桌面任务区域

## 4. 感知模块

输入：RGB 图、深度图、相机内参。

输出：

```python
Detection(label, confidence, bbox_xyxy, angle_rad)
ObjectPose(label, position_camera, yaw_camera, confidence)
ObjectPoseBase(label, position_base, yaw_base, confidence)
```

优先识别类别：

```text
tomato, egg, egg_bowl, bowl, pan, plate, spatula, seasoning, burger
```

## 5. 抓取模块

第一版抓取策略：

1. 使用检测框中心作为抓取中心。
2. 使用深度图中检测框中心附近的中位数深度。
3. 使用 YOLO-OBB / 最小外接矩形短轴方向作为夹爪方向。
4. pre-grasp 点在目标点上方 8-12 cm。
5. grasp 点下降到目标上方 1-3 cm。
6. 夹爪闭合后先垂直 lift，再水平移动。

## 6. 技能库

每个技能都应该返回：

```python
SkillResult(success: bool, message: str, data: dict)
```

必须支持：

- `detect(object_name)`
- `pick(object_name)`
- `place(target_name)`
- `pick_and_place(object_name, target_name)`
- `pour(source, target)`
- `stir(target, seconds)`
- `move_home()`

## 7. Agent 模块

Agent 输入：

```text
做番茄炒蛋
```

Agent 输出：

```yaml
- skill: detect
  object: tomato
- skill: pick
  object: tomato
- skill: place
  target: pan
- skill: pick
  object: egg_bowl
- skill: pour
  source: egg_bowl
  target: pan
- skill: stir
  target: pan
  seconds: 5
```

## 8. 备用方案

现场比赛一定要留后手：

1. 如果规划不稳定，直接执行固定 YAML 菜谱。
2. 如果目标检测不稳定，使用固定物体位置表。
3. 如果真实抓取失败，保留半自动确认模式：检测到目标后人工按 Enter 再执行。
4. 如果热锅动作风险大，改成冷锅演示或摆盘演示。

## 9. 演示成功标准

- Agent 能根据菜谱输出技能序列。
- 系统能识别至少 5 种厨房物体。
- 机械臂能稳定完成至少 3 类动作：pick、place、stir/pour。
- 最终展示两道流程，其中一道为主食。

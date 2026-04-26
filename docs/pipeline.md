# Pipeline：当前应该实现什么

## 1. 第一优先级

先实现单物体抓取闭环：

```text
RGB-D 读取 → 目标检测 → 深度定位 → 手眼转换 → 抓取规划 → 安全检查 → pick/place
```

不要一开始做完整 VLA 或模仿学习。

## 2. 关键接口

- `ObjectDetector.detect(image)`：返回检测框和类别。
- `PoseEstimator.estimate(detection, depth, intrinsics)`：返回 camera frame 中的 3D 位姿。
- `HandEyeTransform.to_base(object_pose)`：转换到 robot base。
- `GraspPlanner.plan_top_down_grasp(object_pose)`：生成 pregrasp/grasp/lift。
- `RebotArmController.move_to_pose(pose)`：执行或 dry-run。
- `RecipeExecutor.execute_file(recipe.yaml)`：执行菜谱。

## 3. 黑客松展示链路

1. 展示相机画面和检测框。
2. 展示检测物体的 3D 坐标。
3. 展示机械臂抓起一个物体并放到指定位置。
4. 展示 Agent 根据菜谱调用技能序列。
5. 展示两道菜的演示视频。

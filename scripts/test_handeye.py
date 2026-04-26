from rebot_cooking_agent.perception.camera import RGBDCamera
from rebot_cooking_agent.perception.detector import ObjectDetector
from rebot_cooking_agent.perception.pose_estimator import PoseEstimator
from rebot_cooking_agent.perception.handeye_transform import HandEyeTransform


def main() -> None:
    cam = RGBDCamera(mock_mode=True)
    det = ObjectDetector(mock_mode=True)
    est = PoseEstimator()
    tf = HandEyeTransform()
    rgb, depth, intrinsics = cam.read()
    tomato = det.find_one(rgb, "tomato")
    assert tomato is not None
    pose_cam = est.estimate(tomato, depth, intrinsics)
    pose_base = tf.to_base(pose_cam)
    print("camera:", pose_cam)
    print("base:", pose_base)


if __name__ == "__main__":
    main()

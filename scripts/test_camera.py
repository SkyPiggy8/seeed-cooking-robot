from rebot_cooking_agent.perception.camera import RGBDCamera


def main() -> None:
    camera = RGBDCamera(mock_mode=True)
    rgb, depth, intrinsics = camera.read()
    print("RGB:", rgb.shape, "Depth:", depth.shape, "Intrinsics:", intrinsics)


if __name__ == "__main__":
    main()

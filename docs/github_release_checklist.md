# GitHub Release Checklist

提交前检查：

- [ ] README.md 可以说明项目目标和运行方式
- [ ] AGENTS.md 明确写清开发约束和安全边界
- [ ] 所有脚本支持 dry-run 或 mock
- [ ] 没有提交模型权重、密钥、本地路径
- [ ] `python scripts/test_pick_place.py` 可以跑通
- [ ] `recipes/*.yaml` 可以被执行器读取
- [ ] PPT 和演示视频链接写入 README

推荐命令：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python scripts/test_pick_place.py --object tomato --target bowl
python scripts/run_cooking_demo.py --recipe recipes/tomato_egg.yaml
```

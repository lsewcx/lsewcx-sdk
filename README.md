# lsewcx

个人工具箱 / SDK，开发早期阶段。目前只搭好了项目骨架：CLI 入口 + 基于 loguru 的统一日志配置。

技术栈：Python 3.12 · [uv](https://docs.astral.sh/uv/) · [loguru](https://github.com/Delgan/loguru) · [python-dotenv](https://github.com/theskumar/python-dotenv)

## 环境要求

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/)

## 快速开始

```bash
# 安装依赖（含开发依赖）
uv sync

# 运行 CLI
uv run lsewcx

# 或在代码中使用
import lsewcx

lsewcx.main()
```

## 日志配置

日志等级通过环境变量 `LSEWCX_LOG_LEVEL` 控制：

| 变量 | 默认值 | 可选值 |
| --- | --- | --- |
| `LSEWCX_LOG_LEVEL` | `INFO` | `TRACE` / `DEBUG` / `INFO` / `SUCCESS` / `WARNING` / `ERROR` / `CRITICAL` |

两种设置方式：

1. 复制 `.env.example` 为 `.env`，修改其中的值（`.env` 已被 `.gitignore` 忽略，不会提交）
2. 临时覆盖，真实环境变量优先于 `.env`：

   ```bash
   LSEWCX_LOG_LEVEL=DEBUG uv run lsewcx
   ```

行为说明：包在 import 时会从当前工作目录向上查找 `.env`，并用**唯一的 sink** 替换 loguru 的现有配置（包括自带的默认 sink）。也就是说它会接管整个进程的 loguru 输出，适合把它当独立工具使用；如果以后要发布给别人 import，需要改成显式的 `configure_logging()` 调用方式。

## 项目结构

```
src/lsewcx/
├── __init__.py          # 包入口，CLI 的 main()
└── config/
    └── logger.py        # 日志配置：.env / 环境变量 → loguru
```

## 开发

```bash
# 代码格式化（建议提交前执行，顺序固定：先 isort 再 black）
uv run isort src/
uv run black src/
```

### Git 提交钩子

仓库自带 Conventional Commits 提交钩子（`.githooks/`），**新克隆的仓库需要启用一次**：

```bash
git config core.hooksPath .githooks
```

启用后：

- `git commit`（不加 `-m`）会弹出类型选择菜单，依次填写 scope、描述、补充说明，自动生成 `feat(logger): xxx` 格式的信息
- `git commit -m "..."` 不弹菜单，但信息必须符合 `<类型>(<可选 scope>): <描述>` 格式，否则会被拒绝
- 可用类型：`feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `build` / `ci` / `chore` / `revert`
- 紧急情况可用 `git commit --no-verify` 跳过检查

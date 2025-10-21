# 将当前 monorepo 拆分为 4 个独立仓库的指南

本仓库目前包含 4 个彼此独立的项目：
- Franklin（Python/Tkinter 桌面端）
- arxiv_llm_digest（Python CLI + PySide6 GUI）
- IDconvert（Python/Tkinter 小工具）
- DNAtranslate（前端 JavaScript 工具）

如果你希望将它们拆分为 4 个单独的 Git 仓库（保留各自目录的提交历史），推荐使用 git subtree。以下脚本示例提供了可复用的做法。

注意：
- 该操作不会更改原有仓库历史；它会基于子目录生成可独立推送的分支。
- 你需要先在远端创建 4 个空仓库（或使用已存在的仓库）。
- 运行前确保工作区干净（没有未提交修改）。

## 一键脚本（推荐）

你可以直接运行仓库根目录下的 `scripts/split_repos.sh`（先按需替换远端仓库地址）：

```bash
bash scripts/split_repos.sh
```

脚本将：
- 为每个子目录创建一个独立分支（仅包含该子目录历史）
- 将分支推送到你指定的远端仓库

## 手动执行步骤（参考）

以下是以 Franklin 子目录为例的手动执行步骤，其他目录同理：

```bash
# 1) 基于子目录导出一条新的分支（仅保留 Franklin 相关历史）
git subtree split --prefix=Franklin -b split/Franklin

# 2) 添加远端（将 URL 替换为你的空仓库地址）
git remote add franklin-origin https://github.com/your-org/Franklin.git

# 3) 推送分支到新仓库（首次推送覆盖目标分支）
git push franklin-origin split/Franklin:main
```

对 arxiv_llm_digest、IDconvert、DNAtranslate 重复上述步骤，分别替换 `--prefix`、远端名与目标仓库地址即可。

## 拆分后的仓库内容建议

每个独立仓库建议保留/新增：
- 独立的 README.md（使用本仓库子目录下已有 README 作为基础）
- 独立的 .gitignore（本仓库已在各子项目目录内放置了示例）
- requirements.txt（如适用；IDconvert 不需要额外依赖）
- 构建脚本（如 PyInstaller 脚本）
- LICENSE（如有需要）

## 常见问题

- Q：为什么使用 git subtree 而不是 git filter-repo？
  - A：subtree 为原生命令，通常无需额外安装；同时能保留子目录的历史，简单可靠。
- Q：推送失败/权限不足？
  - A：检查远端地址和权限；确保新仓库为空或允许强制推送到 main 分支。
- Q：如何验证拆分结果？
  - A：clone 新仓库，确认文件结构与运行说明；检查提交历史仅与对应子目录相关。

---

如需进一步自动化（例如创建远端仓库、设置默认分支保护等），可在 CI 或运维脚本中扩展本指南。

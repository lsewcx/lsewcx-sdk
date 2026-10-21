from huggingface_hub import hf_hub_download, snapshot_download


class Downloader:
    """统一下载器：每种下载方式对应一个方法，目前支持 Hugging Face Hub。"""

    def hf(
        self,
        repo_id: str,
        filename: str,
        *,
        revision: str = "main",
        local_dir: str | None = None,
    ) -> str:
        """从 Hugging Face Hub 下载单个文件，返回本地路径。"""
        return hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            revision=revision,
            local_dir=local_dir,
        )

    def hf_snapshot(
        self,
        repo_id: str,
        *,
        revision: str = "main",
        local_dir: str | None = None,
    ) -> str:
        """下载整个仓库的所有文件，返回本地目录。"""
        return snapshot_download(
            repo_id=repo_id,
            revision=revision,
            local_dir=local_dir,
        )

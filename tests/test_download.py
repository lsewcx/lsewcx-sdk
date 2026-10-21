from lsewcx.utils import download
from lsewcx.utils.download import Downloader


def test_hf_forwards_args(monkeypatch):
    captured = {}

    def fake_hf_hub_download(**kwargs):
        captured.update(kwargs)
        return "/cache/model.bin"

    monkeypatch.setattr(download, "hf_hub_download", fake_hf_hub_download)

    path = Downloader().hf(
        "org/model",
        "model.bin",
        revision="v1",
        local_dir="models/model",
    )

    assert path == "/cache/model.bin"
    assert captured == {
        "repo_id": "org/model",
        "filename": "model.bin",
        "revision": "v1",
        "local_dir": "models/model",
    }


def test_hf_uses_defaults(monkeypatch):
    captured = {}

    def fake_hf_hub_download(**kwargs):
        captured.update(kwargs)
        return "/cache/model.bin"

    monkeypatch.setattr(download, "hf_hub_download", fake_hf_hub_download)

    Downloader().hf("org/model", "model.bin")

    assert captured["revision"] == "main"
    assert captured["local_dir"] is None


def test_hf_snapshot_forwards_args(monkeypatch):
    captured = {}

    def fake_snapshot_download(**kwargs):
        captured.update(kwargs)
        return "/cache/model"

    monkeypatch.setattr(download, "snapshot_download", fake_snapshot_download)

    path = Downloader().hf_snapshot(
        "org/model",
        revision="v1",
        local_dir="models/model",
    )

    assert path == "/cache/model"
    assert captured == {
        "repo_id": "org/model",
        "revision": "v1",
        "local_dir": "models/model",
    }


def test_hf_snapshot_uses_defaults(monkeypatch):
    captured = {}

    def fake_snapshot_download(**kwargs):
        captured.update(kwargs)
        return "/cache/model"

    monkeypatch.setattr(download, "snapshot_download", fake_snapshot_download)

    Downloader().hf_snapshot("org/model")

    assert captured["revision"] == "main"
    assert captured["local_dir"] is None

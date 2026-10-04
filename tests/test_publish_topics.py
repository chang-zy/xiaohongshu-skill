from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from xhs import publish
from xhs.errors import PublishError


class TopicPage:
    def __init__(self, topics: list[str], candidates: list[str] | None = None) -> None:
        self.topics = topics
        self.candidates = candidates or []
        self.clicks: list[tuple[str, int]] = []
        self.typed: list[str] = []

    def evaluate(self, expression: str) -> list[str]:
        if expression.startswith("Array.from"):
            return self.candidates
        return self.topics

    def has_element(self, selector: str) -> bool:
        return True

    def type_text(self, text: str, delay_ms: int = 0) -> None:
        self.typed.append(text)

    def click_nth_element(self, selector: str, index: int) -> None:
        self.clicks.append((selector, index))


def test_plain_hashtag_text_is_not_a_selected_topic() -> None:
    with pytest.raises(PublishError, match="市场观察"):
        publish._verify_topics(TopicPage([]), ".editor", ["市场观察"])


def test_one_selected_topic_does_not_validate_five() -> None:
    with pytest.raises(PublishError, match="全球股市"):
        publish._verify_topics(
            TopicPage(["数据可视化"]),
            ".editor",
            ["市场观察", "全球股市", "A股", "美股", "数据可视化"],
        )


def test_all_five_verified_topics_are_accepted() -> None:
    names = ["市场观察", "全球股市", "A股", "美股", "数据可视化"]
    assert publish._verify_topics(TopicPage(names), ".editor", names) == names


def test_exact_candidate_is_clicked_and_finished_with_space(monkeypatch) -> None:
    monkeypatch.setattr(publish.time, "sleep", lambda _: None)
    page = TopicPage(["市场观察"], ["#市场观察日记\n100次浏览", "#市场观察\n200次浏览"])

    publish._input_single_tag(page, ".editor", "市场观察")

    assert page.clicks == [(f"{publish.TAG_TOPIC_CONTAINER} {publish.TAG_FIRST_ITEM}", 1)]
    assert "".join(page.typed) == "#市场观察 "


def test_click_without_official_topic_raises_error(monkeypatch) -> None:
    monkeypatch.setattr(publish.time, "sleep", lambda _: None)
    page = TopicPage([], ["#市场观察\n200次浏览"])

    with pytest.raises(PublishError, match="话题未被正式识别: 市场观察"):
        publish._input_single_tag(page, ".editor", "市场观察")

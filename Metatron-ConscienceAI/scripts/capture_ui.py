import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main(url: str, out_dir: str, viewport_width: int = 1280, viewport_height: int = 900) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
        page.goto(url, wait_until="domcontentloaded")
        # Wait for streaming UI controls to be ready
        try:
            page.wait_for_selector("section.controls", timeout=5000)
        except Exception:
            page.wait_for_timeout(1500)

        # Full page (light theme)
        page.screenshot(path=str(out / "webui_full_light.png"), full_page=True)

        # Toggle theme and capture dark
        try:
            page.click("#themeToggle")
            page.wait_for_timeout(300)
        except Exception:
            pass
        page.screenshot(path=str(out / "webui_full_dark.png"), full_page=True)

        # Controls section
        try:
            controls = page.locator("section.controls")
            controls.screenshot(path=str(out / "webui_controls.png"))
        except Exception:
            pass

        # Chat section
        try:
            chat = page.locator("#chat")
            chat.screenshot(path=str(out / "webui_chat.png"))
        except Exception:
            pass

        # Demonstrations of new features
        # 1) List uploads
        try:
            print("[capture] Listing uploads...")
            page.wait_for_selector("#uploadsListBtn", timeout=4000)
            page.click("#uploadsListBtn")
            page.wait_for_timeout(600)
            page.locator("#uploadsInfo").screenshot(path=str(out / "uploads_list.png"))
        except Exception as e:
            print("[capture] uploads list failed:", e)

        # 2) Clear uploads
        try:
            print("[capture] Clearing uploads...")
            page.wait_for_selector("#uploadsClearBtn", timeout=4000)
            page.click("#uploadsClearBtn")
            page.wait_for_timeout(800)
            page.locator("#uploadsInfo").screenshot(path=str(out / "uploads_clear.png"))
        except Exception as e:
            print("[capture] uploads clear failed:", e)

        # 3) RSS add/list/ingest
        try:
            print("[capture] Adding RSS feed...")
            page.wait_for_selector("#rssUrl", timeout=4000)
            page.fill("#rssUrl", "https://hnrss.org/frontpage")
            page.wait_for_selector("#rssAddBtn", timeout=4000)
            page.click("#rssAddBtn")
            page.wait_for_timeout(800)
            page.locator("#rssStatus").screenshot(path=str(out / "rss_added.png"))

            print("[capture] Listing RSS feeds...")
            page.wait_for_selector("#rssListBtn", timeout=4000)
            page.click("#rssListBtn")
            page.wait_for_timeout(800)
            page.locator("#rssStatus").screenshot(path=str(out / "rss_list.png"))

            print("[capture] Ingesting RSS feeds...")
            page.wait_for_selector("#rssIngestBtn", timeout=4000)
            page.click("#rssIngestBtn")
            page.wait_for_timeout(2000)
            page.locator("#rssStatus").screenshot(path=str(out / "rss_ingest.png"))
        except Exception as e:
            print("[capture] rss actions failed:", e)

        # 4) Web search ingestion (manual)
        try:
            print("[capture] Web search ingest...")
            page.wait_for_selector("#webSearchToggle", timeout=4000)
            page.click("#webSearchToggle")
            page.wait_for_selector("#message", timeout=4000)
            page.fill("#message", "ConscienceAI GitHub")
            page.wait_for_selector("#webSearchBtn", timeout=4000)
            page.click("#webSearchBtn")
            page.wait_for_timeout(2000)
            page.locator("#webStatus").screenshot(path=str(out / "web_search_ingest.png"))
        except Exception as e:
            print("[capture] web search failed:", e)

        # 5) Auto-index: enable + interval
        try:
            print("[capture] Auto-index apply...")
            page.wait_for_selector("#autoIndexToggle", timeout=4000)
            page.click("#autoIndexToggle")
            page.wait_for_selector("#autoInterval", timeout=4000)
            page.fill("#autoInterval", "15")
            page.wait_for_selector("#autoApplyBtn", timeout=4000)
            page.click("#autoApplyBtn")
            page.wait_for_timeout(1000)
            page.locator("#autoStatus").screenshot(path=str(out / "auto_index_on.png"))
        except Exception as e:
            print("[capture] auto index failed:", e)

        # 6) Chat with web search enabled
        try:
            print("[capture] Chat with web search...")
            page.wait_for_selector("#message", timeout=4000)
            page.fill("#message", "¿Qué es ConscienceAI?")
            page.wait_for_selector("#sendBtn", timeout=4000)
            page.click("#sendBtn")
            page.wait_for_timeout(3000)
            page.locator("#chat").screenshot(path=str(out / "chat_websearch.png"))
        except Exception as e:
            print("[capture] chat failed:", e)

        browser.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Capture Web UI screenshots")
    ap.add_argument("--url", default="http://127.0.0.1:5173/", help="Target URL of the web UI")
    ap.add_argument("--out", default="docs/screenshots", help="Output directory for screenshots")
    ap.add_argument("--width", type=int, default=1280, help="Viewport width")
    ap.add_argument("--height", type=int, default=900, help="Viewport height")
    args = ap.parse_args()
    main(args.url, args.out, viewport_width=args.width, viewport_height=args.height)
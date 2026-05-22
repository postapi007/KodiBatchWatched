# -*- coding: utf-8 -*-
import requests

def mark_episode_watched(kodi_url, tvshow_title, start_ep, end_ep):
    try:
        # 获取剧集ID
        payload = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetTVShows",
            "params": {"properties": ["title"]},
            "id": 1
        }
        response = requests.post(kodi_url, json=payload).json()
        shows = response.get("result", {}).get("tvshows", [])

        tvshowid = None
        for s in shows:
            if tvshow_title in s["title"]:
                tvshowid = s["tvshowid"]
                break

        if not tvshowid:
            print(f"❌ 未找到剧集: {tvshow_title}")
            return

        print(f"✅ 找到剧集ID: {tvshowid}")

        # 获取所有剧集
        payload = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetEpisodes",
            "params": {
                "tvshowid": tvshowid,
                "properties": ["season", "episode", "title"]
            },
            "id": 1
        }
        response = requests.post(kodi_url, json=payload).json()
        episodes = response.get("result", {}).get("episodes", [])

        count = 0
        for ep in episodes:
            if start_ep <= ep["episode"] <= end_ep:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "VideoLibrary.SetEpisodeDetails",
                    "params": {"episodeid": ep["episodeid"], "playcount": 1},
                    "id": 1
                }
                r = requests.post(kodi_url, json=payload)
                if r.status_code == 200:
                    print(f"✅ 已标记: 第{ep['episode']}集 - {ep['title']}")
                    count += 1
                else:
                    print(f"❌ 失败: 第{ep['episode']}集")

        print(f"\n完成，共标记 {count} 集。")

    except Exception as e:
        print(f"❌ 错误: {e}")

def main():
    print("=== Kodi 剧集已观看标记工具 ===")
    ip = input("请输入 Kodi IP（例如 192.168.xx.xxx:8080）: ").strip()
    tvshow = input("请输入剧集名称(支持模糊搜索): ").strip()

    try:
        start_ep = int(input("请输入开始集数: "))
        end_ep = int(input("请输入结束集数: "))
    except ValueError:
        print("❌ 开始集数和结束集数必须是数字")
        return

    if not ip or not tvshow:
        print("❌ 请填写完整信息")
        return

    kodi_url = f"http://{ip}/jsonrpc"
    print("开始执行...\n")
    mark_episode_watched(kodi_url, tvshow, start_ep, end_ep)

if __name__ == "__main__":
    main()

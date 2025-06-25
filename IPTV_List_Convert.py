#!/usr/bin/env python3
"""
IPTV CSV → M3U/TXT 转换脚本
---------------------------
• 读取 CSV 文件
• 同名频道合并多源
• 自动补全播放地址 / Logo 地址协议
• 支持本地 / 在线 logo 或同时生成
• 生成标准 M3U 播放列表
• 生成 TXT 源列表（分组 + 频道名 + 播放地址）
"""

from collections import OrderedDict, defaultdict
import pandas as pd

# ========= 配置 =========
CSV_PATH = 'IPTV_Channels.csv'
APPLY_ONLINE_LOGO = 2  # 0: 本地 logo, 1: 在线 logo, 2: 同时输出两份
OUTPUT_M3U = 'Zhejiang_Telecom_IPTV.m3u'
OUTPUT_M3U_ONLINE_LOGO = 'Zhejiang_Telecom_IPTV_ONLINE_LOGO.m3u'
OUTPUT_TXT = 'Zhejiang_Telecom_IPTV.txt'

UDPXY_ADDRESS = 'http://{{your_udpxy_address}}/udp/'
LOGO_ROOT_ADDRESS = 'http://{{your_logo_address}}/logo/'
# ========================


# ---------- 工具函数 ----------
def fix_url(url: str) -> str:
    url = str(url).strip()
    return url if '://' in url else UDPXY_ADDRESS + url


def fix_logo(logo: str, name: str, use_online: bool) -> str:
    if use_online:
        return f"https://epg.112114.xyz/logo/{name}.png"
    logo = str(logo).strip()
    return logo if '://' in logo else LOGO_ROOT_ADDRESS + logo.lstrip('/')


def load_and_prepare_df(path: str, use_online_logo: bool) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [col.strip().lstrip('\ufeff') for col in df.columns]
    df['播放地址'] = df['播放地址'].apply(fix_url)
    df['Logo链接'] = df.apply(lambda row: fix_logo(row['Logo链接'], row['频道名称'], use_online_logo), axis=1)
    df = df.sort_values(by='序号', kind='stable')
    return df


def build_channel_dict(df: pd.DataFrame) -> OrderedDict:
    channel_dict = OrderedDict()
    for _, row in df.iterrows():
        name = row['频道名称']
        if name not in channel_dict:
            channel_dict[name] = dict(
                logo=row['Logo链接'],
                group=row['频道分类'],
                urls=[row['播放地址']],
                序号=row['序号'],
            )
        else:
            channel_dict[name]['urls'].append(row['播放地址'])
    return OrderedDict(sorted(channel_dict.items(), key=lambda x: x[1]['序号']))


# ---------- 输出函数 ----------
def write_m3u(path: str, channels: OrderedDict) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for name, info in channels.items():
            f.write(
                f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" '
                f'tvg-logo="{info["logo"]}" group-title="{info["group"]}",{name}\n'
            )
            for url in info['urls']:
                f.write(f'{url}\n')


def write_txt(path: str, channels: OrderedDict) -> None:
    group_map = defaultdict(list)
    for name, info in channels.items():
        for url in info['urls']:
            group_map[info['group']].append((name, url))
    with open(path, 'w', encoding='utf-8') as f:
        for group, items in group_map.items():
            f.write(f"{group},#genre#\n")
            for name, url in items:
                f.write(f"{name},{url}\n")


# ---------- 主任务封装 ----------
def generate_output(use_online_logo: bool, output_m3u: str) -> OrderedDict:
    df = load_and_prepare_df(CSV_PATH, use_online_logo)
    channels = build_channel_dict(df)
    write_m3u(output_m3u, channels)
    return channels


# ---------- 主流程 ----------
def main():
    if APPLY_ONLINE_LOGO == 0:
        channels = generate_output(use_online_logo=False, output_m3u=OUTPUT_M3U)
        write_txt(OUTPUT_TXT, channels)
        print(f"生成本地 Logo 源：{OUTPUT_M3U}")
        print(f"TXT源输出：{OUTPUT_TXT}")
    elif APPLY_ONLINE_LOGO == 1:
        channels = generate_output(use_online_logo=True, output_m3u=OUTPUT_M3U_ONLINE_LOGO)
        write_txt(OUTPUT_TXT, channels)
        print(f"生成在线 Logo 源：{OUTPUT_M3U_ONLINE_LOGO}")
        print(f"TXT源输出：{OUTPUT_TXT}")
    elif APPLY_ONLINE_LOGO == 2:
        channels_local = generate_output(use_online_logo=False, output_m3u=OUTPUT_M3U)
        generate_output(use_online_logo=True, output_m3u=OUTPUT_M3U_ONLINE_LOGO)
        write_txt(OUTPUT_TXT, channels_local)
        print(f"本地源输出：{OUTPUT_M3U}")
        print(f"在线源输出：{OUTPUT_M3U_ONLINE_LOGO}")
        print(f"TXT源输出：{OUTPUT_TXT}")
    else:
        print("配置错误：APPLY_ONLINE_LOGO 只能为 0、1 或 2")



if __name__ == '__main__':
    main()

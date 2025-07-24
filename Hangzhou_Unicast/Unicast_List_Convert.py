#!/usr/bin/env python3
"""
IPTV CSV → M3U / TXT 转换器
---------------------------
• 支持本地 / 在线 / 同时输出 logo
• 自动填补 tvg-id、tvg-name、播放地址、logo 地址
• 输出标准 M3U 和 TXT 源文件
"""

import pandas as pd
from collections import defaultdict
from pathlib import Path

# ========= 配置项 =========
CSV_PATH = Path('Hangzhou_Telecom_Unicast.csv')
APPLY_ONLINE_LOGO = 2  # 0: 本地 logo, 1: 在线 logo, 2: 同时输出
OUTPUT_M3U = Path('Hangzhou_Telecom_Unicast.m3u')
OUTPUT_M3U_ONLINE_LOGO = Path('Hangzhou_Telecom_Unicast_ONLINE_LOGO.m3u')
OUTPUT_TXT = Path('Hangzhou_Telecom_Unicast.txt')

UDPXY_ADDRESS = 'http://{{your_udpxy_address}}/udp/'
LOGO_ROOT_ADDRESS = 'http://{{your_logo_address}}/Logo/'
# ==========================


def fix_url(url: str) -> str:
    """
    补全播放地址前缀（若无协议头）

    :param url: 原始播放地址
    :return: 修正后的播放地址
    """
    url = str(url).strip()
    return url if '://' in url else UDPXY_ADDRESS + url


def fix_logo(logo: str, use_online: bool) -> str:
    """
    补全 logo 地址（本地或在线）

    :param logo: 原始 logo 路径
    :param use_online: 是否使用在线 logo
    :return: 修正后的 logo 地址
    """
    if pd.isna(logo) or str(logo).strip() == "":
        return ""
    elif use_online:
        return f"https://myepg.org/Zhejiang_Telecom_IPTV/Logo/{logo}"
    logo = str(logo).strip()
    return logo if '://' in logo else LOGO_ROOT_ADDRESS + logo.lstrip('/')


def load_csv(path: Path, use_online_logo: bool) -> pd.DataFrame:
    """
    加载并清洗 CSV 数据

    :param path: CSV 文件路径
    :param use_online_logo: 是否使用在线 logo 地址
    :return: 标准化的 DataFrame
    """
    df = pd.read_csv(path)
    df.columns = [col.strip().lstrip('\ufeff') for col in df.columns]

    df['Tvg-id'] = df.get('Tvg-id', df['ChannelName'])
    df['Tvg-name'] = df.get('Tvg-name', df['ChannelName'])

    # df['ChannelURL_rtsp'] = df['ChannelURL_rtsp'].apply(fix_url)
    df['Logo'] = df.apply(lambda r: fix_logo(r['Logo'], use_online_logo), axis=1)
    return df


def write_m3u(path: Path, df: pd.DataFrame) -> None:
    """
    生成 M3U 文件

    :param path: 输出文件路径
    :param df: 已处理的频道表
    """
    with path.open('w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for _, row in df.iterrows():
            f.write(
                f'#EXTINF:-1 tvg-id="{row["Tvg-id"]}" tvg-name="{row["Tvg-name"]}" '
                f'tvg-logo="{row["Logo"]}" group-title="{row["ChannelGroup"]}",{row["ChannelName"]}\n'
            )
            f.write(f"{row['ChannelURL_rtsp']}\n")


def write_txt(path: Path, df: pd.DataFrame) -> None:
    """
    生成 TXT 源列表（分组）

    :param path: 输出文件路径
    :param df: 已处理的频道表
    """
    groups = defaultdict(list)
    for _, row in df.iterrows():
        # 判断 Tvg-name 是否为空或 NaN，用 ChannelName 替代
        name = row["Tvg-name"]
        if pd.isna(name) or str(name).strip() == "":
            name = row["ChannelName"]
        groups[row["ChannelGroup"]].append((name, row["ChannelURL_rtsp"]))

    with path.open('w', encoding='utf-8') as f:
        for group, items in groups.items():
            f.write(f"{group},#genre#\n")
            for name, url in items:
                f.write(f"{name},{url}\n")


def process(online_logo: bool, output_path: Path) -> pd.DataFrame:
    """
    加载、处理并写入 M3U 文件

    :param online_logo: 是否使用在线 logo
    :param output_path: M3U 输出路径
    :return: 用于 TXT 输出的 DataFrame（返回本地 logo 版本）
    """
    df = load_csv(CSV_PATH, use_online_logo=online_logo)
    write_m3u(output_path, df)
    return df


def main():
    """
    主函数，根据配置生成对应文件
    """
    if APPLY_ONLINE_LOGO == 0:
        df = process(False, OUTPUT_M3U)
        write_txt(OUTPUT_TXT, df)
        print(f"本地 Logo 源输出：{OUTPUT_M3U}")
        print(f"TXT 源输出：{OUTPUT_TXT}")
    elif APPLY_ONLINE_LOGO == 1:
        df = process(True, OUTPUT_M3U_ONLINE_LOGO)
        write_txt(OUTPUT_TXT, df)
        print(f"在线 Logo 源输出：{OUTPUT_M3U_ONLINE_LOGO}")
        print(f"TXT 源输出：{OUTPUT_TXT}")
    elif APPLY_ONLINE_LOGO == 2:
        df_local = process(False, OUTPUT_M3U)
        process(True, OUTPUT_M3U_ONLINE_LOGO)
        write_txt(OUTPUT_TXT, df_local)
        print(f"输出本地源：{OUTPUT_M3U}")
        print(f"输出在线源：{OUTPUT_M3U_ONLINE_LOGO}")
        print(f"TXT 源输出：{OUTPUT_TXT}")
    else:
        print("APPLY_ONLINE_LOGO 配置无效（应为 0、1、2）")


if __name__ == '__main__':
    main()

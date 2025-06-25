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
CSV_PATH = Path('IPTV_Channels.csv')
APPLY_ONLINE_LOGO = 2  # 0: 本地 logo, 1: 在线 logo, 2: 同时输出
OUTPUT_M3U = Path('Zhejiang_Telecom_IPTV.m3u')
OUTPUT_M3U_ONLINE_LOGO = Path('Zhejiang_Telecom_IPTV_ONLINE_LOGO.m3u')
OUTPUT_TXT = Path('Zhejiang_Telecom_IPTV.txt')

UDPXY_ADDRESS = 'http://{{your_udpxy_address}}/udp/'
LOGO_ROOT_ADDRESS = 'http://{{your_logo_address}}/logo/'
# ==========================


def fix_url(url: str) -> str:
    """
    补全播放地址前缀（若无协议头）

    :param url: 原始播放地址
    :return: 修正后的播放地址
    """
    url = str(url).strip()
    return url if '://' in url else UDPXY_ADDRESS + url


def fix_logo(logo: str, tvg_name: str, use_online: bool) -> str:
    """
    补全 logo 地址（本地或在线）

    :param logo: 原始 logo 路径
    :param tvg_name: 频道名（用于在线 logo）
    :param use_online: 是否使用在线 logo
    :return: 修正后的 logo 地址
    """
    if use_online:
        return f"https://epg.112114.xyz/logo/{tvg_name}.png"
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

    df['tvg-id'] = df.get('tvg-id', df['频道名称'])
    df['tvg-name'] = df.get('tvg-name', df['频道名称'])

    df['播放地址'] = df['播放地址'].apply(fix_url)
    df['Logo链接'] = df.apply(lambda r: fix_logo(r['Logo链接'], r['tvg-name'], use_online_logo), axis=1)
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
                f'#EXTINF:-1 tvg-id="{row["tvg-id"]}" tvg-name="{row["tvg-name"]}" '
                f'tvg-logo="{row["Logo链接"]}" group-title="{row["频道分类"]}",{row["频道名称"]}\n'
            )
            f.write(f"{row['播放地址']}\n")


def write_txt(path: Path, df: pd.DataFrame) -> None:
    """
    生成 TXT 源列表（分组）

    :param path: 输出文件路径
    :param df: 已处理的频道表
    """
    groups = defaultdict(list)
    for _, row in df.iterrows():
        groups[row["频道分类"]].append((row["tvg-name"], row["播放地址"]))

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

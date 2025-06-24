#!/usr/bin/env python3
"""
IPTV CSV → M3U 转换脚本
-----------------------
• 读取 CSV 文件
• 同名频道合并多源
• 自动补全播放地址/Logo 地址协议
• 生成标准 M3U 列表
"""

from collections import OrderedDict
import pandas as pd

# ========= 配置 =========
CSV_PATH = 'IPTV_Channels.csv'             # CSV 文件路径
OUTPUT_M3U = 'Zhejiang_Telecom_IPTV.m3u'               # 输出文件
UDPXY_ADDRESS = 'http://{{your_udpxy_address}}/udp/'    # 播放地址前缀
LOGO_ROOT_ADDRESS = 'http://{{your_logo_address}}/logo/'  # Logo 地址前缀
# ========================


# ---------- 工具函数 ----------
def fix_url(url: str) -> str:
    """若播放地址无协议头则补上 UDPXY_ADDRESS"""
    url = str(url).strip()
    return url if '://' in url else UDPXY_ADDRESS + url


def fix_logo(logo: str) -> str:
    """若 Logo 链接无协议头则补上 LOGO_ROOT_ADDRESS"""
    logo = str(logo).strip()
    return logo if '://' in logo else LOGO_ROOT_ADDRESS + logo.lstrip('/')


def read_csv(path: str, sort_key='序号') -> pd.DataFrame:
    """读取 CSV → 补全地址 → 按序号排序"""
    df = pd.read_csv(path)
    df['播放地址'] = df['播放地址'].apply(fix_url)
    df['Logo链接'] = df['Logo链接'].apply(fix_logo)
    df = df.sort_values(by=sort_key, kind='stable')
    return df


def build_channel_dict(df: pd.DataFrame) -> OrderedDict:
    """把同名频道合并成有序字典"""
    channel_dict = OrderedDict()
    for _, row in df.iterrows():
        name = row['频道名']
        if name not in channel_dict:
            channel_dict[name] = dict(
                logo=row['Logo链接'],
                group=row['分组'],
                urls=[row['播放地址']],
                序号=row['序号'],
            )
        else:
            channel_dict[name]['urls'].append(row['播放地址'])
    return OrderedDict(sorted(channel_dict.items(), key=lambda x: x[1]['序号']))


def write_m3u(file_path: str, channels: OrderedDict) -> None:
    """写出 M3U 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for name, info in channels.items():
            f.write(
                f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" '
                f'tvg-logo="{info["logo"]}" group-title="{info["group"]}",{name}\n'
            )
            for url in info['urls']:
                f.write(f'{url}\n')


# ---------- 主流程 ----------
def main() -> None:
    """读取 CSV → 合并频道 → 输出 M3U"""
    df = read_csv(CSV_PATH)
    channels = build_channel_dict(df)
    write_m3u(OUTPUT_M3U, channels)
    print(f"M3U 文件生成成功：{OUTPUT_M3U}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
IPTV CSV → M3U/M3U8/TXT 转换脚本
--------------------------------
• 读取 CSV 文件
• 同名频道合并多源
• 自动补全播放地址 / Logo 地址协议
• 生成标准 M3U（同时保存 .m3u 与 .m3u8）
• 生成 TXT 源列表
"""

from collections import OrderedDict
import pandas as pd

# ========= 配置 =========
CSV_PATH = 'IPTV_Channels.csv'                         # CSV组播源列表
APPLY_ONLINE_LOGO = True                               # True使用在线logo，False使用列表中的logo
OUTPUT_M3U = 'Zhejiang_Telecom_IPTV.m3u'               # 输出 .m3u
OUTPUT_M3U8 = 'Zhejiang_Telecom_IPTV.m3u8'             # 输出 .m3u8（内容同上）
OUTPUT_TXT = 'Zhejiang_Telecom_IPTV.txt'               # 输出 .txt
UDPXY_ADDRESS = 'http://{{your_udpxy_address}}/udp/'   # 播放地址前缀
LOGO_ROOT_ADDRESS = 'http://{{your_logo_address}}/logo/'  # Logo 地址前缀
# ========================


# ---------- 工具函数 ----------
def fix_url(url: str) -> str:
    """若播放地址无协议头则补上 UDPXY_ADDRESS"""
    url = str(url).strip()
    return url if '://' in url else UDPXY_ADDRESS + url


def fix_logo(logo: str, name: str) -> str:
    """
    根据配置决定 Logo 链接来源：
    - APPLY_ONLINE_LOGO=True：使用线上 Logo 地址（根据频道名）
    - 否则：若无协议则补上 LOGO_ROOT_ADDRESS
    """
    if APPLY_ONLINE_LOGO:
        return f"https://epg.112114.xyz/logo/{name}.png"
    logo = str(logo).strip()
    return logo if '://' in logo else LOGO_ROOT_ADDRESS + logo.lstrip('/')

def read_csv(path: str, sort_key='序号') -> pd.DataFrame:
    """读取 CSV → 补全地址 → 按序号排序"""
    df = pd.read_csv(path)
    df['播放地址'] = df['播放地址'].apply(fix_url)
    df['Logo链接'] = df.apply(lambda row: fix_logo(row['Logo链接'], row['频道名称']), axis=1)
    df = df.sort_values(by=sort_key, kind='stable')
    return df


def build_channel_dict(df: pd.DataFrame) -> OrderedDict:
    """把同名频道合并成有序字典"""
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
    # 保持原始排序
    return OrderedDict(sorted(channel_dict.items(), key=lambda x: x[1]['序号']))


def write_m3u(file_path: str, channels: OrderedDict) -> None:
    """写出标准 M3U 文件（内容通用，可写到 .m3u 或 .m3u8）"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for name, info in channels.items():
            f.write(
                f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" '
                f'tvg-logo="{info["logo"]}" group-title="{info["group"]}",{name}\n'
            )
            for url in info['urls']:
                f.write(f'{url}\n')


def write_txt(file_path: str, channels: OrderedDict) -> None:
    """写出 TXT 格式：分组,#genre# + 频道名,地址"""
    from collections import defaultdict

    # group -> [(name, url), ...]
    group_map = defaultdict(list)
    for name, info in channels.items():
        group = info['group']
        for url in info['urls']:
            group_map[group].append((name, url))

    with open(file_path, 'w', encoding='utf-8') as f:
        for group, items in group_map.items():
            f.write(f"{group},#genre#\n")
            for name, url in items:
                f.write(f"{name},{url}\n")


def main() -> None:
    df = read_csv(CSV_PATH)
    channels = build_channel_dict(df)

    # 同内容写两份：.m3u 和 .m3u8
    write_m3u(OUTPUT_M3U, channels)
    write_m3u(OUTPUT_M3U8, channels)

    # 写 TXT
    write_txt(OUTPUT_TXT, channels)

    print(f"已生成：{OUTPUT_M3U}")
    print(f"已生成：{OUTPUT_M3U8}")
    print(f"已生成：{OUTPUT_TXT}")


if __name__ == '__main__':
    main()

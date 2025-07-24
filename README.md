<h1 style="text-align: center;" align="center">
浙江电信IPTV组播源 & 杭州单播源 & EPG分发
</h1>

<h3 style="text-align: center;" align="center">
🆓免费提供 ✅简单易用 ⏰高频更新 🔍自动检测 📥多格式输出 🧩自定义订阅 🔁提供EPG镜像
</h3>

<div style="text-align: center;" align="center">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/FHZDCJ/Zhejiang_Telecom_IPTV?style=flat">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/FHZDCJ/Zhejiang_Telecom_IPTV?style=flat">
<img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/FHZDCJ/Zhejiang_Telecom_IPTV">
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/FHZDCJ/Zhejiang_Telecom_IPTV">
<img alt="Number of channels" src="https://myepg.org/Zhejiang_Telecom_IPTV/number.php">
</div>

---

## 目录

- [项目简介](#项目简介)
- [频道分辨率及有效性报告](#频道分辨率及有效性报告)
- [节目源收录说明](#节目源收录说明)
- [项目文件说明](#项目文件说明)
- [EPG镜像](#epg镜像)
- [使用方法](#使用方法)
    - [订阅链接形式使用](#订阅链接形式使用)
    - [在线生成并下载节目源文件](#在线生成并下载节目源文件)
    - [使用本地台标](#使用本地台标)
    - [使用在线台标](#使用在线台标)
    - [使用txt文件](#使用txt文件)
    - [自定义使用](#自定义使用)
- [免责声明 / Disclaimer](#免责声明--disclaimer)

---

## 项目简介

本项目收录浙江电信IPTV的组播源及单播源地址，提供`.m3u`、`.txt`格式的直播源，`.csv`格式的列表，提供台标，提供自定义订阅链接接口，提供在线替换变量功能，适配[112114 EPG](https://epg.112114.xyz)节目单。

本项目具有两个同步镜像，两个仓库的数据保持一致：
[GitHub](https://github.com/FHZDCJ/Zhejiang_Telecom_IPTV)  [Gitee](https://gitee.com/FHZDCJ/Zhejiang_Telecom_IPTV)

> ⚠️特别提示：本项目**不是公网直播源，组播、单播地址在公网不可访问**。如你需要测试组播地址，必须先订购浙江电信IPTV服务，并通过IPoE认证后使用UDPXY在局域网内转发才能使用。

## 频道分辨率及有效性报告

本项目每天自动对现有频道列表进行频道分辨率及有效性检测，并提供检测报告，你可以点击以下链接查阅。

[浙江组播源检测报告](https://myepg.org/Zhejiang_Telecom_IPTV/report.html)
[浙江杭州单播源检测报告](https://myepg.org/Zhejiang_Hangzhou_Telecom_IPTV/report.html)

## 组播节目源收录说明

1. 具有1080P或以上清晰度的节目，不收录1080P以下的节目源；
2. 同时具有1080P及1080P以上清晰度的节目源同时收录，4K节目源单独收录至“4K超高清”分组中；
3. 同一节目在清晰度相同的情况下具有多个节目源的，收录1个肉眼观看效果更清晰的节目源；
4. 同一节目同一清晰度具有多个节目源，且肉眼观察清晰度相同，只收录1个；
5. 重复播放没有具体意义视频的直播源，不收录。


## 项目文件说明

#### 本项目提供浙江组播、杭州单播、杭州单组播复合的多种格式的频道源文件，适配不同播放器和使用场景

#### 浙江组播(/Zhejiang_Multicast)：

*解释：浙江组播提供的是纯组播源，如果某一频道单播源对应的组播源发生变更，本组播源也会自动同步。*

- `Zhejiang_Telecom_IPTV.m3u`：使用本地台标的m3u模板，适合局域网内自建http服务器使用。
- `Zhejiang_Telecom_IPTV_ONLINE_LOGO.m3u`：使用本项目在线台标的m3u源。
- `Zhejiang_Telecom_IPTV.txt`：txt格式频道源。
- `IPTV_Channels.csv`：频道清单。
- `IPTV_List_Convert.py`：用于将`.csv`转换为`.m3u`和`txt`格式的转换脚本，支持自定义参数。

所有`.m3u`和`.txt`文件中的`{{your_udpxy_address}}`和`{{your_logo_address}}`占位符需根据你的实际网络环境替换为对应的地址。

#### 杭州单播(/Hangzhou_Unicast)：

*解释：杭州单播提供的是完整的纯单播源，仅适用于杭州，本源每日自动同步更新，并自动分组、更名、排序。*

- `Hangzhou_Telecom_Unicast.m3u`：使用本地台标的m3u模板，适合局域网内自建http服务器使用。
- `Hangzhou_Telecom_Unicast_ONLINE_LOGO.m3u`：使用本项目在线台标的m3u源。
- `Hangzhou_Telecom_Unicast.txt`：纯文本格式频道源。
- `Hangzhou_Telecom_Unicast.csv`：频道清单。
- `Unicast_List_Convert.py`：用于将`.csv`转换为`.m3u`和`txt`格式的转换脚本，支持自定义参数。

#### 杭州组单播复合(/Hangzhou_Multicast_Unicast)：

*解释：杭州组单播复合是为了查漏补缺，仅适用于杭州，由于部分单播源没有高清版本，因此本源在组播源基础上，对有单播源的频道自动改为单播源，每日自动同步更新。*

- `Hangzhou_Multicast_Unicast.m3u`：使用本地台标的m3u模板，适合局域网内自建http服务器使用。
- `Hangzhou_Multicast_Unicast_ONLINE_LOGO.m3u`：使用本项目在线台标的m3u源。
- `Hangzhou_Multicast_Unicast.txt`：纯文本格式频道源。
- `Hangzhou_Multicast_Unicast.csv`：频道清单。
- `Unicast_Multicast_List_Convert.py`：用于将`.csv`转换为`.m3u`和`txt`格式的转换脚本，支持自定义参数。

所有`.m3u`和`.txt`文件中的`{{your_udpxy_address}}`和`{{your_logo_address}}`占位符需根据你的实际网络环境替换为对应的地址。

## EPG镜像

本项目现在提供[112114 EPG](https://epg.112114.xyz/)镜像，镜像地址如下：

- [https://myepg.org/EPG/112114/pp.xml](https://myepg.org/EPG/112114/pp.xml)
- [https://myepg.org/EPG/112114/pp.xml.gz](https://myepg.org/EPG/112114/pp.xml.gz)

## 使用方法

### 订阅链接形式使用

你可以在直播软件订阅以下链接，获取带有自定义 UDPXY 地址的 IPTV 播放列表文件：

- `https://myepg.org/Zhejiang_Telecom_IPTV/Subscribe/?ip=你的IP:端口&type=文件类型`
- `https://myepg.org/Zhejiang_Telecom_IPTV/Subscribe/?ip=你的IP:端口&logo=你的IP或域名:端口`

#### 参数说明：

|    参数名    | 示例值                                                   | 是否必须 | 说明                                                                    |
|:---------:|-------------------------------------------------------|:----:|-----------------------------------------------------------------------|
|   `ip`    | `10.30.0.1:2340`                                      |  否   | 你的 UDPXY 地址（含端口），格式严格为 IPv4:端口，本参数仅在`source`值为`unicast`时无需提供。         |
|  `type`   | `m3u` 或 `txt`                                         |  否   | 指定输出文件类型，默认为 `m3u`。                                                   |
|  `logo`   | `logo.example.com` 或 `192.168.1.2:8080`               |  否   | 仅允许在 `type=m3u` 时使用，替换模板中 `{{your_logo_address}}` 占位符。支持域名或IPv4，可带端口。 |
| `source`  | `multicast`（纯组播源）、`unicast`（杭州纯单播源）、`merged`（杭州组单播复合源） |  否   | 默认为`multicast`（组播源）。                                                  
| `nocache` | -                                                     |  否   | 指示拒绝使用缓存，无需填写参数值                                                      |
---

系统会自动将模板中的 `{{your_udpxy_address}}` 替换为你提供的 IP 和端口；如果传入了 `logo` 参数且 `type=m3u`，还会替换 `{{your_logo_address}}`，返回可直接使用的 IPTV 文件。

所有参数均经过严格格式校验，确保 IP、端口及域名合法。  
错误时会返回 JSON 格式的错误信息，包含 `code` 和 `message` 字段，便于调试。

---

示例请求：

- `https://myepg.org/Zhejiang_Telecom_IPTV/Subscribe/?ip=192.168.1.1:2345`
使用在线台标的m3u源
- `https://myepg.org/Zhejiang_Telecom_IPTV/Subscribe/?ip=192.168.1.1:2345&type=txt`
txt源
- `https://myepg.org/Zhejiang_Telecom_IPTV/Subscribe/?ip=192.168.1.1:2345&logo=192.168.1.1:8090`
使用自定义台标的m3u源
- `https://myepg.org/Zhejiang_Telecom_IPTV/Subscribe/?ip=192.168.1.1:2345&nocache`
使用在线台标的m3u源，并且拒绝使用缓存

#### 请求限制
本功能需要消耗服务器资源，你的请求会受到限制：
- 每秒钟1次
- 每分钟5次
- 每小时20次
- 每24小时30次

为节约服务器资源，本接口有数据缓存，即使源已更新，对于相同的URL请求在一定时间内可能会得到相同的缓存数据，在此情形下不会记入请求次数中。如您需要获取最新数据，可以自行添加nocache参数。

超过请求次数限制后，您将不能获取数据，请设置合理的订阅周期。

### 在线生成并下载节目源文件

本项目已经提供在线生成功能，无需手动替换变量，请点击[在线生成并下载](https://myepg.org/Zhejiang_Telecom_IPTV/OnlineGen.html)前往。  
在线生成支持使用在线台标或本地台标的`.m3u`格式，也支持生成`.txt`格式，请按照网页提示操作。

### 使用本地台标

您可直接下载项目中提供的后缀为 `.m3u` 的文件，
并根据实际环境进行如下替换：

- `{{your_logo_address}}`：替换为您 Logo 存放的 URL 地址，例如 `10.30.0.1:8080`；  
- `{{your_udpxy_address}}`：替换为局域网内的 `udpxy` 代理地址及端口号，例如 `10.30.0.1:4022`。

完成替换后，可将 `.m3u` 文件导入受支持的直播源播放器中进行播放。

### 使用在线台标

如您需要使用在线台标，可直接下载项目中提供的后缀为 `_ONLINE_LOGO.m3u` 的文件，  
并根据实际环境进行如下替换：

- `{{your_udpxy_address}}`：替换为局域网内的 `udpxy` 代理地址及端口号，例如 `10.30.0.1:4022`。

完成替换后，可将 `.m3u` 文件导入受支持的直播源播放器中进行播放。

### 使用.txt文件

如您需要使用txt格式直播源，可直接下载项目中提供的后缀为 `.txt` 的文件，  
并根据实际环境进行如下替换：

- `{{your_udpxy_address}}`：替换为局域网内的 `udpxy` 代理地址及端口号，例如 `10.30.0.1:4022`。

完成替换后，可将 `.txt` 文件导入受支持的直播源播放器中进行播放。

### 自定义使用

如需对频道信息进行个性化编辑，可修改后缀为 `.csv` 的文件内容，  
然后使用本项目提供的后缀为 `_Convert.py`的脚本 将 CSV 文件转换为 `.m3u` 文件。  
请确保已安装脚本所需依赖后再运行转换操作。

---

# ⚠️免责声明 / Disclaimer

## 1. 本项目仅供学习与研究用途
本项目中使用的地址来源于中国电信 IPTV 网络，仅用于技术学习与研究测试，禁止用于任何商业行为、违反电信用户协议以及违反法律法规的用途。作者不对使用者的任何行为或后果承担责任，请自觉遵守相关法律法规。

## 2. IPTV认证提示
本项目中的 IPTV 地址**仅能且必须在经过电信运营商提供的 IPoE（IP over Ethernet）认证网络中访问**，在公网、家庭宽带或未授权网络中均无法播放。本项目**不提供任何破解、模拟或绕过认证的工具或方法**，禁止使用本项目内容进行非法接入。

## 3. 内容版权说明
项目中提及或内嵌的频道名称、台标（Logo）、节目内容等，版权归属原版权方与电信运营商所有。项目仅用于组播地址格式演示与技术分析，**未包含任何节目内容或流媒体数据**。请勿将其用于任何侵犯版权的用途。

项目中提供的EPG分发仅为对应免费EPG服务未经任何改动的镜像文件，本项目作者不享有该EPG镜像文件的任何权利，其中的内容不代表本项目作者的观点，本项目作者亦不对此分发承担任何责任，使用前请自行甄别。

## 4. udpxy安全使用提示
如你在本地搭建了 `udpxy` 代理服务，**请勿将其端口暴露在公网环境中**。`udpxy` 并无身份认证机制，若开放在公网，可能导致非法访问、资源泄漏或安全隐患，并可能违反电信用户协议或侵犯版权方与电信运营商的合法权益。您必须限制访问来源或仅绑定内网地址。

## 5. 责任免除声明
本项目作者不持有任何 IPTV 内容的版权，也不对任何使用本项目所引发的问题（包括但不限于账号封禁、网络封锁、法律责任）承担责任。
**使用者对于本项目采取的任何形式的使用（包含但不限于拷贝、分发）必须自行承担一切风险和后果。**

## 6. 内容准确性提示
本项目内提供的任何内容均为对于互联网资料的人工整理，不能确保其准确性，在进行任何形式的使用之前，请自行确保准确性。

---

> ⚠️ 请合理合法使用本项目内容，禁止用于任何违反当地法律或运营商规定的行为。

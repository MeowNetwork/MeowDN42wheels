# MeowDN42wheels

Some tools for MiaoTony's DN42 Network, aka MeowNet / MeowNetwork

***喵喵又在造轮子啦！***

# DN42 Free ASN Finder

`find_free_ASN.py` 用于查询空闲未被使用的 ASN，你可以自己改代码挑选你喜欢的编号。

你需要先 clone https://git.dn42.dev/dn42/registry 然后列出 `data/aut-num/` 文件夹下的文件到 `aut-num.txt`

```bash
git clone git@git.dn42.dev:<FOO>/registry.git
# Where <FOO> is your gitea username.
ls -1 registry/data/aut-num/ > aut-num.txt
python3 find_free_ASN.py
```


# DN42 Peer Configurator

`peer_configurator.py` 是一个自动化脚本，用于在 DN42 网络中快速配置和建立对等连接（peer）。

只用输入对方的连接信息，该脚本就会生成必要的 WireGuard VPN 和 BIRD 路由配置文件，而后自动完成配置，并展示新建立的连接情况，从而大大简化了整个 peer 过程，同时降低了手工配置而引入的出错风险。

An automated script used to quickly configure and establish peer-to-peer connections in a DN42 network.

This script will generate the necessary WireGuard VPN and BIRD routing configurations and complete them, greatly simplifying the entire peer process and reducing the risk of errors introduced by manual configuration.

## 环境要求 / Environmental requirements 
- Linux
- WireGuard & BIRD (with systemd) 
- Python (Python 3.6 or higher is recommended), no additional dependencies need to be installed 

## 使用步骤 / Steps
### Step1: 下载脚本 Download the script
首先，将 `peer_configurator.py` 脚本下载到您的服务器上。您可以使用喜欢的方式来下载。

```bash
wget https://github.com/MeowNetwork/MeowDN42wheels/raw/master/peer_configurator.py
# OR
# curl -LO https://github.com/MeowNetwork/MeowDN42wheels/raw/master/peer_configurator.py
```

或者

```bash
git clone https://github.com/MeowNetwork/MeowDN42wheels.git
cd MeowDN42wheels
```

### Step2: 修改您的配置信息后运行脚本 Modify your information and run the script

把自己的信息配置好，下面依次是自己的 WireGuard 私钥、DN42 IPv4、DN42 IPv6、link-local IPv6   
*（假设 `xxxxxxxxxxxxxxxxxxxxx`、`172.23.45.67`、`fd00:dead:beaf::1234`、`fe80::1234` 是你的）*

Configure your own information, below are your WireGuard private key, DN42 IPv4, DN42 IPv6, and link local IPv6 in order.      
*(Assuming `xxxxxxxxxxxxxxxxxxxxx`, `172.23.45.67`, `fd00:dead:beaf::1234`, `fe80::1234` are yours)*

```bash
sed -i -e 's#REPLACE_PRIVATEKEY_HERE#xxxxxxxxxxxxxxxxxxxxx#g' -e 's#REPLACE_DN42IPV4_HERE#172.23.45.67#g' -e 's#REPLACE_DN42IPV6_HERE#fd00:dead:beaf::1234#g' -e 's#REPLACE_LINKLOCALIPV6_HERE#fe80::1234#g' peer_configurator.py
```

在执行脚本之前，请确保您具有 root 执行权限。   
Ensure that you have root privileges.  

```bash
sudo python3 peer_configurator.py
```

### Step 3: 输入配置信息 Enter configuration information 

首先配置对方联系信息：    
Configure your peer's contact information:   

- **ASNumber**: 对方的 DN42 自治系统号（AS号），可以直接输入 `424242xxxx` 或者 `AS424242xxxx`   
    Your peer's DN42 autonomous system number (AS number), e.g. `424242xxxx`, `AS424242xxxx`
- **MNT**: 对方的维护者标识   
    Your peer's maintainer 
- **Website/Contact**: *（可选）* 对方的联系信息（网站/电子邮件/Telegram/etc.），便于出问题时联系对方   
     *(Optional)* Contact information of your peer (website/email/Telegram/etc.), to facilitate contacting the peer in case of problems 

接下来是具体的 IP 配置部分：

- **IPv4 Configuration**: 询问是否需要 DN42 IPv4 配置。如果需要，请输入 `y`，并根据后续提示输入 IPv4 地址，否则 `n`。如果支持 Extended Next Hop（需要 BIRD 2.0.8+ 且手动开启），那么可以输入 `n` 省略此项配置。   
    Ask if DN42 IPv4 configuration is needed. If so, enter `y` and follow prompts to input the IPv4 address. If it supports Extended Next Hop (requires BIRD 2.0.8+ and manual activation), you can just enter `n` to omit this configuration.  
    - **DN42_IPv4**: 仅当需要 IPv4 时输入。输入对方的 DN42 IPv4 地址，这将附加在新建立的 WireGuard 网卡上。    
        Enter only if IPv4 is needed. Input your peer's DN42 IPv4 address, which will be attached to the newly established WireGuard device.  
- **Split IPv4 and IPv6 session**: 询问是否需要将 IPv4 和 IPv6 会话分开。如果需要，请输入 `y`，将为 v4 和 v6 分别建立单独的会话，且在路由传递禁用另一协议，不需要请输入 `n`   
    Ask if IPv4 and IPv6 sessions should be split. Enter `y` if required, then separate sessions will be established for v4 and v6 respectively, and the other protocol will be disabled during routing delivery.
- **DN42_IPv6/link-local**：对方的 DN42 IPv6 或本地链路地址   
    Input your peer's DN42 IPv6 or link-local address.

一般而言，MeowNetwork (AS4242422688) 及很多其他的 DN42 网络通常与对方使用 link-local IPv6 地址来建立 Multiprotocol-BGP ([RFC 5549](https://www.rfc-editor.org/info/rfc5549)) v4+v6 channels（只需要建立一个 IPv6 会话），并开启 Extended Next Hop，则上面 **输入两次 `n` 后使用形如 `fe80::<对方ASN后4位>` 的地址来建立 peer 即可**

Generally, MeowNetwork (AS4242422688) and many other DN42 networks typically use link-local IPv6 addresses to establish Multiprotocol-BGP ([RFC 5549](https://www.rfc-editor.org/info/rfc5549)) v4+v6 channels with the peer (just need to establish an IPv6 session) and enable Extended Next Hop. To establish a peer, just enter `n` twice and use an address similar to `fe80::<the last 4 bits of the peer's ASN>`.

接下来是 **WireGuard 配置**：

- **PublicKey**: 输入对方的 WireGuard 公钥    
    your peer's WireGuard public key
- **Endpoint**: 对方的地址，可以是域名或者公网 IP 地址    
    Your peer's hostname or public IP address
- **ListenPort**: 对方 WireGuard 监听的端口号   
    the port number on which your peer's WireGuard listens

如果对端未提供公网地址，将 `Endpoint` 和 `ListenPort` 留空即可。   
If your peer does not provide a public address, just leave `Endpoint` and `ListenPort` blank. 

请注意，本脚本将使用 `20000 + 对方ASN后4位` 作为本机 WireGuard 监听的端口号  
Please note that this script will use `20000 + the last 4 digits of your peer's ASN` as the port for local WireGuard listening. 


### Step4: 确认配置文件并完成配置 Confirmation 
脚本会显示生成的 WireGuard 和 BIRD 配置信息预览。请仔细检查这些信息是否正确。

确认（输入`y`）后脚本将自动写入并执行配置，其中已配置开机自启

请确保使用 systemd 管理 WireGuard 及 BIRD daemon，否则可能配置失败，您可以手动完成最后的启动流程

Preview of the generated WireGuard and BIRD configuration information will be displayed. Please carefully check if this information is correct.

After confirmation (input `y`), the script will automatically write and execute the configuration, where the startup self start has been configured. 

Please ensure to use Systemd to manage WireGuard and BIRD daemons, otherwise configuration may fail. You can manually complete the final startup process.

脚本将自动展示新建立的 peer 的 WireGuard 及 BIRD 连接情况

The WireGuard and BIRD connection status of the newly established peer will be displayed.


## Sponsorship

非常高兴能帮到你，欢迎点个 star，也可以 [给喵喵投喂](https://miaotony.xyz/about/#Sponsorship)！ *（仰望.jpg*

*[Buy me a cup of coffee~](https://miaotony.xyz/about/#Sponsorship)*



## Copyright

**本项目仅供学习研究使用，请在合理合法范围内使用！**  
**The relevant technical content of this project is only for study and research, please use within the reasonable and legal scope!**  

License:  
[MIT License](LICENSE)  

最终解释权归本项目开发者所有。  
The final interpretation right belongs to the developer of the project.  

Copyright © 2023-2024 [MiaoTony](https://github.com/miaotony).  
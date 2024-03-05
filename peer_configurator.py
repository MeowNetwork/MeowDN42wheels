#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DN42 peer configurator
DN42 对等连接配置助手
自动生成 DN42 peer 所需的 WireGuard & BIRD 配置文件并执行

@Author: MiaoTony
"""

import os
import time
import sys

ASN = input('ASNumber: ').strip().replace('AS', '').replace('as', '')
MNT = input('MNT: ').strip()
CONTACT = input('Website/Contact: ').strip()
DATE = time.strftime("%Y%m%d", time.localtime())

is_split_v4v6_session = False
is_IPv4_needed = input("Need IPv4 (y/n): ").strip()
if is_IPv4_needed == 'y' or is_IPv4_needed == 'Y':
    is_IPv4_needed = True
    is_split_v4v6_session = input("Split IPv4 and IPv6 session (y/n): ").strip()
    if is_split_v4v6_session == 'y' or is_split_v4v6_session == 'Y':
        is_split_v4v6_session = True
    else:
        is_split_v4v6_session = False
    DN42V4 = input('DN42_IPv4: ').strip().split('/')[0]  # remove subnet mask
else:
    is_IPv4_needed = False
DN42V6 = input('DN42_IPv6/link-local: ').strip().split('/')[0]  # remove subnet mask
print()

print("""====== WireGuard Config =====
Leave `Endpoint` and `ListenPort` blank if the remote side does not provide a public network address.""")
PublicKey = input('PublicKey: ').strip()
Endpoint = input('Endpoint: ').strip()
ListenPort = input('ListenPort: ').strip()

wg_config = f"""
# /etc/wireguard/wg_{ASN}.conf
# DN42 AS{ASN}
# {MNT}
# {CONTACT}
# {DATE}

[Interface]
PrivateKey = REPLACE_PRIVATEKEY_HERE
ListenPort = 2{ASN[-4:]}
""".strip()

if is_IPv4_needed:
    wg_config += f"""
PostUp = ip addr add REPLACE_DN42IPV4_HERE/32 peer {DN42V4}/32 dev %i"""

if DN42V6.startswith('fe80'):
    # link-local
    wg_config += f"""
PostUp = ip addr add REPLACE_LINKLOCALIPV6_HERE/64 dev %i"""
else:
    wg_config += f"""
PostUp = ip addr add REPLACE_DN42IPV6_HERE/128 peer {DN42V6}/128 dev %i"""

wg_config += f"""
Table = off

[Peer]
PublicKey = {PublicKey}"""
if Endpoint and ListenPort:
    wg_config += f"""
Endpoint = {Endpoint}:{ListenPort}"""
wg_config +="""
AllowedIPs = 10.0.0.0/8, 172.20.0.0/14, 172.31.0.0/16, fd00::/8, fe80::/64
"""


if is_split_v4v6_session:
    bird_config = f"""
# /etc/bird/peers/AS{ASN}.conf
# DN42 AS{ASN}
# {MNT}
# {CONTACT}
# {DATE}

protocol bgp dn42_{ASN}_v6 from dnpeers {{
    neighbor {DN42V6} % 'wg_{ASN}' as {ASN};
    direct;
    ipv4 {{
        import none;
        export none;
    }};
}}

protocol bgp dn42_{ASN}_v4 from dnpeers {{
    neighbor {DN42V4} % 'wg_{ASN}' as {ASN};
    direct;
    ipv6 {{
        import none;
        export none;
    }};
}}
""".strip()
else:
    bird_config = f"""
# /etc/bird/peers/AS{ASN}.conf
# DN42 AS{ASN}
# {MNT}
# {CONTACT}
# {DATE}

protocol bgp dn42_{ASN}_v6 from dnpeers {{
    neighbor {DN42V6} % 'wg_{ASN}' as {ASN};
    direct;
}}
""".strip()


print("\n####### WireGuard Info #######\n")
print(wg_config)

print("\n####### BIRD Info #######\n")
print(bird_config)
print()

while True:
    choice = input("##### Is everything OK (y/n): ").strip()
    if choice == 'y' or choice == 'Y':
        break
    elif choice == 'n' or choice == 'N':
        sys.exit(1)

print("\n##### Write WireGuard config...")
with open(f"/etc/wireguard/wg_{ASN}.conf", 'w', encoding='utf-8') as f_wg:
    f_wg.write(wg_config)

print("\n##### Write BIRD config...")
with open(f"/etc/bird/peers/AS{ASN}.conf", 'w', encoding='utf-8') as f_bird:
    f_bird.write(bird_config)

print("\n##### Write OK! #####")

print("\n##### Generate WireGuard connection...")
os.system(f"systemctl enable wg-quick@wg_{ASN}.service && service wg-quick@wg_{ASN} start")

print("\n##### Reconfigure BIRD...")
os.system("birdc c")
print('====================================================\n')

time.sleep(5)
print(f'-----> wg show wg_{ASN}')
os.system(f"wg show wg_{ASN}")
print('----------------------------------------------------')
print(f'-----> birdc s p all dn42_{ASN}_v6')
os.system(f"birdc s p all dn42_{ASN}_v6")
if is_split_v4v6_session:
    print(f'-----> birdc s p all dn42_{ASN}_v4')
    os.system(f"birdc s p all dn42_{ASN}_v4")

print("\n##### Everything is OK!")

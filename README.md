# MeowDN42wheels

Some tools for MiaoTony's DN42 Network, aka MeowNetwork

***喵喵又在造轮子啦！***

# Tools

## DN42 Free ASN Finder

`find_free_ASN.py` 用于查询空闲未被使用的 ASN，你可以自己改代码挑选你喜欢的编号。

你需要先 clone https://git.dn42.dev/dn42/registry 然后列出 `data/aut-num/` 文件夹下的文件到 `aut-num.txt`

```bash
git clone git@git.dn42.dev:<FOO>/registry.git
# Where <FOO> is your gitea username.
ls -1 registry/data/aut-num/ > aut-num.txt
python3 find_free_ASN.py
```


## Copyright

**本项目仅供学习研究使用，请在合理合法范围内使用！**  
**The relevant technical content of this project is only for study and research, please use within the reasonable and legal scope!**  

License:  
[MIT License](LICENSE)  

最终解释权归本项目开发者所有。  
The final interpretation right belongs to the developer of the project.  

Copyright © 2023 [MiaoTony](https://github.com/miaotony).  
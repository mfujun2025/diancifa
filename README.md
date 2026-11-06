# 电磁阀.cn 官方网站

销售电磁阀产品的静态官网 + 「电磁阀.cn / 电磁阀.中国」域名出售专页。纯 HTML / CSS / 原生 JS，无后端、无第三方依赖，可直接托管在 GitHub Pages 或任意静态服务器。

- 咨询邮箱：`548827878@qq.com`（全站顶部、页脚、CTA 与联系页均显著展示）
- QQ：`548827878`
- 域名：`电磁阀.cn`（punycode：`xn--wnyq9e038a.cn`）

## 页面清单

| 页面 | 文件 | 说明 |
| --- | --- | --- |
| 首页 | `index.html` | 主视觉、产品分类、常用型号、应用行业、询价流程、FAQ |
| 产品中心 | `products.html` | 8 款产品网格，支持分类筛选与关键词搜索 |
| 产品详情 | `products/*.html` | 每款独立详情页：大图、参数表、特点、应用、选型须知、询价按钮 |
| 关于我们 | `about.html` | 站点定位、服务内容、工作方式 |
| 联系我们 | `contact.html` | 邮箱 / QQ / 一键复制 / 询价入口 |
| 询价订购 | `inquiry.html` | 询价单表单（生成邮件 + 复制内容），支持 `?model=` 带入型号 |
| 域名出售 | `domains.html` | 两个域名的优势、价格说明、购买流程、联系方式、FAQ |
| 404 | `404.html` | 错误页 |

附属文件：`sitemap.xml`、`robots.txt`、`.nojekyll`、`assets/data/products.json`（产品数据源）。

## 目录结构

```
.
├── index.html / products.html / about.html / contact.html
├── inquiry.html / domains.html / 404.html
├── products/                 # 8 个产品详情页
├── assets/
│   ├── css/style.css         # 全站样式（含响应式断点 1024 / 820 / 600）
│   ├── js/main.js            # 导航、筛选、复制、询价表单、toast
│   ├── images/               # 产品图与场景图，WebP + JPEG 双格式
│   └── data/products.json    # 产品数据（由生成脚本导出）
├── tools/build.py            # 页面生成脚本（模板 + 数据集中维护）
├── sitemap.xml / robots.txt / .nojekyll
└── README.md
```

## 本地预览

```bash
python -m http.server 8080
# 浏览器打开 http://127.0.0.1:8080/
```

也可以直接用浏览器打开 `index.html`（站内链接均为相对路径，`file://` 下同样可用）。

## 修改内容

所有页面由 `tools/build.py` 生成，**请勿直接改 HTML**（会被下次生成覆盖）：

```bash
python tools/build.py
```

- 改产品型号 / 参数 / 分类：编辑 `tools/build.py` 顶部的 `PRODUCTS` 与 `CATEGORIES`
- 改邮箱 / QQ / 站点域名：编辑 `EMAIL`、`QQ`、`SITE` 常量
- 改页面文案与结构：编辑对应的 `build_xxx()` 函数
- 生成后请重新检查 `sitemap.xml` 的 `TODAY` 日期

## 部署与访问

仓库 `mfujun2025/diancifa` 已通过 `gh-pages` 分支启用 GitHub Pages，并绑定中文域名：

- **主站（已生效）：https://xn--wnyq9e038a.cn/**（浏览器地址栏显示为「电磁阀.cn」）
- 项目预览地址：`https://mfujun2025.github.io/diancifa/`，会跳转到主域名

仓库根目录 `CNAME` 文件的内容为 `xn--wnyq9e038a.cn`（中文域名的 punycode 形式），由 GitHub Pages 用于绑定自定义域名，**请勿删除**。DNS 已解析生效，HTTP 与 HTTPS 均可访问。

分支约定：

- `main`：主分支，日常内容修改提交到这里
- `gh-pages`：GitHub Pages 发布源，内容与 `main` 保持一致

更新线上内容（`main` 提交推送后执行）：

```bash
git push origin main
git push --force-with-lease origin main:gh-pages
```

如果不想维护两个分支，可在仓库 Settings → Pages 把发布源改为 `main` / `/(root)`，之后只推送 `main` 即可。

> 提示：DNS 未生效前不要添加 `CNAME`，否则 GitHub Pages 会把 `github.io` 地址重定向到未解析的域名，导致预览地址也无法访问。境内服务器还需按法规完成 ICP 备案；使用 GitHub Pages 时请自行评估合规要求。

## 询价表单工作方式

静态站点没有后端，表单**不会**在服务器留存数据：点击提交后由本机浏览器生成一封格式化邮件（`mailto:`）并唤起邮件客户端；用户也可点击「复制询价单内容」粘贴到邮箱或 QQ 发送。从产品详情页点「询价 / 订购」会通过 URL 参数自动带入型号；域名页的购买入口会带入域名名称。

## 待确认 / 可替换信息

以下内容未擅自编造，需要站方确认后替换：

| 项目 | 当前处理 |
| --- | --- |
| 域名挂牌价格 | 页面写「面议 / 欢迎出价」，说明单独购买、打包购买与议价方式；如需一口价，改 `build_domains()` 中的 `.domain-price` 与「价格说明」区块 |
| 公司主体信息 | 未编造企业名称、资质、注册资本、案例数据；`about.html` 以站点定位与服务内容描述，如有正式主体可替换 |
| 电话 / 地址 / 工作时间 | 未提供，页面仅展示用户指定的邮箱与由邮箱对应的 QQ |
| 产品参数 | 为行业典型参考值，已全站标注「以双方确认的订货参数为准」 |
| 产品图片 | 来源于网络公开资料的电磁阀实物照片，本地托管为 WebP + JPEG；如涉版权或需换成自有产品图，替换 `assets/images/` 同名文件即可 |
| 备案与隐私合规 | 表单不收集服务器数据；如后续增加在线支付、用户注册或境内服务器，需补充隐私政策与备案 |

## 图片与性能

- 产品图统一裁为 900×900 白底，WebP 优先、JPEG 兜底（`<picture>`），单张 WebP 约 7–32 KB
- 非首屏图片 `loading="lazy"`、`decoding="async"`
- 无外部字体、无 JS 框架、无外部图片请求，页面可离线打开（图片已本地化）

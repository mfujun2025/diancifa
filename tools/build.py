# -*- coding: utf-8 -*-
"""
电磁阀.cn 官网静态页面生成脚本

用法：在项目根目录执行  python tools/build.py
产物：根目录 HTML、products/ 详情页、guides/ 技术文章页、sitemap.xml、robots.txt
页面模板与数据集中在本文件，长文正文在 content/*.md（Markdown）。
改内容后重新运行即可全站更新，勿直接编辑生成的 HTML。
"""
from pathlib import Path
from urllib.parse import quote
from html import escape as html_escape
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mdrender import render_markdown

ROOT = Path(__file__).resolve().parent.parent
EMAIL = "548827878@qq.com"
QQ = "548827878"
BRAND = "电磁阀.cn"
SITE = "https://xn--wnyq9e038a.cn"  # 电磁阀.cn 的 punycode 形式
TODAY = "2026-11-06"

# 技术指南栏目：Markdown 源文件 → 栏目页 + 长文详情页
GUIDE_SLUG = "solenoid-valve-guide"
GUIDE_MD = "content/" + GUIDE_SLUG + ".md"
GUIDE_PATH = "guides/" + GUIDE_SLUG + ".html"
GUIDE_DESC = (
    "约 1.1 万字电磁阀系统长文：讲清电磁阀工作原理、直动式与先导式结构差异、类型与关键参数、"
    "典型应用场景、电磁阀选型流程、安装维护要点与电磁阀故障排查思路，并附常见问题解答，"
    "面向工业自动化、设备维护与采购读者。"
)

CATEGORIES = [
    ("all", "全部产品"),
    ("general", "通用水用型"),
    ("pneumatic", "气动控制型"),
    ("special", "特殊工况型"),
    ("custom", "定制选型"),
]

PRODUCTS = [
    {
        "slug": "2w160-15",
        "name": "2W160-15 二位二通直动式电磁阀",
        "series": "2W 系列 · 通用水用型",
        "cat": "general",
        "cat_label": "通用水用型",
        "img": "product-01",
        "short": "直动式常闭结构，黄铜阀体，无压差启动，适合水、空气及轻油等常规介质的通断控制。",
        "lead": "2W160-15 属于二位二通常闭直动式电磁阀，通电开启、断电靠弹簧复位关闭。直动式结构不依赖介质压差，从 0 bar 起即可动作，常用于小通径给排水、设备配套与自动化管路。",
        "specs": [
            ("产品系列", "2W 系列 / 2W160-15"),
            ("结构形式", "二位二通（2/2 通），常闭型，直动式"),
            ("阀体材质", "黄铜锻压阀体"),
            ("接口尺寸", "G1/2 英寸（4 分），可按需确认其他螺纹规格"),
            ("公称通径", "约 15 mm"),
            ("适用介质", "水、压缩空气、轻油及中性流体"),
            ("工作压力", "0 ~ 1.0 MPa（典型值）"),
            ("介质温度", "-5 ~ 80 ℃（视密封材质而定）"),
            ("密封材质", "NBR / EPDM / FKM 可选"),
            ("工作电压", "AC220V、AC110V、DC24V、DC12V 可选"),
            ("防护等级", "IP65（配标准线圈，可选防爆线圈）"),
            ("安装方式", "水平管路安装，线圈朝上，介质流向与阀体箭头一致"),
        ],
        "features": [
            "零压差启动，低压力或重力供水工况同样可靠",
            "黄铜阀体耐腐蚀性与机械强度兼顾，通用性高",
            "常闭设计，断电自动关闭，降低无人值守泄漏风险",
            "线圈可选交流 / 直流多种电压，便于对接控制系统",
            "结构紧凑、拆装方便，密封件可按介质选配",
            "适用于频繁启闭的自动化通断控制场景",
        ],
        "apps": ["给排水设备", "水处理系统", "清洗设备", "空压机配套", "灌溉系统", "通用自动化"],
        "keywords": "2W160-15 二位二通 直动式 常闭 黄铜 水用电磁阀 G1/2 DC24V",
    },
    {
        "slug": "2w250-25",
        "name": "2W250-25 先导膜片式电磁阀",
        "series": "2W 系列 · 大流量水用型",
        "cat": "general",
        "cat_label": "通用水用型",
        "img": "product-02",
        "short": "先导膜片结构，通径更大、流量更高，适用于主管路供水、循环水与设备冷却的通断控制。",
        "lead": "2W250-25 采用先导式膜片结构，借助介质压差放大开启力，在较大通径下仍能保持较低功耗与稳定启闭。适合主管路、循环冷却水、清洗线等需要较大流量的场合。",
        "specs": [
            ("产品系列", "2W 系列 / 2W250-25"),
            ("结构形式", "二位二通（2/2 通），常闭型，先导膜片式"),
            ("阀体材质", "黄铜阀体，膜片组件可更换"),
            ("接口尺寸", "G1 英寸（1 寸），可确认法兰或其他规格"),
            ("公称通径", "约 25 mm"),
            ("适用介质", "水、中性液体、压缩空气"),
            ("工作压力", "0.05 ~ 1.0 MPa（先导式需最小压差）"),
            ("介质温度", "-5 ~ 80 ℃（视密封材质而定）"),
            ("密封材质", "NBR / EPDM / FKM 可选"),
            ("工作电压", "AC220V、DC24V 等，可按需选配"),
            ("防护等级", "IP65（标准线圈）"),
            ("安装方式", "建议水平安装，进口侧需保证最低启动压差"),
        ],
        "features": [
            "先导膜片结构，大通径下仍保持较低线圈功率",
            "流量系数高，适合主管路与循环水管网",
            "膜片组件可单独更换，后期维护成本低",
            "常闭断电关闭，便于系统安全联锁",
            "多种电压与密封材质组合，适配不同介质",
            "可提供常开型、法兰连接等配置确认",
        ],
        "apps": ["循环冷却水", "主管路供水", "工业清洗线", "泳池与水景", "水处理设备", "锅炉补水"],
        "keywords": "2W250-25 先导式 膜片 大流量 常闭 水用电磁阀 G1 1寸",
    },
    {
        "slug": "2w320-32",
        "name": "2W320-32 大口径膜片电磁阀",
        "series": "2W 系列 · 大口径型",
        "cat": "general",
        "cat_label": "通用水用型",
        "img": "product-03",
        "short": "面向更大口径管路的膜片式电磁阀，适合大流量供水、冷却循环及管网分区控制。",
        "lead": "2W320-32 面向更大口径的管路通断需求，膜片式先导结构在 DN32 级别仍能提供稳定启闭与较大流通能力。常用于厂区供水分区、冷却塔补水和大流量清洗系统。",
        "specs": [
            ("产品系列", "2W 系列 / 2W320-32"),
            ("结构形式", "二位二通，常闭型，先导膜片式"),
            ("阀体材质", "黄铜阀体（可选不锈钢版本）"),
            ("接口尺寸", "G1-1/4 英寸，可确认法兰连接"),
            ("公称通径", "约 32 mm"),
            ("适用介质", "水、中性液体"),
            ("工作压力", "0.05 ~ 1.0 MPa（典型值）"),
            ("介质温度", "-5 ~ 80 ℃（视密封材质而定）"),
            ("密封材质", "NBR / EPDM 可选"),
            ("工作电压", "AC220V、DC24V 等"),
            ("防护等级", "IP65（标准线圈）"),
            ("安装方式", "水平安装，管路前端建议加装过滤器"),
        ],
        "features": [
            "大通径设计，压损小、通过能力强",
            "膜片先导开启，线圈功耗与口径解耦",
            "建议配合过滤器使用，降低杂质卡滞风险",
            "可按需确认常开型、法兰式或不锈钢阀体",
            "适合长周期通断、间歇补水的分区控制",
            "阀体结构便于现场检修与膜片更换",
        ],
        "apps": ["厂区供水分区", "冷却塔补水", "大流量清洗", "水处理主管道", "农业灌溉", "楼宇水系统"],
        "keywords": "2W320-32 大口径 膜片电磁阀 DN32 大流量 常闭 黄铜",
    },
    {
        "slug": "3v210-08",
        "name": "3V210-08 二位三通电磁阀",
        "series": "3V 系列 · 气动控制型",
        "cat": "pneumatic",
        "cat_label": "气动控制型",
        "img": "product-04",
        "short": "二位三通气动电磁阀，用于单作用气缸、真空吸附与气路切换，响应快、体积小。",
        "lead": "3V210-08 为二位三通气动换向阀，可实现供气、排气与保持三种气路状态切换，常用于单作用气缸驱动、真空发生与吸附控制。紧凑阀体适合集成在设备气路板上。",
        "specs": [
            ("产品系列", "3V 系列 / 3V210-08"),
            ("结构形式", "二位三通（3/2 通），常闭型"),
            ("阀体材质", "铝合金 / 不锈钢阀体，按配置确认"),
            ("接口尺寸", "G1/4 英寸"),
            ("适用介质", "洁净压缩空气（建议过滤、干燥）"),
            ("工作压力", "0.15 ~ 0.8 MPa（典型值）"),
            ("介质温度", "-5 ~ 60 ℃"),
            ("工作电压", "DC24V、DC12V、AC220V 可选"),
            ("响应时间", "≤ 0.05 s（典型值，视工况而定）"),
            ("防护等级", "IP65（标准线圈）"),
            ("安装方式", "单阀或汇流板集成安装"),
            ("选配附件", "线圈、接头、消声器、汇流板"),
        ],
        "features": [
            "三通切换，兼顾供气与排气，控制逻辑简单",
            "响应速度快，适合高频动作的气动执行机构",
            "体积小巧，支持汇流板多阀集成",
            "多种电压与接线方式，便于接入 PLC 控制",
            "建议前端配置过滤减压与润滑单元",
            "可按需确认常开型与不同接口规格",
        ],
        "apps": ["单作用气缸", "真空吸附", "包装机械", "自动化装配", "气路切换", "检测设备"],
        "keywords": "3V210-08 二位三通 气动电磁阀 3/2 常闭 G1/4 DC24V 单作用气缸",
    },
    {
        "slug": "4v210-08",
        "name": "4V210-08 二位五通气动电磁阀",
        "series": "4V 系列 · 气动换向型",
        "cat": "pneumatic",
        "cat_label": "气动控制型",
        "img": "product-05",
        "short": "二位五通换向阀，用于双作用气缸往复控制，是自动化设备最常配的气动元件之一。",
        "lead": "4V210-08 属于二位五通气动换向电磁阀，通过切换两路工作口实现双作用气缸的伸出与缩回。滑柱式结构动作可靠、维护方便，广泛用于各类自动化设备与产线。",
        "specs": [
            ("产品系列", "4V 系列 / 4V210-08"),
            ("结构形式", "二位五通（5/2 通），单线圈"),
            ("阀体材质", "铝合金阀体，滑柱式阀芯"),
            ("接口尺寸", "G1/4 英寸（进气 / 工作口 / 排气）"),
            ("适用介质", "洁净压缩空气（40 μm 以上过滤）"),
            ("工作压力", "0.15 ~ 0.8 MPa（典型值）"),
            ("介质温度", "-5 ~ 60 ℃"),
            ("工作电压", "DC24V、DC12V、AC220V、AC110V 可选"),
            ("防护等级", "IP65（标准线圈）"),
            ("接线方式", "DIN 插座式 / 出线式可选"),
            ("安装方式", "单阀安装或汇流板集成"),
            ("选配附件", "汇流板、消声器、接头、手动override装置"),
        ],
        "features": [
            "五通双工作口，专为双作用气缸往复动作设计",
            "滑柱式阀芯，换向平稳、寿命长",
            "可配手动调试装置，方便现场试机与排查",
            "支持单阀与汇流板集成，扩展阀组灵活",
            "多种电压与接线形式，适配不同电控柜",
            "配套消声器可降低排气噪声",
        ],
        "apps": ["双作用气缸", "自动化产线", "包装设备", "机床上下料", "工装夹具", "物流分拣"],
        "keywords": "4V210-08 二位五通 气动电磁阀 5/2 换向阀 DC24V 双作用气缸 汇流板",
    },
    {
        "slug": "4v410-15",
        "name": "4V410-15 五通集成阀组",
        "series": "4V 系列 · 阀岛集成型",
        "cat": "pneumatic",
        "cat_label": "气动控制型",
        "img": "product-06",
        "short": "多联阀组集成方案，统一供气与排气，减少管路接头，适合多气缸集中控制。",
        "lead": "4V410-15 集成阀组把多个五通电磁阀安装在共用汇流板上，统一供气、统一排气，显著减少现场管路与接头数量。适用于多执行机构集中控制的设备与产线，也便于后期扩展阀位。",
        "specs": [
            ("产品系列", "4V 系列 / 4V410-15 阀组"),
            ("结构形式", "二位五通多联集成，共用汇流板"),
            ("阀体材质", "铝合金阀体与汇流板"),
            ("接口尺寸", "G1/2 英寸（主进气），工作口按配置确认"),
            ("适用介质", "洁净压缩空气"),
            ("工作压力", "0.15 ~ 0.8 MPa（典型值）"),
            ("介质温度", "-5 ~ 60 ℃"),
            ("工作电压", "DC24V / AC220V 可选"),
            ("阀位数量", "按需求配置联数，可预留扩展位"),
            ("防护等级", "IP65（标准线圈）"),
            ("安装方式", "汇流板整体固定于设备气控柜"),
            ("选配附件", "盲板、消声器、接头、气管"),
        ],
        "features": [
            "统一供排气，管路简洁，泄漏点更少",
            "阀位可按需增减，方便设备改型与扩容",
            "集中安装，检修时单阀可独立拆换",
            "减少接头与气管用量，降低装配工时",
            "可配合 PLC 多路输出实现集中控制",
            "适合多气缸、多工位的自动化设备",
        ],
        "apps": ["多工位设备", "装配产线", "包装机械", "机器人周边", "气控柜集成", "物流输送"],
        "keywords": "4V410-15 阀组 阀岛 汇流板 五通电磁阀 集成 气路 多联",
    },
    {
        "slug": "slz-timer",
        "name": "数显定时自动排水电磁阀",
        "series": "智能控制 · 定制选型",
        "cat": "custom",
        "cat_label": "定制选型",
        "img": "product-07",
        "short": "内置数显定时控制，按设定周期自动排放冷凝水，适用于空压机、储气罐与过滤系统。",
        "lead": "数显定时排水电磁阀把控制单元与阀体集成在一起，可按设定的开启时长与间隔周期自动排放冷凝水，减少人工巡检与忘记排水造成的积水问题。定时参数可按现场工况调整，也可按需求选配不同电压与接口。",
        "specs": [
            ("产品类型", "定时控制一体式排水电磁阀"),
            ("控制方式", "数显定时，可设定开启间隔与排放时长"),
            ("阀体材质", "黄铜阀体，按配置确认"),
            ("接口尺寸", "G1/2 英寸等，按现场管路确认"),
            ("适用介质", "冷凝水、压缩空气系统排水"),
            ("工作压力", "0 ~ 1.6 MPa（典型值，以配置为准）"),
            ("介质温度", "-5 ~ 80 ℃"),
            ("工作电压", "AC220V / DC24V 可选"),
            ("防护等级", "IP65（按配置确认）"),
            ("安装位置", "储气罐、过滤器、干燥机底部排水口"),
            ("选配项", "手动测试按钮、过滤网、报警输出"),
            ("交付方式", "按参数确认后供货，支持批量订购"),
        ],
        "features": [
            "定时自动排放，减少人工巡检与遗漏排水",
            "开启间隔与排放时长可调，避免压缩空气浪费",
            "控制与阀体一体集成，接线与安装简单",
            "带手动测试功能，便于现场验证动作",
            "可按电压、接口、压力范围做配置确认",
            "适用于多台设备的批量改造与配套",
        ],
        "apps": ["空压机系统", "储气罐", "冷干机", "精密过滤器", "气源净化", "设备改造"],
        "keywords": "定时排水阀 数显 自动排水电磁阀 空压机 冷凝水 储气罐 定制",
    },
    {
        "slug": "zs-high-pressure",
        "name": "ZS 系列高压耐热黄铜电磁阀",
        "series": "ZS 系列 · 特殊工况型",
        "cat": "special",
        "cat_label": "特殊工况型",
        "img": "product-08",
        "short": "面向较高压力与温度工况的加强型阀体结构，适合蒸汽、热水及高压气液管路。",
        "lead": "ZS 系列面向压力、温度条件高于常规水路的应用场景，采用加强型阀体与耐高温密封配置，适合热水、蒸汽及高压气液管路的通断控制。具体压力、温度与密封组合需按现场工况逐项确认后选型。",
        "specs": [
            ("产品系列", "ZS 系列 · 加强型"),
            ("结构形式", "二位二通，常闭型，先导活塞 / 膜片按配置确认"),
            ("阀体材质", "黄铜加强阀体（可选不锈钢）"),
            ("接口尺寸", "G1/2、G3/4 等，按管路确认"),
            ("适用介质", "热水、蒸汽、高压空气、中性液体"),
            ("工作压力", "按工况确认，高于常规水用型"),
            ("介质温度", "按密封材质确认，可选耐高温配置"),
            ("密封材质", "FKM / PTFE / EPDM 可选"),
            ("工作电压", "AC220V、DC24V 等"),
            ("防护等级", "IP65，可选耐高温线圈"),
            ("安装方式", "水平安装，建议前端加装过滤与减压"),
            ("选型要求", "需提供介质、压力、温度、电压与接口参数"),
        ],
        "features": [
            "加强型阀体，适配更高压力与温度条件",
            "多种耐高温密封材质可按需选配",
            "可选耐高温线圈，降低长期通电温升影响",
            "建议按实际工况逐项核对，避免超范围使用",
            "支持不锈钢阀体等材质的替代确认",
            "适合设备配套改造与批量选型",
        ],
        "apps": ["热水系统", "蒸汽管路", "高压气源", "清洗灭菌", "工业炉配套", "化工辅机"],
        "keywords": "高压电磁阀 耐热 蒸汽 热水 黄铜加强 FKM PTFE 特殊工况 选型",
    },
]


def picture(name, alt, base="", cls=""):
    """WebP 优先 + JPEG 兜底的产品图片标签"""
    return (
        '<picture class="' + cls + '">'
        '<source srcset="' + base + 'assets/images/' + name + '.webp" type="image/webp">'
        '<img src="' + base + 'assets/images/' + name + '.jpg" alt="' + alt + '" loading="lazy" decoding="async">'
        '</picture>'
    )


def header(active, B):
    items = [
        ("index.html", "首页", "home"),
        ("products.html", "产品中心", "products"),
        ("guides.html", "技术指南", "guides"),
        ("about.html", "关于我们", "about"),
        ("contact.html", "联系我们", "contact"),
        ("domains.html", "域名出售", "domains"),
    ]
    links = "".join(
        '<a href="' + B + f + '"' + (' class="is-active"' if k == active else '') + '>' + t + '</a>'
        for f, t, k in items
    )
    return f'''<header class="site-header">
  <div class="topbar">
    <div class="container topbar-inner">
      <span class="topbar-tag">电磁阀选型 · 报价 · 订购一站式对接</span>
      <div class="topbar-contact">
        <span>咨询邮箱：<strong><a href="mailto:{EMAIL}">{EMAIL}</a></strong></span>
        <span class="sep">·</span>
        <span class="topbar-qq">QQ：<strong>{QQ}</strong></span>
        <span class="sep">·</span>
        <a class="topbar-domain" href="{B}domains.html">域名出售：电磁阀.cn / .中国</a>
      </div>
    </div>
  </div>
  <div class="container nav-inner">
    <a class="logo" href="{B}index.html" aria-label="{BRAND} 首页">
      <span class="logo-mark">DCF</span>
      <span><span class="logo-text">{BRAND}</span><span class="logo-sub">SOLENOID VALVE</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-label="展开导航菜单" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav" aria-label="主导航">{links}</nav>
    <a class="btn btn-primary nav-cta" href="{B}inquiry.html">获取报价</a>
  </div>
</header>'''


def cta_band(B, title="需要选型建议或批量报价？", text="把型号、数量和使用工况发给我们，我们会尽快回复并提供报价与选型建议。"):
    return f'''<section class="section section--soft" style="padding:44px 0">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>{title}</h2>
        <p>{text}</p>
        <p class="mt-s"><a class="cta-mail" href="mailto:{EMAIL}">✉ {EMAIL}</a></p>
      </div>
      <div class="btn-row">
        <a class="btn btn-primary btn-lg" href="{B}inquiry.html">在线询价 / 订购</a>
        <a class="btn btn-ghost-light btn-lg" href="{B}contact.html">更多联系方式</a>
      </div>
    </div>
  </div>
</section>'''


def footer(B):
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <h3>{BRAND}</h3>
        <p>聚焦电磁阀产品选型、询价与订购对接的垂直站点。提供通用水用、气动控制、特殊工况及定制选型等多类产品的选型参考与报价服务。</p>
        <p>产品图片来源于网络公开资料，仅作产品类型示意；如需替换或涉及版权问题，请联系 <a href="mailto:{EMAIL}">{EMAIL}</a>。</p>
      </div>
      <div>
        <h3>快速导航</h3>
        <ul>
          <li><a href="{B}index.html">首页</a></li>
          <li><a href="{B}products.html">产品中心</a></li>
          <li><a href="{B}guides.html">技术指南</a></li>
          <li><a href="{B}about.html">关于我们</a></li>
          <li><a href="{B}contact.html">联系我们</a></li>
          <li><a href="{B}domains.html">域名出售</a></li>
        </ul>
      </div>
      <div>
        <h3>产品分类</h3>
        <ul>
          <li><a href="{B}products.html">通用水用型</a></li>
          <li><a href="{B}products.html">气动控制型</a></li>
          <li><a href="{B}products.html">特殊工况型</a></li>
          <li><a href="{B}products.html">定制选型</a></li>
          <li><a href="{B}inquiry.html">询价 / 订购</a></li>
        </ul>
      </div>
      <div>
        <h3>联系我们</h3>
        <p class="contact-label">咨询 / 报价 / 域名购买</p>
        <p><a class="footer-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p>QQ：{QQ}</p>
        <p><a class="btn btn-outline" href="{B}inquiry.html">填写询价单</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {BRAND} · 保留所有权利</span>
      <span>本站产品参数为典型参考值，实际配置以双方确认的订货信息为准</span>
    </div>
  </div>
</footer>'''


def faq(items):
    return '<div class="faq">' + "".join(
        '<details' + (' open' if i == 0 else '') + '><summary>' + q + '</summary><p>' + a + '</p></details>'
        for i, (q, a) in enumerate(items)
    ) + '</div>'


def page(title, desc, body, B, active, path, show_cta=True, jsonld="",
         og_type="website", keywords=None):
    canonical = SITE + "/" + path if path else SITE + "/"
    kw = keywords or "电磁阀,电磁阀选型,电磁阀报价,气动电磁阀,水用电磁阀," + BRAND
    main_body = body + (cta_band(B) if show_cta else "")
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{B}assets/css/style.css">
{jsonld}
</head>
<body>
{header(active, B)}
<main>
{main_body}
</main>
{footer(B)}
<div class="mobile-bar">
  <a href="mailto:{EMAIL}">✉ 邮件咨询</a>
  <a href="{B}products.html">产品中心</a>
  <a class="primary" href="{B}inquiry.html">立即询价</a>
</div>
<div class="toast" role="status" aria-live="polite"></div>
<script src="{B}assets/js/main.js"></script>
</body>
</html>
'''


def product_card(p, B, link_prefix):
    href = link_prefix + p["slug"] + ".html"
    return f'''<article class="product-card" data-category="{p['cat']}" data-keywords="{p['keywords']} {p['name']}">
  <a class="product-card__img" href="{href}">{picture(p['img'], p['name'] + ' 产品照片', B)}</a>
  <div class="product-card__body">
    <span class="product-card__cat">{p['cat_label']}</span>
    <h3><a href="{href}">{p['name']}</a></h3>
    <p>{p['short']}</p>
    <div class="product-card__foot">
      <span class="price-note">价格：按配置报价</span>
      <a class="btn btn-outline" href="{B}inquiry.html?model={quote(p['name'])}">询价</a>
    </div>
  </div>
</article>'''


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("  ->", rel)


# =========================================================
# 首页
# =========================================================
def build_index():
    B = ""
    cards = "".join(product_card(PRODUCTS[i], B, "products/") for i in (0, 1, 4, 6))
    home_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": BRAND,
        "url": SITE + "/",
        "description": "电磁阀产品选型、询价与订购对接站点",
        "contactPoint": {"@type": "ContactPoint", "email": EMAIL, "contactType": "sales", "availableLanguage": "zh-CN"}
    }, ensure_ascii=False)
    hero = f'''<section class="hero">
  <div class="container hero-inner">
    <span class="eyebrow">SOLENOID VALVE · 选型 / 报价 / 订购</span>
    <h1>电磁阀选型、报价与订购<br>一站式对接</h1>
    <p class="hero-lead">通用水用、气动控制、特殊工况与定制选型多类产品集中展示，提供参数参考、选型建议与快速报价通道。看中型号即可直接发起询价。</p>
    <div class="btn-row">
      <a class="btn btn-primary btn-lg" href="products.html">浏览全部产品</a>
      <a class="btn btn-ghost-light btn-lg" href="inquiry.html">立即询价 / 订购</a>
    </div>
    <div class="hero-points">
      <span>多系列型号集中展示</span><span>按工况协助选型</span><span>邮箱 / QQ 直接对接</span>
    </div>
  </div>
</section>'''

    trust = '''<section class="section section--soft">
  <div class="container">
    <div class="stat-strip">
      <div><strong>产品分类清晰</strong><small>按用途与工况归类，快速定位</small></div>
      <div><strong>参数逐项列出</strong><small>接口、压力、电压一目了然</small></div>
      <div><strong>选型协助</strong><small>提供工况信息即可协助匹配</small></div>
      <div><strong>询价通道</strong><small>表单 / 邮件 / QQ 多种方式</small></div>
    </div>
  </div>
</section>'''

    cats = '''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">PRODUCT CATEGORIES</span><h2>按用途找产品</h2><p>先按应用方向缩小范围，再进入详情页核对参数与配置。</p></div>
    <div class="grid grid-4">
      <a class="card" href="products.html"><div class="card-icon">01</div><h3>通用水用型</h3><p>二位二通常闭阀，覆盖给排水、循环水与设备配套等常见水路通断控制。</p></a>
      <a class="card" href="products.html"><div class="card-icon">02</div><h3>气动控制型</h3><p>二位三通、二位五通换向阀与集成阀组，适配气缸驱动与气路切换。</p></a>
      <a class="card" href="products.html"><div class="card-icon">03</div><h3>特殊工况型</h3><p>面向较高压力、温度或特殊介质，按工况确认阀体与密封配置。</p></a>
      <a class="card" href="products.html"><div class="card-icon">04</div><h3>定制选型</h3><p>定时控制、特殊电压与接口等需求，提供参数后协助确认配置。</p></a>
    </div>
  </div>
</section>'''

    hot = f'''<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FEATURED PRODUCTS</span><h2>常用型号展示</h2><p>以下为常见选型方向的代表型号，点击可查看详细参数与询价入口。</p></div>
    <div class="product-grid">{cards}</div>
    <div class="text-center mt-l"><a class="btn btn-blue btn-lg" href="products.html">查看全部 {len(PRODUCTS)} 款产品 →</a></div>
  </div>
</section>'''

    apps = '''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">APPLICATIONS</span><h2>常见应用行业</h2><p>电磁阀广泛用于流体通断与气动控制，以下为常见配套场景。</p></div>
    <div class="grid grid-3">
      <div class="card"><h3>水处理与给排水</h3><p>净水设备、循环冷却水、补水与管网分区控制。</p></div>
      <div class="card"><h3>工业自动化</h3><p>气缸驱动、工装夹具、装配与包装产线的气动换向。</p></div>
      <div class="card"><h3>食品与饮料</h3><p>清洗、灌装、CIP 清洗管路的介质通断与切换。</p></div>
      <div class="card"><h3>空压与气源</h3><p>储气罐、冷干机、过滤器的冷凝水定时排放。</p></div>
      <div class="card"><h3>暖通与锅炉</h3><p>热水、蒸汽及补水系统的通断与温度工况适配。</p></div>
      <div class="card"><h3>化工与辅机</h3><p>中性介质管路、设备配套及特殊材质的选型确认。</p></div>
    </div>
  </div>
</section>'''

    steps = '''<section class="section section--navy">
  <div class="container">
    <div class="section-head"><span class="eyebrow">HOW IT WORKS</span><h2>询价与订购流程</h2><p>把需求说清楚，剩下的选型与报价由我们对接。</p></div>
    <div class="steps">
      <div class="step"><h3>提交需求</h3><p>通过询价表单、邮件或 QQ 提供型号、数量与工况信息。</p></div>
      <div class="step"><h3>确认选型</h3><p>核对介质、压力、温度、电压、接口与密封材质等参数。</p></div>
      <div class="step"><h3>获取报价</h3><p>按确认后的配置提供报价说明与交付信息。</p></div>
      <div class="step"><h3>下单交付</h3><p>双方确认订货信息后安排后续供货与对接。</p></div>
    </div>
  </div>
</section>'''

    guide_teaser = '''<section class="section section--soft" style="padding:38px 0">
  <div class="container">
    <div class="card" style="display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap">
      <div>
        <p style="font-size:13px;color:var(--accent);font-weight:700;letter-spacing:.06em;margin:0 0 6px">技术指南 · 约 1.1 万字系统长文</p>
        <h3 style="margin-bottom:6px">电磁阀完全指南：工作原理、类型划分、选型要点与故障排查</h3>
        <p>系统梳理定义与原理、类型划分、关键参数、应用场景、选型流程、安装维护、故障排查与常见误区，附参数核对清单和常见问题。<a href="guides/solenoid-valve-guide.html">阅读全文 →</a></p>
      </div>
      <a class="btn btn-outline" href="guides.html">进入技术指南</a>
    </div>
  </div>
</section>'''

    domain_teaser = '''<section class="section section--soft">
  <div class="container">
    <div class="card" style="display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap">
      <div><h3 style="margin-bottom:6px">域名出售：电磁阀.cn / 电磁阀.中国</h3><p>两个行业精准中文域名同步转让，适合终端品牌与行业平台建设。<a href="domains.html">查看域名详情与购买方式 →</a></p></div>
      <a class="btn btn-outline" href="domains.html">查看域名出售页</a>
    </div>
  </div>
</section>'''

    home_faq = faq([
        ("如何获取产品报价？", "在询价页填写型号、数量与使用工况，或直接发邮件到 " + EMAIL + " / QQ " + QQ + "，我们会按确认后的配置回复报价。"),
        ("页面上没有我要的型号怎么办？", "可以直接把介质、压力、温度、电压、接口尺寸等信息发给我们，我们会协助匹配可供货的型号与配置。"),
        ("产品参数可以直接用于设计选型吗？", "页面参数为典型参考值，用于初步筛选。正式选型请以双方确认的订货参数与产品资料为准。"),
        ("支持批量订购吗？", "支持。请提供型号清单与数量，我们会按批量需求统一回复报价与交付安排。"),
    ])
    faq_sec = f'''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FAQ</span><h2>常见问题</h2></div>
    {home_faq}
  </div>
</section>'''

    body = hero + trust + cats + hot + apps + guide_teaser + steps + domain_teaser + faq_sec + cta_band(
        B, "把需求发过来，报价与选型一次对接", "咨询邮箱 " + EMAIL + " · QQ " + QQ + " · 也可直接填写在线询价单")
    write("index.html", page(
        BRAND + " - 电磁阀选型、产品展示与询价订购",
        "电磁阀.cn 提供二位二通水用电磁阀、气动换向电磁阀、集成阀组与定制选型的产品参数展示、选型建议及询价订购入口，联系邮箱 " + EMAIL + "。",
        body, B, "home", "", show_cta=False,
        jsonld='<script type="application/ld+json">' + home_jsonld + '</script>'))


# =========================================================
# 产品中心
# =========================================================
def build_products():
    B = ""
    btns = "".join(
        '<button class="filter-btn' + (' is-active' if k == "all" else '') + '" type="button" data-filter="' + k + '">' + t + '</button>'
        for k, t in CATEGORIES
    )
    cards = "".join(product_card(p, B, "products/") for p in PRODUCTS)
    body = f'''<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">首页</a><span>/</span>产品中心</div>
    <h1>产品中心</h1>
    <p>按用途与工况分类展示常用电磁阀型号，逐款提供参数表、特点说明与询价入口。</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="filter-bar">
      {btns}
      <label class="filter-search"><span aria-hidden="true">🔍</span><input id="product-search" type="search" placeholder="搜索型号或关键词" aria-label="搜索产品型号或关键词"></label>
    </div>
    <div class="product-grid" id="product-list">{cards}</div>
    <p class="filter-empty" id="filter-empty" style="display:none">没有匹配的产品，试试其他关键词，或直接 <a href="inquiry.html">提交定制需求</a>。</p>
    <div class="detail-buy mt-l">
      <strong>选型提示：</strong>页面参数为典型参考值。请结合介质、压力、温度、电压、接口尺寸与密封材质逐项核对；不确定时，把工况信息发到 <a href="mailto:{EMAIL}">{EMAIL}</a>，我们协助匹配型号。
    </div>
  </div>
</section>'''
    write("products.html", page(
        "产品中心 - 电磁阀型号与参数 | " + BRAND,
        "电磁阀产品中心：通用水用型、气动控制型、特殊工况型与定制选型的型号列表、参数参考与询价入口。",
        body, B, "products", "products.html"))


# =========================================================
# 产品详情页
# =========================================================
def build_detail(p, idx):
    B = "../"
    spec_rows = "".join('<tr><th>' + k + '</th><td>' + v + '</td></tr>' for k, v in p["specs"])
    key_specs = "".join('<div><span>' + k + '</span>' + v + '</div>' for k, v in p["specs"][:4])
    features = "".join('<li>' + x + '</li>' for x in p["features"])
    apps = "".join('<span>' + x + '</span>' for x in p["apps"])
    related = [PRODUCTS[(idx + i) % len(PRODUCTS)] for i in (1, 2, 3)]
    related_html = "".join(product_card(r, B, "") for r in related)

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Product",
        "name": p["name"], "description": p["short"],
        "image": SITE + "/assets/images/" + p["img"] + ".jpg",
        "category": p["cat_label"], "brand": {"@type": "Brand", "name": BRAND}
    }, ensure_ascii=False)

    body = f'''<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="{B}index.html">首页</a><span>/</span><a href="{B}products.html">产品中心</a><span>/</span>{p['cat_label']}</div>
    <h1>产品详情</h1>
    <p>核对参数、确认工况，即可直接发起询价或订购。</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="detail-layout">
      <div class="detail-photo">
        {picture(p['img'], p['name'] + ' 实物照片', B)}
        <div class="photo-note">图片为该类产品的实物照片示意，实际外观与配置以双方确认的订货信息为准。</div>
      </div>
      <div class="detail-info">
        <div class="series">{p['series']}</div>
        <h1>{p['name']}</h1>
        <p class="lead">{p['lead']}</p>
        <div class="key-specs">{key_specs}</div>
        <div class="btn-row">
          <a class="btn btn-primary btn-lg" href="{B}inquiry.html?model={quote(p['name'])}">询价 / 订购此型号</a>
          <a class="btn btn-outline btn-lg" href="mailto:{EMAIL}?subject={quote('询价：' + p['name'])}">邮件咨询</a>
        </div>
        <div class="detail-buy">
          <strong>询价时请一并提供：</strong>介质类型、工作压力、介质温度、电源电压、接口尺寸、采购数量。信息越完整，选型与报价越准确。
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">SPECIFICATIONS</span><h2>技术参数</h2><p>下表为典型参考值，正式选型请以确认后的订货参数为准。</p></div>
    <table class="spec-table"><tbody>{spec_rows}</tbody></table>
    <p class="table-note">说明：不同电压、密封材质与接口配置会改变部分参数；如工况超出上表范围，请先联系我们确认可行性。</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid-2">
      <div>
        <h2>产品特点</h2>
        <ul class="check-list">{features}</ul>
      </div>
      <div>
        <h2>典型应用</h2>
        <div class="tag-list">{apps}</div>
        <h3 class="mt-l">选型与订货须知</h3>
        <p style="color:#5d6c7b">电磁阀选型需同时确认介质相容性、压差条件、电压制式与安装方向。先导式结构需要最小启动压差；介质含杂质时建议前端加装过滤器。本站不承诺具体交期与库存，相关信息以双方书面确认的订单为准。</p>
        <a class="btn btn-blue mt-s" href="{B}inquiry.html?model={quote(p['name'])}">带型号发起询价 →</a>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">RELATED</span><h2>相关产品</h2></div>
    <div class="product-grid">{related_html}</div>
  </div>
</section>'''
    write("products/" + p["slug"] + ".html", page(
        p["name"] + " - 参数、选型与询价 | " + BRAND,
        p["short"] + " 查看 " + p["name"] + " 的技术参数、产品特点、典型应用与询价方式。",
        body, B, "products", "products/" + p["slug"] + ".html",
        jsonld='<script type="application/ld+json">' + ld + '</script>'))


# =========================================================
# 关于我们
# =========================================================
def build_about():
    B = ""
    body = f'''<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">首页</a><span>/</span>关于我们</div>
    <h1>关于我们</h1>
    <p>认识电磁阀.cn：我们做什么、如何服务，以及为什么把「选型信息说清楚」放在第一位。</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="detail-layout">
      <div>
        <span class="eyebrow" style="color:#e2621b;font-weight:700;letter-spacing:.12em;font-size:13px">ABOUT {BRAND}</span>
        <h2>一个把电磁阀选型讲清楚的站点</h2>
        <p>{BRAND} 是聚焦电磁阀产品选型、询价与订购对接的垂直站点。我们把常见的通用水用阀、气动换向阀、集成阀组与特殊工况产品按用途归类，逐款列出接口、压力、电压、材质等选型必须确认的参数，让采购与技术人员在发起询价前就能缩小范围。</p>
        <p>我们不做夸张的宣传，也不虚构资质与案例数据。能做的是什么就写什么：把型号信息整理清楚，按客户提供的工况协助匹配，再把报价与订货信息逐项确认。产品图片来源于网络公开资料，仅用于产品类型示意。</p>
        <p>如果你是企业采购、设备工程师或系统集成商，只需要一个能快速查参数、能直接联系到人的入口，这个站点就是为此而建。</p>
      </div>
      <div>
        <picture><source srcset="assets/images/scene-pipeline.webp" type="image/webp"><img src="assets/images/scene-pipeline.jpg" alt="工业管道与设备现场照片" loading="lazy" decoding="async" style="border-radius:10px"></picture>
        <div class="detail-buy mt-s"><strong>联系通道：</strong><br>邮箱 <a href="mailto:{EMAIL}">{EMAIL}</a><br>QQ {QQ}<br><a href="inquiry.html">在线询价单 →</a></div>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">WHAT WE DO</span><h2>我们提供的服务</h2><p>围绕「选对型号、问清价格、顺利下单」三个环节展开。</p></div>
    <div class="grid grid-4">
      <div class="card"><div class="card-icon">A</div><h3>选型信息整理</h3><p>按用途与工况分类展示型号，逐款列出需要核对的技术参数。</p></div>
      <div class="card"><div class="card-icon">B</div><h3>工况匹配建议</h3><p>根据介质、压力、温度、电压与接口信息，协助缩小可选型号范围。</p></div>
      <div class="card"><div class="card-icon">C</div><h3>报价对接</h3><p>按确认后的配置回复报价说明，批量需求可统一整理清单。</p></div>
      <div class="card"><div class="card-icon">D</div><h3>订购流程跟进</h3><p>订货信息确认后，配合完成后续供货对接与信息核对。</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">PRINCIPLES</span><h2>我们的做法</h2></div>
    <div class="grid grid-3">
      <div class="card"><h3>参数先说清楚</h3><p>典型参考值与实际配置的边界写明，避免选型时产生误解。</p></div>
      <div class="card"><h3>不虚构信息</h3><p>不编造企业资质、产能、客户案例与库存数据；未确认的信息如实标注。</p></div>
      <div class="card"><h3>联系路径短</h3><p>顶部、底部与产品页都留有邮箱与询价入口，不用层层跳转。</p></div>
    </div>
  </div>
</section>'''
    write("about.html", page(
        "关于我们 - " + BRAND,
        "了解 " + BRAND + " 的定位、服务内容与选型对接方式，联系邮箱 " + EMAIL + "。",
        body, B, "about", "about.html"))


# =========================================================
# 联系我们
# =========================================================
def build_contact():
    B = ""
    body = f'''<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">首页</a><span>/</span>联系我们</div>
    <h1>联系我们</h1>
    <p>产品询价、选型咨询、批量订购与域名购买，都可以通过以下方式直接联系。</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid-2">
      <div class="contact-card">
        <h2 style="margin-bottom:6px">咨询邮箱</h2>
        <p class="contact-label">产品询价 / 订购 / 域名购买，均使用此邮箱</p>
        <p><a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
        <div class="btn-row">
          <a class="btn btn-primary" href="mailto:{EMAIL}">发送邮件</a>
          <button class="btn btn-outline" type="button" data-copy="{EMAIL}">复制邮箱</button>
        </div>
        <div class="mt-l">
          <div class="contact-row"><span class="contact-label">QQ</span><strong>{QQ}</strong><a class="btn btn-outline" style="padding:7px 14px" href="https://wpa.qq.com/msgrd?v=3&uin={QQ}&site=qq&menu=yes" target="_blank" rel="noopener">QQ 咨询</a></div>
          <div class="contact-row"><span class="contact-label">在线询价</span><a href="inquiry.html">填写询价 / 订购单 →</a></div>
          <div class="contact-row"><span class="contact-label">域名业务</span><a href="domains.html">电磁阀.cn / 电磁阀.中国 出售详情 →</a></div>
        </div>
      </div>
      <div>
        <div class="card">
          <h2>联系前准备这些信息</h2>
          <p>信息越完整，回复越准确。建议按下面清单整理后一并发送：</p>
          <ul class="check-list">
            <li>需要的型号或应用场景</li>
            <li>介质类型（水 / 气 / 油 / 蒸汽等）</li>
            <li>工作压力与介质温度范围</li>
            <li>电源电压（AC220V / DC24V 等）</li>
            <li>接口尺寸与安装方式</li>
            <li>采购数量与期望交付时间</li>
          </ul>
          <p class="mt-m"><a class="btn btn-blue" href="inquiry.html">直接填写在线询价单 →</a></p>
        </div>
        <div class="detail-buy mt-m">
          <strong>说明：</strong>本站为静态展示站点，询价表单通过您本机的邮件客户端发送，不会在网站服务器上留存表单内容。邮件与 QQ 留言收到后会尽快回复。
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FAQ</span><h2>联系相关常见问题</h2></div>
    {faq([
        ("发邮件后多久会有回复？", "我们会在收到邮件后尽快回复。若涉及多型号或需要核对工况，回复中可能先与您确认参数，再给出报价。"),
        ("没有邮箱客户端怎么办？", "可以复制询价单内容后通过 QQ " + QQ + " 发送，或直接在询价页复制内容粘贴到网页版邮箱。"),
        ("可以只咨询选型、不下单吗？", "可以。把工况参数发过来即可，我们会协助梳理需要重点确认的选型项。"),
        ("域名购买和产品询价是同一个联系方式吗？", "是。域名购买请在邮件主题中注明「域名购买 - 电磁阀.cn」或「域名购买 - 电磁阀.中国」，便于分办。"),
    ])}
  </div>
</section>'''
    write("contact.html", page(
        "联系我们 - 邮箱 " + EMAIL + " | " + BRAND,
        "联系 " + BRAND + "：咨询邮箱 " + EMAIL + "、QQ " + QQ + "，支持产品询价、选型咨询、批量订购及域名购买咨询。",
        body, B, "contact", "contact.html", show_cta=False))


# =========================================================
# 询价 / 订购
# =========================================================
def build_inquiry():
    B = ""
    opts = "".join('<option value="' + p["name"] + '">' + p["name"] + '</option>' for p in PRODUCTS)
    body = f'''<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">首页</a><span>/</span>询价 / 订购</div>
    <h1>询价 / 订购</h1>
    <p>填写下方信息，系统会生成一封格式化的询价邮件；确认内容后通过邮件客户端发送即可。</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="detail-layout">
      <div class="card">
        <h2 style="margin-bottom:4px">询价 / 订购单</h2>
        <p style="color:#5d6c7b;font-size:14px">带 <span style="color:#e2621b">*</span> 为必填项。提交后会唤起您的邮件客户端，请核对后发送。</p>
        <form id="inquiry-form" novalidate>
          <div class="form-grid">
            <div class="field"><label for="f-name">联系人 <span class="req">*</span></label><input id="f-name" name="name" type="text" required placeholder="您的姓名"></div>
            <div class="field"><label for="f-company">公司名称</label><input id="f-company" name="company" type="text" placeholder="公司 / 单位名称"></div>
            <div class="field"><label for="f-phone">联系电话</label><input id="f-phone" name="phone" type="tel" placeholder="手机或座机"></div>
            <div class="field"><label for="f-email">电子邮箱 <span class="req">*</span></label><input id="f-email" name="email" type="email" required placeholder="便于我们回复报价"></div>
            <div class="field field--full"><label for="f-model">产品型号 / 需求</label><input id="f-model" name="model" type="text" list="model-list" placeholder="可填写型号，或描述需求"><datalist id="model-list">{opts}<option value="其他型号 / 待协助选型"></option></datalist></div>
            <div class="field"><label for="f-qty">采购数量</label><input id="f-qty" name="qty" type="text" placeholder="例如：20 只"></div>
            <div class="field"><label for="f-type">需求类型</label><select id="f-type" name="type"><option value="询价">产品询价</option><option value="订购">直接订购</option><option value="选型咨询">选型咨询</option><option value="批量报价">批量报价</option><option value="域名购买">域名购买</option></select></div>
            <div class="field field--full"><label for="f-medium">介质与工况</label><input id="f-medium" name="medium" type="text" placeholder="例如：清水 / 0.4MPa / 常温 / DC24V / G1/2"></div>
            <div class="field field--full"><label for="f-note">补充说明</label><textarea id="f-note" name="note" placeholder="交付要求、替代型号、预算范围、域名报价等均可在此说明"></textarea><span class="field-hint">若咨询域名购买，请注明具体域名：电磁阀.cn 或 电磁阀.中国。</span></div>
          </div>
          <label class="form-agree mt-m"><input type="checkbox" required><span>我同意将上述信息用于本次询价与订购沟通；本站不会在服务器上留存表单内容。</span></label>
          <div class="form-actions">
            <button class="btn btn-primary btn-lg" type="submit">生成询价邮件并发送</button>
            <button class="btn btn-outline btn-lg" id="copy-inquiry" type="button">复制询价单内容</button>
          </div>
          <p class="form-note">若未自动打开邮件客户端，可点击「复制询价单内容」，粘贴到邮箱或 QQ 发送给 <a href="mailto:{EMAIL}">{EMAIL}</a>。</p>
        </form>
      </div>
      <div>
        <div class="contact-card">
          <h2>直接联系</h2>
          <p class="contact-label">咨询 / 报价 / 订购</p>
          <p><a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p>QQ：{QQ}</p>
          <div class="btn-row"><a class="btn btn-blue" href="mailto:{EMAIL}">发送邮件</a><button class="btn btn-outline" type="button" data-copy="{EMAIL}">复制邮箱</button></div>
        </div>
        <div class="card mt-m">
          <h3>询价单里最好写清楚什么</h3>
          <ul>
            <li>型号或应用场景</li>
            <li>介质、压力、温度</li>
            <li>电压、接口、密封材质</li>
            <li>数量与交付要求</li>
          </ul>
          <p style="color:#5d6c7b;font-size:14px;margin-bottom:0">参数越完整，报价越准确；不确定时也可以先发需求，我们会协助核对。</p>
        </div>
        <div class="detail-buy mt-m"><strong>隐私说明：</strong>本页为静态页面，表单内容仅在您的浏览器内生成邮件，不经过网站服务器，也不会被自动保存。</div>
      </div>
    </div>
  </div>
</section>'''
    write("inquiry.html", page(
        "询价 / 订购 - 在线询价单 | " + BRAND,
        "填写电磁阀询价 / 订购单，提供型号、数量与工况信息，发送至 " + EMAIL + " 获取报价与选型建议。",
        body, B, "inquiry", "inquiry.html", show_cta=False))


# =========================================================
# 域名出售页
# =========================================================
def build_domains():
    B = ""
    domain_data = [
        {
            "name": "电磁阀.cn",
            "punycode": "xn--wnyq9e038a.cn",
            "type": ".cn 国家顶级域名",
            "desc": "与产品词完全一致的短域名，行业指向明确、输入简短，适合作为企业官网主域名长期持有。",
            "points": [
                "与核心产品词「电磁阀」完全一致，用户一眼就知道站点做什么",
                ".cn 后缀简短、认知度高，适合印在名片、包装与宣传物料上",
                "中文母语用户可直接记忆与口述，降低推广中的拼写流失",
                "适合承接官网、产品目录、询盘落地页与行业内容站",
                "行业通用词域名具备长期品牌与流量价值",
            ],
        },
        {
            "name": "电磁阀.中国",
            "punycode": "xn--wnyq9e038a.xn--fiqs8s",
            "type": ".中国 中文顶级域名",
            "desc": "纯中文后缀域名，与 .cn 组合持有可形成品牌保护，适合面向国内客户做本地化传播。",
            "points": [
                "域名与后缀全部为中文，品牌表达完整统一",
                "与「电磁阀.cn」组合持有，可覆盖不同输入习惯的用户",
                "适合做中文品牌宣传、跳转入口或防御性注册",
                "利于防止同行业抢注近似中文域名造成品牌混淆",
                "对面向国内市场的行业平台与渠道站点尤其友好",
            ],
        },
    ]
    cards = ""
    for d in domain_data:
        pts = "".join('<li>' + x + '</li>' for x in d["points"])
        cards += f'''<article class="domain-card">
  <div class="domain-card__top">
    <span class="domain-card__status">● 可转让 / 接受询价</span>
    <div class="domain-card__name">{d['name']}</div>
    <div class="domain-card__punycode">{d['type']} · 转码 {d['punycode']}</div>
  </div>
  <div class="domain-card__body">
    <p style="color:#5d6c7b">{d['desc']}</p>
    <div class="domain-price"><span class="label">价格</span><span class="value">面议 / 欢迎出价</span><span class="hint">支持单独或打包购买</span></div>
    <ul>{pts}</ul>
    <div class="btn-row">
      <a class="btn btn-primary" href="{B}inquiry.html?domain={quote(d['name'])}">提交购买意向</a>
      <a class="btn btn-outline" href="mailto:{EMAIL}?subject={quote('域名购买咨询：' + d['name'])}">邮件报价</a>
    </div>
  </div>
</article>'''

    adv = '''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">WHY THESE DOMAINS</span><h2>为什么这两个域名值得持有</h2><p>行业精准中文域名的价值，来自「好记、好懂、好传播」三件事。</p></div>
    <div class="advantage-num">
      <div class="card"><h3>01 · 词与生意完全一致</h3><p>「电磁阀」是行业核心产品词，客户搜索、询价、口述推荐时用的就是这三个字，域名无需二次解释。</p></div>
      <div class="card"><h3>02 · 中文记忆成本低</h3><p>中文用户可以直接记住并念出来，不需要拼写英文缩写或猜测拼音组合，线下与电话场景尤其明显。</p></div>
      <div class="card"><h3>03 · 品牌与流量双重资产</h3><p>既是官网门牌，也是自然流量入口。用于官网、产品站、询价落地页或行业内容站都能直接承接意向客户。</p></div>
      <div class="card"><h3>04 · 稀缺性明确</h3><p>行业通用词 + 短后缀的组合数量有限，同类精准中文域名一旦被终端持有，通常很难再次流通。</p></div>
      <div class="card"><h3>05 · 两域名形成保护</h3><p>.cn 与 .中国 一并持有，可覆盖不同输入习惯，并减少近似域名造成的分流与混淆。</p></div>
      <div class="card"><h3>06 · 适配搜索与 AI 问答</h3><p>域名与站点主题高度一致，配合清晰的产品结构、问答式内容与实体信息，更利于被搜索与生成式问答引用。</p></div>
    </div>
  </div>
</section>'''

    scenes = '''<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">WHO SHOULD BUY</span><h2>适合谁购买</h2></div>
    <div class="grid grid-4">
      <div class="card"><h3>电磁阀生产厂商</h3><p>用作品牌官网主域名，让产品词直接成为品牌入口。</p></div>
      <div class="card"><h3>经销商与代理商</h3><p>搭建区域销售站、产品目录与询盘落地页。</p></div>
      <div class="card"><h3>行业平台 / 媒体</h3><p>承接选型资料、行业资讯与供应商黄页内容。</p></div>
      <div class="card"><h3>域名投资与品牌保护</h3><p>组合持有两个中文后缀，作为长期资产或防御性注册。</p></div>
    </div>
  </div>
</section>'''

    policy = '''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">PRICE & TERMS</span><h2>价格与交易说明</h2><p>把定价方式、购买方式与交割流程写清楚，方便双方一次谈到位。</p></div>
    <div class="grid grid-2">
      <div class="price-policy">
        <h3>价格说明</h3>
        <ul>
          <li><strong>挂牌价格：面议（接受买方出价）</strong>，请以邮件报价为准，我们会对每个报价逐一回复。</li>
          <li>两个域名可<strong>单独购买</strong>，也可<strong>打包购买</strong>；打包询价可优先洽谈，价格从优。</li>
          <li>如需书面报价单、域名证书信息或权属材料，请在邮件中注明，我们按需提供。</li>
          <li>价格、支付方式与交割时间均以双方最终书面确认的内容为准，页面展示不构成要约。</li>
        </ul>
      </div>
      <div class="card">
        <h3>购买流程</h3>
        <ul class="check-list" style="grid-template-columns:1fr">
          <li>发送邮件或填写询价单，注明域名与您的出价</li>
          <li>双方确认价格、域名清单与交易方式</li>
          <li>通过双方认可的注册商 / 平台办理转移或过户</li>
          <li>确认过户完成后完成交割</li>
        </ul>
        <p class="mt-s" style="color:#5d6c7b;font-size:14px">过户所需材料与操作时长以实际注册商规则为准，我们会配合提供必要信息。</p>
      </div>
    </div>
  </div>
</section>'''

    buy = f'''<section class="section section--soft">
  <div class="container">
    <div class="buy-block">
      <h2>有意购买？直接联系</h2>
      <p>请在邮件主题中注明「域名购买 - 电磁阀.cn」或「域名购买 - 电磁阀.中国」，并留下您的报价与联系方式。</p>
      <a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a>
      <p style="margin-top:8px">QQ：{QQ}</p>
      <div class="btn-row">
        <a class="btn btn-primary btn-lg" href="mailto:{EMAIL}?subject={quote('域名购买咨询：电磁阀.cn / 电磁阀.中国')}">发送购买邮件</a>
        <a class="btn btn-ghost-light btn-lg" href="{B}inquiry.html?domain={quote('电磁阀.cn / 电磁阀.中国')}">填写购买意向上表</a>
        <button class="btn btn-ghost-light btn-lg" type="button" data-copy="{EMAIL}">复制邮箱</button>
      </div>
    </div>
  </div>
</section>'''

    domain_faq = faq([
        ("这两个域名的价格是多少？", "当前采用议价方式，接受买方出价。请发邮件到 " + EMAIL + " 注明域名与报价，我们会逐一回复；如需书面报价单也可在邮件中说明。"),
        ("可以只买其中一个吗？", "可以。电磁阀.cn 与电磁阀.中国 均支持单独购买；同时打包购买可优先洽谈，价格从优。"),
        ("域名如何过户？", "双方确认价格后，通过双方认可的注册商或域名交易平台办理转移 / 过户，具体材料与时长以注册商规则为准。"),
        ("可以先看看域名当前解析的站点吗？", "可以。电磁阀.cn 当前展示的就是本产品站，可作为域名使用场景的参考；.中国 后缀可按购买方需求另行规划。"),
        ("除了域名，还能一起谈站点内容吗？", "可以一并说明需求。若希望连同站点结构、产品内容一起交接，请在邮件中写明范围，我们会在回复中一并说明可行性与条件。"),
    ])
    faq_sec = f'''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FAQ</span><h2>域名购买常见问题</h2></div>
    {domain_faq}
    <p class="text-center mt-m" style="color:#5d6c7b;font-size:13px">域名状态、价格与交易条件以双方最终书面确认为准；本页面信息不构成要约或权属承诺。</p>
  </div>
</section>'''

    hero = f'''<section class="domain-hero">
  <div class="container">
    <span class="eyebrow">PREMIUM CHINESE DOMAINS FOR SALE</span>
    <h1>两个行业精准中文域名，正在出售</h1>
    <p>电磁阀.cn 与 电磁阀.中国 —— 与核心产品词完全一致，适合电磁阀厂商、经销商、行业平台与品牌保护长期持有。接受单独或打包购买询价。</p>
    <div class="domain-badges"><span>行业通用词</span><span>中文直达</span><span>.cn + .中国 组合</span><span>可议价</span><span>支持过户</span></div>
    <div class="btn-row" style="justify-content:center;margin-top:28px">
      <a class="btn btn-primary btn-lg" href="{B}inquiry.html?domain={quote('电磁阀.cn / 电磁阀.中国')}">提交购买意向</a>
      <a class="btn btn-ghost-light btn-lg" href="mailto:{EMAIL}?subject={quote('域名购买咨询：电磁阀.cn / 电磁阀.中国')}">邮件报价</a>
    </div>
  </div>
</section>'''

    list_sec = f'''<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">DOMAIN LIST</span><h2>出售域名清单</h2><p>两个域名均为行业精准中文域名，可单独或组合持有。</p></div>
    <div class="domain-grid">{cards}</div>
  </div>
</section>'''

    body = hero + list_sec + adv + scenes + policy + buy + faq_sec
    write("domains.html", page(
        "域名出售 - 电磁阀.cn / 电磁阀.中国 转让 | " + BRAND,
        "电磁阀.cn 与电磁阀.中国 两个行业精准中文域名出售，说明域名优势、价格方式、购买流程与联系方式，购买咨询邮箱 " + EMAIL + "。",
        body, B, "domains", "domains.html", show_cta=False))


# =========================================================
# 技术指南栏目 / 长文详情页
# =========================================================
def _guide(base):
    """读取 Markdown 源文并渲染一次；栏目页与详情页复用解析结果。"""
    return render_markdown((ROOT / GUIDE_MD).read_text(encoding="utf-8"), base=base)


def build_guides():
    B = ""
    g = _guide(B)
    words = "约 %.1f 万字" % (g["cjk"] / 10000)
    minutes = max(1, round(g["cjk"] / 450))
    title_text = html_escape(g["title"])
    topics = "".join(
        '<a class="topic-chip" href="' + GUIDE_PATH + "#" + sid + '">' + html_escape(label) + "</a>"
        for sid, label in g["toc"] if label not in ("常见问题", "结语")
    )

    hero = '''<section class="guide-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">首页</a><span>/</span>技术指南</div>
    <span class="eyebrow">TECHNICAL GUIDE</span>
    <h1>技术指南</h1>
    <p class="guide-hero__lead">围绕电磁阀工作原理、类型划分、关键参数、选型流程与故障排查，整理可长期查阅的中文技术资料，面向工业自动化、设备维护与采购读者。</p>
  </div>
</section>'''

    listing = f'''<section class="section">
  <div class="container">
    <div class="section-head"><span class="eyebrow">LATEST ARTICLES</span><h2>全部文章</h2><p>按主题成体系展开，附参数核对清单与常见问题。</p></div>
    <div class="guide-list">
      <article class="guide-card">
        <div class="guide-card__main">
          <span class="guide-card__tag">选型与维护 · 系统长文</span>
          <h2><a href="{GUIDE_PATH}">{title_text}</a></h2>
          <p>{GUIDE_DESC}</p>
          <div class="guide-card__meta"><span>更新：{TODAY}</span><span>{words}</span><span>预计阅读 {minutes} 分钟</span><span>{len(g["toc"])} 个章节 · {len(g["faq"])} 条常见问题</span></div>
        </div>
        <div class="guide-card__side">
          <a class="btn btn-primary" href="{GUIDE_PATH}">阅读全文 →</a>
          <a class="btn btn-outline" href="inquiry.html">按工况询价</a>
        </div>
      </article>
    </div>
  </div>
</section>'''

    quick = f'''<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">BROWSE BY TOPIC</span><h2>按主题快速跳转</h2><p>直接从目录进入长文对应章节，便于查阅与分享。</p></div>
    <div class="topic-list">{topics}</div>
  </div>
</section>'''

    help_block = f'''<section class="section">
  <div class="container">
    <div class="card">
      <h3>需要针对具体工况核对参数？</h3>
      <p>把介质、压力、温度、电压、接口与数量整理好，可通过 <a href="inquiry.html">在线询价 / 订购</a> 提交，或发邮件到 <a href="mailto:{EMAIL}">{EMAIL}</a>；也可先到 <a href="products.html">产品中心</a> 对照常见型号的典型参数。</p>
    </div>
  </div>
</section>'''

    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "技术指南 - " + BRAND,
        "description": "电磁阀工作原理、类型划分、关键参数、选型流程、安装维护与故障排查的中文技术文章合集。",
        "url": SITE + "/guides.html",
        "inLanguage": "zh-CN",
        "mainEntity": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": g["title"], "url": SITE + "/" + GUIDE_PATH}
        ]},
    }, ensure_ascii=False)
    body = hero + listing + quick + help_block
    write("guides.html", page(
        "技术指南 - 电磁阀工作原理、选型与故障排查文章 | " + BRAND,
        "电磁阀.cn 技术指南栏目：系统整理电磁阀工作原理、类型划分、关键参数、电磁阀选型流程与电磁阀故障排查方法的中文长文。",
        body, B, "guides", "guides.html",
        keywords="电磁阀,电磁阀工作原理,电磁阀选型,电磁阀故障,电磁阀技术指南," + BRAND,
        jsonld='<script type="application/ld+json">' + ld + '</script>'))


def build_guide_article():
    B = "../"
    g = _guide(B)
    words = "约 %.1f 万字" % (g["cjk"] / 10000)
    minutes = max(1, round(g["cjk"] / 450))
    title_text = html_escape(g["title"])
    toc = "".join(
        '<li><a href="#' + sid + '">' + html_escape(label) + "</a></li>" for sid, label in g["toc"]
    )
    article_html = g["html"]
    related_cards = "".join(product_card(PRODUCTS[i], B, B + "products/") for i in (0, 1, 4))

    hero = f'''<section class="article-hero" id="top">
  <div class="container">
    <div class="breadcrumb"><a href="{B}index.html">首页</a><span>/</span><a href="{B}guides.html">技术指南</a><span>/</span>电磁阀完全指南</div>
    <span class="article-tag">技术指南 · 选型与维护</span>
    <h1>{title_text}</h1>
    <p class="article-deck">从电磁阀工作原理到电磁阀选型与电磁阀故障排查，按十个章节系统梳理现场最常遇到的判断依据与处理顺序，附参数核对清单和常见问题。</p>
    <div class="article-meta"><span>更新：{TODAY}</span><span>{words}</span><span>预计阅读 {minutes} 分钟</span><span>面向：工业自动化 / 设备维护 / 采购</span></div>
  </div>
</section>'''

    article = f'''<section class="section article-section">
  <div class="container article-layout">
    <aside class="article-toc" aria-label="本文目录">
      <div class="toc-inner">
        <p class="toc-title">本文目录</p>
        <ol>{toc}</ol>
        <a class="toc-top" href="#top">↑ 回到顶部</a>
      </div>
    </aside>
    <article class="article-body">
      {article_html}
      <div class="article-footnote">本文整理的是通用工程判断方法，不替代具体产品的说明书、图纸与现场安全规范；参数边界以制造商资料与双方确认的订货信息为准。</div>
    </article>
  </div>
</section>'''

    related = f'''<section class="section section--soft">
  <div class="container">
    <div class="section-head"><span class="eyebrow">RELATED PRODUCTS</span><h2>相关产品与延伸阅读</h2><p>对照具体型号的参数，或直接提交工况信息获取选型建议。</p></div>
    <div class="product-grid">{related_cards}</div>
    <div class="related-links">
      <a href="{B}guides.html">← 返回技术指南</a>
      <a href="{B}products.html">浏览全部产品</a>
      <a href="{B}inquiry.html">在线询价 / 订购</a>
      <a href="{B}contact.html">联系我们</a>
    </div>
  </div>
</section>'''

    faq_entities = [
        {"@type": "Question", "name": item["q"],
         "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
        for item in g["faq"]
    ]
    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首页", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "技术指南", "item": SITE + "/guides.html"},
                {"@type": "ListItem", "position": 3, "name": g["title"], "item": SITE + "/" + GUIDE_PATH},
            ]},
            {"@type": "Article", "headline": g["title"], "description": GUIDE_DESC,
             "inLanguage": "zh-CN", "wordCount": g["cjk"],
             "datePublished": TODAY, "dateModified": TODAY,
             "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
             "publisher": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
             "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + "/" + GUIDE_PATH},
             "keywords": "电磁阀,电磁阀工作原理,电磁阀选型,电磁阀故障"},
            {"@type": "FAQPage", "mainEntity": faq_entities},
        ],
    }, ensure_ascii=False)
    body = hero + article + related
    write(GUIDE_PATH, page(
        g["title"] + " | " + BRAND,
        GUIDE_DESC,
        body, B, "guides", GUIDE_PATH, og_type="article",
        keywords="电磁阀,电磁阀工作原理,电磁阀选型,电磁阀故障,电磁阀类型,电磁阀参数," + BRAND,
        jsonld='<script type="application/ld+json">' + ld + '</script>'))


# =========================================================
# 404 / sitemap / robots
# =========================================================
def build_misc():
    B = ""
    body = f'''<section class="section">
  <div class="container text-center">
    <p style="font-size:64px;font-weight:800;color:#12558f;margin:0">404</p>
    <h1>页面没有找到</h1>
    <p style="color:#5d6c7b">您访问的页面可能已调整，可以从下面的入口继续浏览。</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary" href="index.html">返回首页</a>
      <a class="btn btn-outline" href="products.html">产品中心</a>
      <a class="btn btn-outline" href="guides.html">技术指南</a>
      <a class="btn btn-outline" href="domains.html">域名出售</a>
    </div>
  </div>
</section>'''
    write("404.html", page("页面未找到 - " + BRAND, "页面未找到，请返回首页或产品中心继续浏览。", body, B, "", "404.html", show_cta=False))

    paths = ["", "products.html", "guides.html", GUIDE_PATH, "about.html", "contact.html", "inquiry.html", "domains.html"] + [
        "products/" + p["slug"] + ".html" for p in PRODUCTS
    ]
    urls = "".join(
        '  <url><loc>' + SITE + '/' + p + '</loc><lastmod>' + TODAY + '</lastmod><changefreq>weekly</changefreq><priority>' +
        ('1.0' if p == "" else '0.8' if p in ("products.html", "domains.html", "guides.html", GUIDE_PATH) else '0.6') + '</priority></url>\n'
        for p in paths
    )
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: " + SITE + "/sitemap.xml\n")
    write(".nojekyll", "")
    write("assets/data/products.json", json.dumps(PRODUCTS, ensure_ascii=False, indent=2))


def main():
    print("生成 " + BRAND + " 站点页面 ...")
    build_index()
    build_products()
    for i, p in enumerate(PRODUCTS):
        build_detail(p, i)
    build_about()
    build_contact()
    build_inquiry()
    build_domains()
    build_guides()
    build_guide_article()
    build_misc()
    print("完成。共生成", 8 + len(PRODUCTS) + 4, "个 HTML/附属文件。")


if __name__ == "__main__":
    main()

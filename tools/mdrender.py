# -*- coding: utf-8 -*-
"""
站点技术文章专用的极简 Markdown 渲染器（无第三方依赖）。

支持语法：# / ## / ### / #### 标题、段落、GFM 表格，
行内 **加粗**、`代码` 与 [文字](链接)。链接中的 {{B}} 会替换成页面相对根路径。

正文先做 HTML 转义、再还原受支持的行内标记，避免内容意外注入。
额外产出章节目录、FAQ 问答对与汉字数，供页面生成和结构化数据使用。
"""
import html
import re

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SEP_RE = re.compile(r"^[-:\s]*$")


def plain(text):
    """去掉行内标记，得到用于目录与结构化数据的纯文本。"""
    return re.sub(r"\*\*|`", "", LINK_RE.sub(r"\1", text)).strip()


def _href(url, base):
    return url.replace("{{B}}", base)


def inline(text, base=""):
    s = html.escape(text, quote=True)
    s = LINK_RE.sub(
        lambda m: '<a href="' + _href(m.group(2), base) + '">' + m.group(1) + "</a>", s
    )
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _blocks(lines):
    """把 Markdown 切成 (块类型, 行列表) 序列。"""
    blocks, buf, kind = [], [], None

    def flush():
        nonlocal buf, kind
        if buf:
            blocks.append((kind, buf))
            buf = []
        kind = None

    for raw in lines:
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("#"):
            flush()
            blocks.append(("heading", [line]))
        elif line.startswith("|"):
            if kind not in (None, "table"):
                flush()
            kind = "table"
            buf.append(line)
        else:
            if kind == "table":
                flush()
            kind = "p"
            buf.append(line)
    flush()
    return blocks


def _table(rows, base):
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    head = cells[0]
    data = [r for r in cells[1:] if not all(SEP_RE.match(c or "-") for c in r)]
    thead = "<thead><tr>" + "".join("<th>" + inline(c, base) + "</th>" for c in head) + "</tr></thead>"
    body = "".join(
        "<tr>" + "".join("<td>" + inline(c, base) + "</td>" for c in r) + "</tr>" for r in data
    )
    return '<div class="table-wrap"><table>' + thead + "<tbody>" + body + "</tbody></table></div>"


def render_markdown(md, base=""):
    """返回 {title, html, toc, faq, cjk}；H1 由页面头部单独输出，不重复渲染。"""
    out, toc, faq = [], [], []
    title = ""
    sec = sub = 0
    in_faq = faq_open = details_open = False

    def close_details():
        nonlocal details_open
        if details_open:
            out.append("</details>")
            details_open = False

    def close_faq():
        nonlocal faq_open
        close_details()
        if faq_open:
            out.append("</div>")
            faq_open = False

    def toc_label(text):
        return re.sub(r"^[一二三四五六七八九十]+、\s*", "", plain(text))

    for kind, rows in _blocks(md.splitlines()):
        if kind == "heading":
            m = HEAD_RE.match(rows[0])
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                title = plain(text)
                continue
            close_details()
            if level == 2 and in_faq:
                close_faq()
                in_faq = False
            if level == 2:
                sec, sub = sec + 1, 0
                sid = "sec-%d" % sec
                out.append('<h2 id="' + sid + '">' + inline(text, base) + "</h2>")
                toc.append((sid, toc_label(text)))
                if plain(text) == "常见问题":
                    in_faq = faq_open = True
                    out.append('<div class="faq faq--article">')
            elif level == 3:
                sub += 1
                if in_faq:
                    out.append(("<details open>" if not faq else "<details>") + "<summary>" + inline(text, base) + "</summary>")
                    details_open = True
                    faq.append({"q": plain(text), "a": ""})
                else:
                    out.append('<h3 id="sec-%d-%d">' % (sec, sub) + inline(text, base) + "</h3>")
            else:
                out.append("<h4>" + inline(text, base) + "</h4>")
            continue

        if kind == "table":
            out.append(_table(rows, base))
            continue

        text = " ".join(rows)
        out.append("<p>" + inline(text, base) + "</p>")
        if details_open and faq:
            faq[-1]["a"] = (faq[-1]["a"] + " " + plain(text)).strip()

    close_faq()
    raw = LINK_RE.sub(r"\1", md).replace("{{B}}", "")
    return {
        "title": title,
        "html": "\n".join(out),
        "toc": toc,
        "faq": faq,
        "cjk": len(re.findall(r"[\u4e00-\u9fff]", raw)),
    }

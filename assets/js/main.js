/* 电磁阀.cn 官网交互脚本（无第三方依赖） */
(function () {
  'use strict';

  var EMAIL = '548827878@qq.com';

  /* ---------- 工具 ---------- */
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  var toastTimer;
  function toast(msg) {
    var el = $('.toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('is-show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove('is-show'); }, 2600);
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy') ? resolve() : reject(); }
      catch (e) { reject(e); }
      finally { document.body.removeChild(ta); }
    });
  }

  /* ---------- 移动端导航 ---------- */
  var toggle = $('.nav-toggle');
  var nav = $('.nav');
  if (toggle && nav) {
    toggle.setAttribute('aria-label', '展开导航菜单');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    $$('a', nav).forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- 复制邮箱 ---------- */
  $$('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy') || EMAIL;
      copyText(text).then(function () { toast('已复制：' + text); })
        .catch(function () { toast('复制失败，请手动复制：' + text); });
    });
  });

  /* ---------- 页脚年份 ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = String(new Date().getFullYear()); });

  /* ---------- 产品筛选与搜索 ---------- */
  var filterBtns = $$('.filter-btn');
  var searchInput = $('#product-search');
  var productCards = $$('.product-card[data-category]');
  var emptyTip = $('#filter-empty');

  function applyFilter() {
    if (!productCards.length) return;
    var active = $('.filter-btn.is-active');
    var cat = active ? active.getAttribute('data-filter') : 'all';
    var kw = (searchInput && searchInput.value || '').trim().toLowerCase();
    var shown = 0;
    productCards.forEach(function (card) {
      var okCat = cat === 'all' || card.getAttribute('data-category') === cat;
      var text = (card.getAttribute('data-keywords') || card.textContent).toLowerCase();
      var okKw = !kw || text.indexOf(kw) !== -1;
      card.style.display = (okCat && okKw) ? '' : 'none';
      if (okCat && okKw) shown++;
    });
    if (emptyTip) emptyTip.style.display = shown ? 'none' : 'block';
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      filterBtns.forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
      applyFilter();
    });
  });
  if (searchInput) searchInput.addEventListener('input', applyFilter);

  /* ---------- 询价表单 ---------- */
  var form = $('#inquiry-form');
  if (form) {
    // 支持从产品详情页带入型号：inquiry.html?model=2W160-15
    var params = new URLSearchParams(window.location.search);
    var preset = params.get('model') || params.get('domain');
    if (preset) {
      var modelField = form.elements['model'];
      if (modelField) modelField.value = preset;
      var noteField = form.elements['note'];
      if (noteField && params.get('domain') && !noteField.value) {
        noteField.value = '我想咨询域名购买：' + params.get('domain');
      }
    }

    function buildMail() {
      var v = function (name) {
        var el = form.elements[name];
        return el ? String(el.value || '').trim() : '';
      };
      var lines = [
        '【电磁阀.cn 询价 / 订购单】',
        '',
        '联系人：' + (v('name') || '未填写'),
        '公司名称：' + (v('company') || '未填写'),
        '联系电话：' + (v('phone') || '未填写'),
        '电子邮箱：' + (v('email') || '未填写'),
        '产品型号 / 数量：' + (v('model') || '未填写') + ' ／ ' + (v('qty') || '未填写'),
        '介质与工况：' + (v('medium') || '未填写'),
        '需求类型：' + (v('type') || '未填写'),
        '补充说明：',
        v('note') || '无',
        '',
        '（此邮件由询价页面自动生成，请核对后发送）'
      ];
      var subject = '询价/订购：' + (v('model') || '产品咨询') + ' - ' + (v('company') || v('name') || '客户');
      return {
        subject: subject,
        body: lines.join('\n'),
        mailto: 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'))
      };
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var mail = buildMail();
      window.location.href = mail.mailto;
      toast('已唤起邮件客户端，请核对后发送');
    });

    var copyBtn = $('#copy-inquiry');
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        if (!form.checkValidity()) { form.reportValidity(); return; }
        copyText(buildMail().body).then(function () { toast('询价单已复制，可直接粘贴到邮件或 QQ'); })
          .catch(function () { toast('复制失败，请手动选择文本'); });
      });
    }
  }

  /* ---------- 详情页询价按钮自动带型号 ---------- */
  $$('[data-inquiry-model]').forEach(function (a) {
    var base = a.getAttribute('href') || '';
    var model = a.getAttribute('data-inquiry-model');
    if (base.indexOf('?') === -1) a.setAttribute('href', base + '?model=' + encodeURIComponent(model));
  });

  /* ---------- 技术长文：当前章节目录高亮 ---------- */
  var tocLinks = $$('.article-toc li a');
  if (tocLinks.length) {
    var sections = tocLinks.map(function (a) {
      return document.getElementById((a.getAttribute('href') || '').slice(1));
    });
    var ticking = false;
    function updateToc() {
      ticking = false;
      var active = tocLinks[0];
      sections.forEach(function (el, i) {
        if (el && el.getBoundingClientRect().top <= 150) active = tocLinks[i];
      });
      tocLinks.forEach(function (a) { a.classList.toggle('is-current', a === active); });
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(updateToc); }
    }, { passive: true });
    window.addEventListener('resize', updateToc, { passive: true });
    updateToc();
  }

})();

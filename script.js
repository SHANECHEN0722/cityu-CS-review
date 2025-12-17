let allCourses = [];

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function getBasePath() {
  let basePath = window.location.origin + window.location.pathname;
  basePath = basePath.replace(/\/index\.html$/, '').replace(/\/$/, '');
  return basePath;
}

function buildFullUrl(filePath) {
  const encodedPath = String(filePath)
    .replace(/\\/g, '/')
    .split('/')
    .map((part) => encodeURIComponent(part))
    .join('/');
  return `${getBasePath()}/${encodedPath}`;
}

function syncCourseDetailHeaderLayout() {
  const header = document.querySelector('.course-detail-header');
  if (!header) return;
  const back = header.querySelector('.course-back');
  if (!back) return;

  const width = Math.ceil(back.getBoundingClientRect().width);
  header.style.setProperty('--side-width', `${width}px`);
}

async function loadData() {
  try {
    const response = await fetch('courses-data.json');
    if (!response.ok) throw new Error('无法加载 courses-data.json');
    const data = await response.json();

    allCourses = Array.isArray(data.courses) ? data.courses : [];
    document.getElementById('courseCount').textContent = data.courses_count || allCourses.length;
    displayCourses(allCourses);

    handleHashRoute();
  } catch (error) {
    console.error('加载数据失败:', error);
    document.getElementById('coursesGrid').innerHTML =
      '<div class="no-results"><span class="emoji">⚠️</span><p>加载课程数据失败</p><p style="font-size: 0.9em; margin-top: 10px;">请确保：<br>1. courses-data.json 存在<br>2. 用 HTTP 服务器访问（如 http://localhost:8000）<br>3. 不要用 file:// 打开本地文件</p></div>';
  }
}

function displayCourses(courses) {
  const grid = document.getElementById('coursesGrid');

  if (!courses.length) {
    grid.innerHTML = '<div class="no-results"><span class="emoji">🔍</span><p>未找到匹配的课程</p></div>';
    return;
  }

  grid.innerHTML = courses
    .map((course) => {
      const rawCode = String(course.code || '').trim();
      let rawName = String(course.name || course.folder || course.id || '').trim();
      if (rawCode && rawName.toLowerCase().startsWith(rawCode.toLowerCase())) {
        const rest = rawName.slice(rawCode.length).replace(/^[-_\s]+/, '');
        if (rest) rawName = rest;
      }
      const code = escapeHtml(rawCode);
      const name = escapeHtml(rawName);
      const id = escapeHtml(course.id || course.folder || '');
      return `
        <div class="course-card" data-course-id="${id}">
          <div class="course-code">${code}</div>
          <div class="course-name">${name}</div>
          <div class="course-link">查看详情 →</div>
        </div>
      `;
    })
    .join('');
}

function filterCourses(query) {
  const q = String(query || '').trim().toLowerCase();
  if (!q) {
    displayCourses(allCourses);
    return;
  }

  const filtered = allCourses.filter((course) => {
    const code = String(course.code || '').toLowerCase();
    const name = String(course.name || '').toLowerCase();
    const folder = String(course.folder || course.id || '').toLowerCase();
    return code.includes(q) || name.includes(q) || folder.includes(q);
  });

  displayCourses(filtered);
}

function countFiles(fileTree) {
  let count = 0;
  if (Array.isArray(fileTree.files)) count += fileTree.files.length;
  if (fileTree.folders) {
    for (const subfolder of Object.values(fileTree.folders)) {
      count += countFiles(subfolder);
    }
  }
  return count;
}

let folderIdCounter = 0;

function guessPreviewKind(fileName) {
  const ext = String(fileName).split('.').pop().toLowerCase();
  if (ext === 'pdf') return 'pdf';
  if (['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'].includes(ext)) return 'image';
  if (['mp4', 'webm', 'mov', 'avi', 'mkv'].includes(ext)) return 'video';
  if (['mp3', 'wav', 'flac', 'm4a'].includes(ext)) return 'audio';
  if (['pptx', 'ppt', 'docx', 'doc', 'xlsx', 'xls'].includes(ext)) return 'office';
  return 'file';
}

function officePreviewUrl(url) {
  return `https://view.officeapps.live.com/op/view.aspx?src=${encodeURIComponent(url)}`;
}

function buildFileTreeHTML(fileTree) {
  let html = '';

  if (fileTree.folders && Object.keys(fileTree.folders).length > 0) {
    for (const [name, subfolder] of Object.entries(fileTree.folders)) {
      const folderId = 'folder-' + folderIdCounter++;
      const fileCount = countFiles(subfolder);
      html += `
        <div class="folder-item" id="${folderId}">
          <div class="folder-header" data-toggle-folder="${folderId}">
            <span class="folder-icon">▼</span>
            <span>📁 ${escapeHtml(name)}</span>
            <span class="folder-count">${fileCount} 个文件</span>
          </div>
          <div class="folder-content">
            ${buildFileTreeHTML(subfolder)}
          </div>
        </div>
      `;
    }
  }

  if (Array.isArray(fileTree.files) && fileTree.files.length > 0) {
    html += `<ul class="file-list">`;
    for (const file of fileTree.files) {
      const href = buildFullUrl(file.path);
      const kind = guessPreviewKind(file.name);
      const safeName = escapeHtml(file.name);

      let icon = '📄';
      if (kind === 'pdf') icon = '📕';
      else if (kind === 'office') icon = '📝';
      else if (kind === 'image') icon = '🖼️';
      else if (kind === 'video') icon = '🎬';
      else if (kind === 'audio') icon = '🎵';

      let mainHref = href;
      let target = '_blank';
      let previewAttr = '';

      if (kind === 'office') {
        mainHref = officePreviewUrl(href);
      } else if (kind === 'image' || kind === 'video' || kind === 'audio') {
        previewAttr = `data-preview-kind="${kind}" data-preview-url="${escapeHtml(href)}" data-preview-name="${safeName}"`;
        target = '_self';
      }

      html += `
        <li class="file-item">
          <a href="${mainHref}" ${previewAttr} target="${target}" class="file-link">
            ${icon} ${safeName}
          </a>
          <a href="${href}" download class="download-link" title="下载文件">📥</a>
        </li>
      `;
    }
    html += `</ul>`;
  }

  return html;
}

function ensurePreviewModal() {
  let modal = document.getElementById('previewModal');
  if (modal) return modal;

  modal = document.createElement('div');
  modal.id = 'previewModal';
  modal.className = 'preview-modal hidden';
  modal.innerHTML = `
    <div class="preview-backdrop" data-preview-close="1"></div>
    <div class="preview-dialog" role="dialog" aria-modal="true">
      <div class="preview-header">
        <div class="preview-title" id="previewTitle"></div>
        <button class="preview-close" data-preview-close="1" aria-label="Close">×</button>
      </div>
      <div class="preview-body" id="previewBody"></div>
    </div>
  `;

  document.body.appendChild(modal);
  return modal;
}

function openPreview({ kind, url, name }) {
  const modal = ensurePreviewModal();
  const titleEl = modal.querySelector('#previewTitle');
  const bodyEl = modal.querySelector('#previewBody');

  titleEl.textContent = name || '';
  bodyEl.innerHTML = '';

  if (kind === 'pdf') {
    const iframe = document.createElement('iframe');
    iframe.className = 'preview-frame';
    iframe.src = url;
    iframe.loading = 'lazy';
    bodyEl.appendChild(iframe);
  } else if (kind === 'image') {
    const img = document.createElement('img');
    img.className = 'preview-image';
    img.src = url;
    img.alt = name || '';
    bodyEl.appendChild(img);
  } else if (kind === 'video') {
    const video = document.createElement('video');
    video.className = 'preview-video';
    video.src = url;
    video.controls = true;
    video.playsInline = true;
    bodyEl.appendChild(video);
  } else if (kind === 'audio') {
    const audio = document.createElement('audio');
    audio.className = 'preview-audio';
    audio.src = url;
    audio.controls = true;
    bodyEl.appendChild(audio);
  } else {
    const link = document.createElement('a');
    link.href = url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.className = 'course-link';
    link.textContent = '在新标签页打开';
    bodyEl.appendChild(link);
  }

  modal.classList.remove('hidden');
  document.body.classList.add('modal-open');
}

function closePreview() {
  const modal = document.getElementById('previewModal');
  if (!modal) return;
  modal.classList.add('hidden');
  const bodyEl = modal.querySelector('#previewBody');
  if (bodyEl) bodyEl.innerHTML = '';
  document.body.classList.remove('modal-open');
}

async function loadCourseIntro(course) {
  if (!course.intro_html) return null;
  const url = buildFullUrl(course.intro_html);

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('fetch failed');
    const text = await res.text();

    const parser = new DOMParser();
    const doc = parser.parseFromString(text, 'text/html');
    doc.querySelectorAll('script, style, link').forEach((el) => el.remove());

    const contentEl = doc.querySelector('.course-html') || doc.querySelector('main') || doc.body;
    if (!contentEl) return null;

    const wrapper = document.createElement('div');
    wrapper.innerHTML = contentEl.innerHTML;

    // Fix relative links/src inside embedded content
    const fixAttr = (selector, attr) => {
      wrapper.querySelectorAll(selector).forEach((el) => {
        const raw = el.getAttribute(attr);
        if (!raw) return;
        const v = raw.trim();
        if (!v) return;
        if (
          v.startsWith('#') ||
          v.startsWith('http://') ||
          v.startsWith('https://') ||
          v.startsWith('mailto:') ||
          v.startsWith('tel:') ||
          v.startsWith('data:') ||
          v.startsWith('javascript:') ||
          v.startsWith('/')
        ) {
          return;
        }
        try {
          const abs = new URL(v, url).href;
          el.setAttribute(attr, abs);
        } catch {
          // ignore
        }
      });
    };

    fixAttr('a[href]', 'href');
    fixAttr('img[src]', 'src');
    fixAttr('video[src]', 'src');
    fixAttr('audio[src]', 'src');
    fixAttr('source[src]', 'src');

    return wrapper.innerHTML;
  } catch (e) {
    console.warn('加载课程内容失败:', e);
    return null;
  }
}

async function showCourseDetail(courseId) {
  const course = allCourses.find((c) => (c.id || c.folder) === courseId);
  if (!course) return;

  folderIdCounter = 0;

  const title = `${course.code || ''}${course.name ? ' ' + course.name : ''}`.trim() || course.folder || course.id;
  const headerHTML = `
    <header class="course-detail-header">
      <a href="#" class="course-link course-back" data-back-to-list="1">← 返回列表</a>
      <h1 class="review-title"><span class="highlight">${escapeHtml(title)}</span></h1>
      <div class="course-detail-header-spacer" aria-hidden="true"></div>
    </header>
  `;

  const layoutHTML = `
    <div class="course-detail-layout">
      <section class="course-panel">
        <h2>📘 内容</h2>
        <div class="course-html" id="courseIntro">正在加载课程内容...</div>
      </section>
      <aside class="course-panel">
        <div class="course-panel-header">
          <h2>📂 资料</h2>
          <button class="course-link course-action-btn" type="button" data-download-zip="1">打包下载</button>
        </div>
        <div class="file-tree">
          ${course.files ? buildFileTreeHTML(course.files) : '<p class="muted">暂无资料</p>'}
        </div>
      </aside>
    </div>
  `;

  const courseDetailEl = document.getElementById('courseDetail');
  courseDetailEl.innerHTML = headerHTML + layoutHTML;
  courseDetailEl.dataset.currentCourseId = courseId;
  syncCourseDetailHeaderLayout();

  document.getElementById('listView').classList.add('hidden');
  document.getElementById('detailView').classList.add('active');
  document.getElementById('footerView').style.display = 'none';
  window.location.hash = `course=${encodeURIComponent(courseId)}`;
  window.scrollTo(0, 0);

  const introHTML = await loadCourseIntro(course);
  const introEl = document.getElementById('courseIntro');
  if (introEl) {
    introEl.innerHTML = introHTML || '<p class="muted">暂无课程内容</p>';
  }
}

function backToList() {
  document.getElementById('listView').classList.remove('hidden');
  document.getElementById('detailView').classList.remove('active');
  document.getElementById('footerView').style.display = 'block';
  if (window.location.hash) window.location.hash = '';
}

function handleHashRoute() {
  const hash = window.location.hash || '';
  if (!hash.startsWith('#course=')) return;
  const courseId = decodeURIComponent(hash.replace('#course=', ''));
  if (courseId) showCourseDetail(courseId);
}

function flattenFileEntries(tree, prefixParts = []) {
  const out = [];
  if (!tree) return out;

  if (tree.folders) {
    for (const [folderName, sub] of Object.entries(tree.folders)) {
      out.push(...flattenFileEntries(sub, [...prefixParts, folderName]));
    }
  }

  if (Array.isArray(tree.files)) {
    for (const file of tree.files) {
      out.push({ ...file, relativeName: [...prefixParts, file.name].join('/') });
    }
  }

  return out;
}

function downloadUrl(url, suggestedName) {
  const a = document.createElement('a');
  a.href = url;
  if (suggestedName) a.download = suggestedName;
  a.rel = 'noopener noreferrer';
  document.body.appendChild(a);
  a.click();
  a.remove();
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  downloadUrl(url, filename);
  setTimeout(() => URL.revokeObjectURL(url), 60_000);
}

let crcTable = null;

function getCrcTable() {
  if (crcTable) return crcTable;
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[n] = c >>> 0;
  }
  crcTable = table;
  return table;
}

function crc32(bytes) {
  const table = getCrcTable();
  let crc = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) {
    crc = table[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function makeLocalHeader(nameBytes, crc, size) {
  const header = new Uint8Array(30 + nameBytes.length);
  const dv = new DataView(header.buffer);
  dv.setUint32(0, 0x04034b50, true);
  dv.setUint16(4, 20, true); // version needed
  dv.setUint16(6, 0x0800, true); // UTF-8
  dv.setUint16(8, 0, true); // store
  dv.setUint16(10, 0, true); // time
  dv.setUint16(12, 0, true); // date
  dv.setUint32(14, crc, true);
  dv.setUint32(18, size, true);
  dv.setUint32(22, size, true);
  dv.setUint16(26, nameBytes.length, true);
  dv.setUint16(28, 0, true);
  header.set(nameBytes, 30);
  return header;
}

function makeCentralHeader(nameBytes, crc, size, localHeaderOffset) {
  const header = new Uint8Array(46 + nameBytes.length);
  const dv = new DataView(header.buffer);
  dv.setUint32(0, 0x02014b50, true);
  dv.setUint16(4, 20, true); // version made by
  dv.setUint16(6, 20, true); // version needed
  dv.setUint16(8, 0x0800, true); // UTF-8
  dv.setUint16(10, 0, true); // store
  dv.setUint16(12, 0, true); // time
  dv.setUint16(14, 0, true); // date
  dv.setUint32(16, crc, true);
  dv.setUint32(20, size, true);
  dv.setUint32(24, size, true);
  dv.setUint16(28, nameBytes.length, true);
  dv.setUint16(30, 0, true); // extra
  dv.setUint16(32, 0, true); // comment
  dv.setUint16(34, 0, true); // disk start
  dv.setUint16(36, 0, true); // internal attrs
  dv.setUint32(38, 0, true); // external attrs
  dv.setUint32(42, localHeaderOffset, true);
  header.set(nameBytes, 46);
  return header;
}

function makeEndOfCentralDirectory(entryCount, centralSize, centralOffset) {
  const eocd = new Uint8Array(22);
  const dv = new DataView(eocd.buffer);
  dv.setUint32(0, 0x06054b50, true);
  dv.setUint16(4, 0, true);
  dv.setUint16(6, 0, true);
  dv.setUint16(8, entryCount, true);
  dv.setUint16(10, entryCount, true);
  dv.setUint32(12, centralSize, true);
  dv.setUint32(16, centralOffset, true);
  dv.setUint16(20, 0, true);
  return eocd;
}

async function downloadCourseAsZip(course, buttonEl) {
  const entries = flattenFileEntries(course.files || {}).filter((f) => {
    const ext = String(f.name).split('.').pop().toLowerCase();
    return ext !== 'html';
  });

  if (!entries.length) {
    alert('暂无可下载资料');
    return;
  }

  const totalBytes = entries.reduce((sum, f) => sum + (Number(f.size) || 0), 0);
  const totalMB = Math.round((totalBytes / 1024 / 1024) * 10) / 10;
  const ok = confirm(
    `将打包 ${entries.length} 个文件（约 ${totalMB} MB）为 zip，并保留原始文件夹结构。\n\n这会在浏览器中逐个下载文件并打包，可能需要较长时间/占用较多内存。\n继续吗？`
  );
  if (!ok) return;

  const originalText = buttonEl ? buttonEl.textContent : '';
  if (buttonEl) buttonEl.disabled = true;

  const encoder = new TextEncoder();
  const zipRoot = [course.code, course.name]
    .map((v) => String(v || '').trim())
    .filter(Boolean)
    .join(' ')
    .trim()
    .replace(/[\\/]/g, '-')
    .replace(/\s{2,}/g, ' ')
    .replace(/^\.+/, '')
    .replace(/\.+$/, '') || String(course.folder || course.id || 'course').trim();
  const chunks = [];
  const centralHeaders = [];
  let offset = 0;

  try {
    for (let i = 0; i < entries.length; i++) {
      if (buttonEl) buttonEl.textContent = `打包中 ${i + 1}/${entries.length}`;

      const url = buildFullUrl(entries[i].path);
      const res = await fetch(url);
      if (!res.ok) throw new Error(`下载失败: ${entries[i].relativeName}`);

      const data = new Uint8Array(await res.arrayBuffer());
      const nameInZip = `${zipRoot}/${entries[i].relativeName}`;
      const nameBytes = encoder.encode(nameInZip);
      const fileCrc = crc32(data);

      const localHeaderOffset = offset;
      const localHeader = makeLocalHeader(nameBytes, fileCrc, data.length);
      chunks.push(localHeader);
      chunks.push(data);
      offset += localHeader.length + data.length;

      const central = makeCentralHeader(nameBytes, fileCrc, data.length, localHeaderOffset);
      centralHeaders.push(central);
    }

    const centralOffset = offset;
    for (const c of centralHeaders) {
      chunks.push(c);
      offset += c.length;
    }
    const centralSize = offset - centralOffset;
    const eocd = makeEndOfCentralDirectory(centralHeaders.length, centralSize, centralOffset);
    chunks.push(eocd);

    const blob = new Blob(chunks, { type: 'application/zip' });
    downloadBlob(blob, `${zipRoot}.zip`);
  } catch (e) {
    console.error(e);
    alert(`打包失败：${e && e.message ? e.message : '未知错误'}`);
  } finally {
    if (buttonEl) {
      buttonEl.textContent = originalText || '打包下载';
      buttonEl.disabled = false;
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => filterCourses(e.target.value));
  }

  const coursesGrid = document.getElementById('coursesGrid');
  if (coursesGrid) {
    coursesGrid.addEventListener('mousemove', (e) => {
      const cards = document.querySelectorAll('.course-card');
      cards.forEach((card) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--x', `${x}px`);
        card.style.setProperty('--y', `${y}px`);
      });
    });

    coursesGrid.addEventListener('click', (e) => {
      const card = e.target.closest('.course-card');
      if (!card) return;
      const courseId = card.getAttribute('data-course-id');
      if (courseId) showCourseDetail(courseId);
    });
  }

  const courseDetail = document.getElementById('courseDetail');
  if (courseDetail) {
    courseDetail.addEventListener('click', (e) => {
      const backLink = e.target.closest('[data-back-to-list]');
      if (backLink) {
        e.preventDefault();
        backToList();
        return;
      }

      const downloadZip = e.target.closest('[data-download-zip]');
      if (downloadZip) {
        e.preventDefault();
        const courseId = courseDetail.dataset.currentCourseId;
        const course = allCourses.find((c) => (c.id || c.folder) === courseId);
        if (course) downloadCourseAsZip(course, downloadZip);
        return;
      }

      const toggle = e.target.closest('[data-toggle-folder]');
      if (toggle) {
        const folderId = toggle.getAttribute('data-toggle-folder');
        const folder = document.getElementById(folderId);
        if (folder) folder.classList.toggle('collapsed');
        return;
      }

      const preview = e.target.closest('a[data-preview-kind]');
      if (preview) {
        e.preventDefault();
        openPreview({
          kind: preview.getAttribute('data-preview-kind'),
          url: preview.getAttribute('data-preview-url'),
          name: preview.getAttribute('data-preview-name'),
        });
      }
    });
  }

  window.addEventListener('hashchange', function () {
    if (!window.location.hash || window.location.hash === '#') {
      backToList();
      return;
    }
    handleHashRoute();
  });

  document.addEventListener('click', (e) => {
    const closeEl = e.target.closest('[data-preview-close]');
    if (closeEl) closePreview();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closePreview();
  });

  window.addEventListener('resize', () => {
    syncCourseDetailHeaderLayout();
  });
});

window.addEventListener('load', loadData);

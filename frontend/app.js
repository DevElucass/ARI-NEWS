const form = document.querySelector('#news-form');
const feed = document.querySelector('#feed');
const context = document.querySelector('#context');
const notice = document.querySelector('#notice');
const error = document.querySelector('#error');
const hero = document.querySelector('#hero');

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

function renderContext(data) {
  context.innerHTML = [
    `<span class="tag">${escapeHtml(data.sector)}</span>`,
    `<span class="tag">${escapeHtml(data.region)}</span>`,
    `<span class="tag tag--light">Data: ${escapeHtml(data.date)}</span>`,
  ].join('');
}

function renderNews(items) {
  feed.innerHTML = items.map((item, index) => `
    <article>
      <p class="index">${String(index + 1).padStart(2, '0')} / 03</p>
      <h2>${escapeHtml(item.title)}</h2>
      <p class="metadata">${escapeHtml(item.source)} · ${escapeHtml(item.published_date)}</p>
      <p>${escapeHtml(item.summary)}</p>
      <div class="links">
        <a href="${escapeHtml(item.original_url)}" target="_blank" rel="noreferrer">Acesse a Fonte →</a>
        <a href="${escapeHtml(item.google_search_url)}" target="_blank" rel="noreferrer">Buscar no Google →</a>
      </div>
    </article>
  `).join('');
}

async function loadNews() {
  const values = new URLSearchParams(new FormData(form));
  error.hidden = true;
  notice.hidden = true;
  const response = await fetch(`/api/news?${values.toString()}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Não foi possível carregar as notícias.');
  hero.src = data.hero_image;
  renderContext(data);
  notice.textContent = data.notice || '';
  notice.hidden = !data.notice;
  renderNews(data.news);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  try { await loadNews(); } catch (requestError) {
    feed.innerHTML = '';
    notice.hidden = true;
    error.textContent = requestError.message;
    error.hidden = false;
  }
});

loadNews().catch((requestError) => {
  notice.hidden = true;
  error.textContent = requestError.message;
  error.hidden = false;
});

/**
 * CelebrateAI — Cool & Classic Client Atelier
 */

// Global State
let currentEvent = null;
let allEvents = [];
let activeTimelineFilter = 'all';

// DOM Elements
const eventSelector = document.getElementById('eventSelector');
const btnOpenNewModal = document.getElementById('btnOpenNewModal');
const btnOpenSettings = document.getElementById('btnOpenSettings');
const btnPrintDossier = document.getElementById('btnPrintDossier');
const btnThemeToggle = document.getElementById('btnThemeToggle');
const themeIcon = document.getElementById('themeIcon');
const modalNewEvent = document.getElementById('modalNewEvent');
const modalSettings = document.getElementById('modalSettings');
const formNewEvent = document.getElementById('formNewEvent');
const inputApiKey = document.getElementById('inputApiKey');
const btnSaveApiKey = document.getElementById('btnSaveApiKey');
const loadingOverlay = document.getElementById('loadingOverlay');
const toastContainer = document.getElementById('toastContainer');

// Hero elements
const textEventTitle = document.getElementById('textEventTitle');
const textEventTagline = document.getElementById('textEventTagline');
const textLocation = document.getElementById('textLocation');
const badgeEventType = document.getElementById('badgeEventType');
const colorPaletteSwatches = document.getElementById('colorPaletteSwatches');
const paletteDescription = document.getElementById('paletteDescription');
const kpiBudget = document.getElementById('kpiBudget');
const kpiGuests = document.getElementById('kpiGuests');
const kpiDate = document.getElementById('kpiDate');
const kpiCountdown = document.getElementById('kpiCountdown');
const textAiSummary = document.getElementById('textAiSummary');
const heroAccentBar = document.getElementById('heroAccentBar');

// Budget elements
const budgetTotalCap = document.getElementById('budgetTotalCap');
const budgetTotalAllocated = document.getElementById('budgetTotalAllocated');
const budgetAllocatedPct = document.getElementById('budgetAllocatedPct');
const budgetTotalSpent = document.getElementById('budgetTotalSpent');
const budgetRemaining = document.getElementById('budgetRemaining');
const budgetBalanceStatus = document.getElementById('budgetBalanceStatus');
const budgetCategoryBar = document.getElementById('budgetCategoryBar');
const budgetLegend = document.getElementById('budgetLegend');
const budgetTableBody = document.getElementById('budgetTableBody');
const btnAutoRebalance = document.getElementById('btnAutoRebalance');
const btnAddBudgetItem = document.getElementById('btnAddBudgetItem');

// Timeline elements
const timelinePercentComplete = document.getElementById('timelinePercentComplete');
const tabBadgeTimelineProgress = document.getElementById('tabBadgeTimelineProgress');
const timelineContainer = document.getElementById('timelineContainer');
const btnAddTimelineItem = document.getElementById('btnAddTimelineItem');

// Vendor elements
const vendorsGrid = document.getElementById('vendorsGrid');
const btnAddVendor = document.getElementById('btnAddVendor');

// Ideas elements
const ideasGrid = document.getElementById('ideasGrid');
const customIdeaPrompt = document.getElementById('customIdeaPrompt');
const btnGenerateCustomIdeas = document.getElementById('btnGenerateCustomIdeas');

// Tab buttons
const tabButtons = document.querySelectorAll('.tab-btn-classic');
const tabContents = document.querySelectorAll('.tab-content');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSettings();
  setupEventListeners();
  loadAllEvents();
});

// ----------------------
// THEME & TOAST SYSTEM
// ----------------------
function initTheme() {
  const savedTheme = localStorage.getItem('celebrate_theme') || 'dark'; // Default to cool dark noir
  if (savedTheme === 'dark') {
    document.documentElement.classList.add('dark');
    themeIcon.textContent = '🌙';
  } else {
    document.documentElement.classList.remove('dark');
    themeIcon.textContent = '☀️';
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  const themeName = isDark ? 'dark' : 'light';
  localStorage.setItem('celebrate_theme', themeName);
  themeIcon.textContent = isDark ? '🌙' : '☀️';
  showToast(isDark ? 'Switched to Midnight Noir Mode' : 'Switched to Classic Ivory Mode', isDark ? '🌌' : '🏛️');
}

function showToast(message, icon = '✨') {
  if (!toastContainer) return;
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px) scale(0.95)';
    toast.style.transition = 'all 0.25s ease-out';
    setTimeout(() => toast.remove(), 250);
  }, 2800);
}

function initSettings() {
  const savedKey = localStorage.getItem('gemini_api_key') || '';
  if (inputApiKey) inputApiKey.value = savedKey;
}

function setupEventListeners() {
  // Theme Toggle
  if (btnThemeToggle) btnThemeToggle.addEventListener('click', toggleTheme);

  // Tabs
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      tabButtons.forEach(b => {
        b.classList.remove('active');
        b.classList.add('text-[var(--text-muted)]');
      });
      btn.classList.add('active');
      btn.classList.remove('text-[var(--text-muted)]');

      tabContents.forEach(c => c.classList.add('hidden'));
      const activePanel = document.getElementById(targetTab);
      if (activePanel) activePanel.classList.remove('hidden');
    });
  });

  // Event Switcher
  eventSelector.addEventListener('change', (e) => {
    selectEventById(e.target.value);
  });

  // Modals
  btnOpenNewModal.addEventListener('click', () => modalNewEvent.classList.remove('hidden'));
  btnOpenSettings.addEventListener('click', () => modalSettings.classList.remove('hidden'));
  btnPrintDossier.addEventListener('click', () => window.print());

  document.querySelectorAll('.btnCloseModal').forEach(btn => {
    btn.addEventListener('click', () => {
      modalNewEvent.classList.add('hidden');
      modalSettings.classList.add('hidden');
    });
  });

  // Save Settings
  btnSaveApiKey.addEventListener('click', () => {
    const key = inputApiKey.value.trim();
    localStorage.setItem('gemini_api_key', key);
    modalSettings.classList.add('hidden');
    showToast(key ? 'Gemini API Key activated for live reasoning' : 'Running in local high-fidelity heuristic mode', '🔑');
  });

  // Preset Vibe Chips
  document.querySelectorAll('.preset-vibe').forEach(chip => {
    chip.addEventListener('click', () => {
      document.getElementById('newThemeVibe').value = chip.textContent;
    });
  });

  // Create Event Form
  formNewEvent.addEventListener('submit', handleCreateEvent);

  // Budget Actions
  btnAutoRebalance.addEventListener('click', handleAutoRebalance);
  btnAddBudgetItem.addEventListener('click', handleAddBudgetItem);

  // Timeline filters
  document.querySelectorAll('.timeline-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.timeline-filter-btn').forEach(b => {
        b.classList.remove('active', 'bg-[var(--bg-card)]', 'text-[var(--text-main)]', 'shadow-xs');
        b.classList.add('text-[var(--text-muted)]');
      });
      btn.classList.add('active', 'bg-[var(--bg-card)]', 'text-[var(--text-main)]', 'shadow-xs');
      btn.classList.remove('text-[var(--text-muted)]');
      activeTimelineFilter = btn.getAttribute('data-timeline-filter');
      renderTimeline();
    });
  });

  btnAddTimelineItem.addEventListener('click', handleAddTimelineItem);
  btnAddVendor.addEventListener('click', handleAddVendor);

  // Ideas Generation
  btnGenerateCustomIdeas.addEventListener('click', handleGenerateCustomIdeas);
  document.querySelectorAll('.quick-prompt').forEach(qp => {
    qp.addEventListener('click', () => {
      customIdeaPrompt.value = qp.getAttribute('data-prompt');
      handleGenerateCustomIdeas();
    });
  });
}

// Fetch all events
async function loadAllEvents() {
  try {
    const res = await fetch('/api/events');
    allEvents = await res.json();
    populateEventSelector();
    if (allEvents.length > 0) {
      selectEventById(allEvents[0].id);
    }
  } catch (err) {
    console.error('Failed to load events:', err);
    showToast('Failed to load event plans', '⚠️');
  }
}

function populateEventSelector() {
  eventSelector.innerHTML = '';
  allEvents.forEach(evt => {
    const opt = document.createElement('option');
    opt.value = evt.id;
    const icon = evt.event_type === 'wedding' ? '💍' : evt.event_type === 'birthday' ? '🎂' : '🌳';
    opt.textContent = `${icon} ${evt.title}`;
    eventSelector.appendChild(opt);
  });
}

function selectEventById(id) {
  const found = allEvents.find(e => e.id === id);
  if (found) {
    currentEvent = found;
    eventSelector.value = id;
    renderFullEvent();
  }
}

// Render everything
function renderFullEvent() {
  if (!currentEvent) return;

  renderHero();
  renderBudget();
  renderTimeline();
  renderVendors();
  renderIdeas();
}

function renderHero() {
  const e = currentEvent;
  textEventTitle.textContent = e.title;
  textEventTagline.textContent = `"${e.tagline || e.theme_vibe}"`;
  textLocation.textContent = e.location || 'Location TBD';

  // Badge icon
  const icon = e.event_type === 'wedding' ? '💍 Wedding Collection' : e.event_type === 'birthday' ? '🎂 Milestone Soiree' : '🌳 Civic Gathering';
  badgeEventType.textContent = icon;

  // Palette
  const p = e.color_palette || {};
  heroAccentBar.style.background = `linear-gradient(to right, ${p.primary || '#D4AF37'}, ${p.secondary || '#854D0E'}, ${p.accent || '#D97706'})`;
  paletteDescription.textContent = p.description || 'Custom Aesthetic';

  colorPaletteSwatches.innerHTML = '';
  [p.primary, p.secondary, p.accent, p.neutral].filter(Boolean).forEach(color => {
    const s = document.createElement('div');
    s.className = 'w-6 h-6 rounded-full border border-[var(--border-main)] shadow-xs cursor-pointer hover:scale-115 transition transform';
    s.style.backgroundColor = color;
    s.title = `Click to copy ${color}`;
    s.onclick = () => {
      navigator.clipboard.writeText(color);
      showToast(`Copied ${color} to clipboard`, '🎨');
    };
    colorPaletteSwatches.appendChild(s);
  });

  // KPIs
  const cur = e.currency || '$';
  kpiBudget.textContent = `${cur}${e.total_budget.toLocaleString()}`;
  kpiGuests.textContent = `${e.guest_count} Attendees`;

  if (e.date) {
    const d = new Date(e.date);
    kpiDate.textContent = isNaN(d.getTime()) ? e.date : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
    const diffDays = Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
    kpiCountdown.textContent = diffDays > 0 ? `${diffDays} Days Ahead` : diffDays === 0 ? 'Today' : 'Completed';
  } else {
    kpiDate.textContent = 'Date Flexible';
    kpiCountdown.textContent = 'In Curation';
  }

  textAiSummary.textContent = e.ai_summary_and_tips || 'Safeguard your contingency buffer for unexpected overtime and weather adjustments.';

  // Badges count on tabs
  document.getElementById('tabBadgeBudgetCount').textContent = e.budget_items.length;
  document.getElementById('tabBadgeVendorCount').textContent = e.vendor_checklist.length;
  document.getElementById('tabBadgeIdeaCount').textContent = e.personalized_ideas.length;
}

// ----------------------
// BUDGET LOGIC & RENDER
// ----------------------
function renderBudget() {
  const e = currentEvent;
  const cur = e.currency || '$';
  const totalCap = e.total_budget;

  let totalAllocated = 0;
  let totalSpent = 0;
  const categoryTotals = {};

  e.budget_items.forEach(item => {
    totalAllocated += Number(item.allocated_amount) || 0;
    totalSpent += Number(item.actual_amount) || 0;
    categoryTotals[item.category] = (categoryTotals[item.category] || 0) + Number(item.allocated_amount);
  });

  const remaining = totalCap - totalSpent;
  const pctAllocated = Math.round((totalAllocated / (totalCap || 1)) * 100);

  budgetTotalCap.textContent = `${cur}${totalCap.toLocaleString()}`;
  budgetTotalAllocated.textContent = `${cur}${totalAllocated.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
  budgetAllocatedPct.textContent = `${pctAllocated}% of ceiling`;
  budgetTotalSpent.textContent = `${cur}${totalSpent.toLocaleString()}`;
  budgetRemaining.textContent = `${cur}${remaining.toLocaleString()}`;

  // Contingency calculation
  const contingencyItem = e.budget_items.find(i => i.category.toLowerCase().includes('contingency'));
  if (contingencyItem) {
    document.getElementById('budgetContingencyLabel').textContent = `Includes ${cur}${contingencyItem.allocated_amount.toLocaleString()} contingency buffer`;
  }

  // Balance status
  if (Math.abs(totalCap - totalAllocated) < 1) {
    budgetBalanceStatus.className = 'text-emerald-600 flex items-center gap-1.5 font-bold';
    budgetBalanceStatus.innerHTML = `<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Balanced at 100%`;
  } else if (totalAllocated > totalCap) {
    const over = totalAllocated - totalCap;
    budgetBalanceStatus.className = 'text-rose-600 flex items-center gap-1.5 font-bold';
    budgetBalanceStatus.innerHTML = `⚠️ Exceeds ceiling by ${cur}${over.toLocaleString()}`;
  } else {
    const under = totalCap - totalAllocated;
    budgetBalanceStatus.className = 'text-amber-600 dark:text-amber-400 flex items-center gap-1.5 font-medium';
    budgetBalanceStatus.innerHTML = `Unallocated reserve: ${cur}${under.toLocaleString()}`;
  }

  // Visual Category Distribution Bar
  budgetCategoryBar.innerHTML = '';
  budgetLegend.innerHTML = '';
  const colors = ['#D4AF37', '#9A7B38', '#10B981', '#06B6D4', '#8B5CF6', '#EC4899', '#F97316', '#64748B'];
  let colorIdx = 0;

  Object.entries(categoryTotals).forEach(([cat, amount]) => {
    const pct = ((amount / (totalAllocated || 1)) * 100).toFixed(1);
    const color = colors[colorIdx % colors.length];
    colorIdx++;

    const seg = document.createElement('div');
    seg.style.width = `${pct}%`;
    seg.style.backgroundColor = color;
    seg.title = `${cat}: ${cur}${amount.toLocaleString()} (${pct}%)`;
    budgetCategoryBar.appendChild(seg);

    const leg = document.createElement('div');
    leg.className = 'flex items-center gap-1.5';
    leg.innerHTML = `<span class="w-2.5 h-2.5 rounded-full" style="background-color: ${color}"></span><span>${cat} <strong class="text-[var(--text-main)]">${pct}%</strong></span>`;
    budgetLegend.appendChild(leg);
  });

  // Table rows
  budgetTableBody.innerHTML = '';
  e.budget_items.forEach((item, index) => {
    const tr = document.createElement('tr');
    tr.className = 'hover:bg-[var(--bg-card-subtle)] transition';

    tr.innerHTML = `
      <td class="py-3 px-5">
        <div class="font-bold text-[var(--text-main)]">${item.name}</div>
        <span class="text-[10px] px-2 py-0.5 rounded-full badge-gold font-semibold uppercase tracking-wider">${item.category}</span>
      </td>
      <td class="py-3 px-4">
        <select class="text-xs border border-[var(--border-main)] rounded-lg px-2.5 py-1 bg-[var(--bg-card)] text-[var(--text-main)] status-select font-medium" data-index="${index}">
          <option value="estimated" ${item.status === 'estimated' ? 'selected' : ''}>Estimated</option>
          <option value="quoted" ${item.status === 'quoted' ? 'selected' : ''}>Quoted</option>
          <option value="booked" ${item.status === 'booked' ? 'selected' : ''}>Booked</option>
          <option value="paid" ${item.status === 'paid' ? 'selected' : ''}>Paid in Full</option>
        </select>
      </td>
      <td class="py-3 px-4 text-right">
        <div class="flex items-center justify-end gap-1">
          <span class="text-[var(--text-muted)]">${cur}</span>
          <input type="number" step="50" class="w-24 text-right font-bold text-[var(--text-main)] border border-[var(--border-main)] bg-[var(--bg-card)] rounded-lg px-2 py-1 text-xs allocated-input focus:border-amber-500" value="${item.allocated_amount}" data-index="${index}">
        </div>
      </td>
      <td class="py-3 px-4 text-right">
        <div class="flex items-center justify-end gap-1">
          <span class="text-[var(--text-muted)]">${cur}</span>
          <input type="number" step="50" class="w-24 text-right font-semibold text-emerald-600 border border-[var(--border-main)] bg-[var(--bg-card)] rounded-lg px-2 py-1 text-xs spent-input focus:border-amber-500" value="${item.actual_amount}" data-index="${index}">
        </div>
      </td>
      <td class="py-3 px-5 text-[var(--text-muted)] text-xs max-w-xs truncate" title="${item.notes || ''}">
        ${item.notes || '-'}
      </td>
      <td class="py-3 px-4 text-right">
        <button class="text-[var(--text-subtle)] hover:text-rose-600 p-1 delete-budget-btn transition" data-index="${index}" title="Remove item">
          ✕
        </button>
      </td>
    `;
    budgetTableBody.appendChild(tr);
  });

  // Attach table events
  budgetTableBody.querySelectorAll('.allocated-input').forEach(input => {
    input.addEventListener('change', (e) => {
      const idx = e.target.getAttribute('data-index');
      currentEvent.budget_items[idx].allocated_amount = parseFloat(e.target.value) || 0;
      saveCurrentEvent();
      renderBudget();
    });
  });

  budgetTableBody.querySelectorAll('.spent-input').forEach(input => {
    input.addEventListener('change', (e) => {
      const idx = e.target.getAttribute('data-index');
      currentEvent.budget_items[idx].actual_amount = parseFloat(e.target.value) || 0;
      saveCurrentEvent();
      renderBudget();
    });
  });

  budgetTableBody.querySelectorAll('.status-select').forEach(sel => {
    sel.addEventListener('change', (e) => {
      const idx = e.target.getAttribute('data-index');
      currentEvent.budget_items[idx].status = e.target.value;
      saveCurrentEvent();
    });
  });

  budgetTableBody.querySelectorAll('.delete-budget-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = btn.getAttribute('data-index');
      currentEvent.budget_items.splice(idx, 1);
      saveCurrentEvent();
      renderBudget();
      showToast('Line item removed', '🗑️');
    });
  });
}

// Auto-Rebalance proportionally
function handleAutoRebalance() {
  const e = currentEvent;
  const targetCap = e.total_budget;
  let currentTotal = e.budget_items.reduce((sum, item) => sum + (Number(item.allocated_amount) || 0), 0);

  if (currentTotal === 0) return;

  const ratio = targetCap / currentTotal;
  e.budget_items.forEach(item => {
    item.allocated_amount = Math.round((Number(item.allocated_amount) * ratio) / 10) * 10;
  });

  saveCurrentEvent();
  renderBudget();
  showToast('Budget proportionally rebalanced to 100%', '⚖️');
}

function handleAddBudgetItem() {
  const name = prompt('Line item designation (e.g. String Quartet, Late-Night Woodfired Pizza):');
  if (!name) return;
  const category = prompt('Category (e.g. Venue, Catering, Media, Decor, Entertainment):') || 'General';
  const amount = parseFloat(prompt('Allocated capital ($):', '750')) || 750;

  currentEvent.budget_items.push({
    id: 'bgt-' + Math.random().toString(36).substring(2, 8),
    category,
    name,
    allocated_amount: amount,
    actual_amount: 0,
    status: 'estimated',
    notes: 'Custom organizer line item'
  });

  saveCurrentEvent();
  renderBudget();
  showToast('New item added to ledger', '➕');
}

// ----------------------
// TIMELINE LOGIC & RENDER
// ----------------------
function renderTimeline() {
  const e = currentEvent;
  const tasks = e.timeline_items || [];

  const completedCount = tasks.filter(t => t.is_completed).length;
  const pct = tasks.length > 0 ? Math.round((completedCount / tasks.length) * 100) : 0;

  timelinePercentComplete.textContent = `${pct}% Complete (${completedCount}/${tasks.length})`;
  tabBadgeTimelineProgress.textContent = `${pct}%`;

  // Group by Phase
  const phases = {};
  tasks.forEach((task, idx) => {
    if (activeTimelineFilter === 'pending' && task.is_completed) return;
    if (activeTimelineFilter === 'completed' && !task.is_completed) return;

    const p = task.phase || 'Master Milestones';
    if (!phases[p]) phases[p] = [];
    phases[p].push({ task, originalIndex: idx });
  });

  timelineContainer.innerHTML = '';

  if (Object.keys(phases).length === 0) {
    timelineContainer.innerHTML = `
      <div class="classic-card p-10 rounded-2xl text-center text-[var(--text-muted)] font-serif-luxury italic">
        No milestones match the selected filter.
      </div>
    `;
    return;
  }

  Object.entries(phases).forEach(([phaseName, phaseTasks]) => {
    const phaseBox = document.createElement('div');
    phaseBox.className = 'classic-card rounded-2xl overflow-hidden';

    let taskRowsHtml = '';
    phaseTasks.forEach(({ task, originalIndex }) => {
      const priorityColor = task.priority === 'high' ? 'bg-rose-500/10 text-rose-600 border-rose-500/30' :
                            task.priority === 'medium' ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30' :
                            'bg-slate-500/10 text-slate-500 border-slate-500/30';

      taskRowsHtml += `
        <div class="p-4 sm:p-5 flex items-start gap-4 hover:bg-[var(--bg-card-subtle)] transition border-b border-[var(--border-main)] last:border-0 ${task.is_completed ? 'opacity-50' : ''}">
          <input type="checkbox" class="mt-1 w-4 h-4 rounded text-amber-600 border-[var(--border-main)] focus:ring-amber-500 timeline-check cursor-pointer" data-index="${originalIndex}" ${task.is_completed ? 'checked' : ''}>
          
          <div class="flex-1 space-y-1">
            <div class="flex flex-wrap items-center gap-2.5">
              <span class="font-bold text-sm ${task.is_completed ? 'line-through text-[var(--text-muted)]' : 'text-[var(--text-main)]'}">${task.title}</span>
              <span class="text-[9px] px-2 py-0.5 rounded-full font-bold border ${priorityColor} uppercase tracking-wider">${task.priority}</span>
              <span class="text-xs text-[var(--text-muted)] font-medium">⏱️ ${task.timeframe}</span>
            </div>
            <p class="text-xs text-[var(--text-muted)] leading-relaxed">${task.description}</p>
            <div class="text-[11px] text-[var(--text-subtle)]">Director: <strong class="text-[var(--text-main)]">${task.assigned_to || 'Organizer'}</strong></div>
          </div>

          <button class="text-[var(--text-subtle)] hover:text-rose-600 p-1 delete-timeline-btn transition" data-index="${originalIndex}">✕</button>
        </div>
      `;
    });

    phaseBox.innerHTML = `
      <div class="bg-[var(--bg-card-subtle)] px-6 py-3.5 border-b border-[var(--border-main)] flex items-center justify-between">
        <h4 class="font-serif-luxury font-bold text-sm tracking-wide text-[var(--text-main)] flex items-center gap-2">
          <span>🚩</span> ${phaseName}
        </h4>
        <span class="text-xs text-[var(--text-muted)] font-medium">${phaseTasks.length} Milestones</span>
      </div>
      <div>${taskRowsHtml}</div>
    `;

    timelineContainer.appendChild(phaseBox);
  });

  // Attach event listeners
  timelineContainer.querySelectorAll('.timeline-check').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const idx = e.target.getAttribute('data-index');
      currentEvent.timeline_items[idx].is_completed = e.target.checked;
      saveCurrentEvent();
      renderTimeline();
      showToast(e.target.checked ? 'Milestone achieved' : 'Milestone reopened', e.target.checked ? '✅' : '⏳');
    });
  });

  timelineContainer.querySelectorAll('.delete-timeline-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = btn.getAttribute('data-index');
      currentEvent.timeline_items.splice(idx, 1);
      saveCurrentEvent();
      renderTimeline();
      showToast('Task removed from roadmap', '🗑️');
    });
  });
}

function handleAddTimelineItem() {
  const title = prompt('Milestone action title:');
  if (!title) return;
  const phase = prompt('Phase (e.g. Phase 1: Foundation, Phase 3: Details, Day-Of Run of Show):') || 'Master Milestones';
  const timeframe = prompt('Timeframe (e.g. 6 Months Out or 03:00 PM):') || 'Upcoming';
  const desc = prompt('Detailed instructions:') || '';

  currentEvent.timeline_items.push({
    id: 'tml-' + Math.random().toString(36).substring(2, 8),
    phase,
    timeframe,
    title,
    description: desc,
    is_completed: false,
    priority: 'medium',
    assigned_to: 'Organizer'
  });

  saveCurrentEvent();
  renderTimeline();
  showToast('New milestone added to roadmap', '🚩');
}

// ----------------------
// VENDOR CRM & INTERVIEW
// ----------------------
function renderVendors() {
  const e = currentEvent;
  const cur = e.currency || '$';
  vendorsGrid.innerHTML = '';

  e.vendor_checklist.forEach((v, index) => {
    const card = document.createElement('div');
    card.className = 'classic-card rounded-2xl p-6 space-y-4';

    let questionsHtml = '';
    if (v.key_questions_to_ask && v.key_questions_to_ask.length > 0) {
      questionsHtml = `
        <div class="mt-3 pt-3 border-t border-[var(--border-main)]">
          <details class="group cursor-pointer">
            <summary class="text-xs font-bold text-amber-600 dark:text-amber-400 flex items-center justify-between">
              <span class="flex items-center gap-1.5 font-serif-luxury text-[13px]">
                <span>🧠</span> Expert Interview Protocol (${v.key_questions_to_ask.length})
              </span>
              <span class="text-[var(--text-muted)] group-open:rotate-180 transition-transform">▼</span>
            </summary>
            <ul class="mt-2.5 space-y-2 pl-4 list-disc text-xs text-[var(--text-muted)] leading-relaxed">
              ${v.key_questions_to_ask.map(q => `<li>${q}</li>`).join('')}
            </ul>
          </details>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="flex items-start justify-between gap-3">
        <div>
          <span class="text-[9px] font-bold uppercase tracking-wider badge-gold px-2.5 py-0.5 rounded-full">${v.category}</span>
          <h4 class="font-serif-luxury font-bold text-lg text-[var(--text-main)] mt-1.5">${v.name}</h4>
        </div>
        <select class="text-xs border border-[var(--border-main)] rounded-full px-3 py-1 bg-[var(--bg-card-subtle)] text-[var(--text-main)] font-semibold vendor-status-select" data-index="${index}">
          <option value="to_contact" ${v.status === 'to_contact' ? 'selected' : ''}>To Contact</option>
          <option value="proposal_received" ${v.status === 'proposal_received' ? 'selected' : ''}>Proposal In Hand</option>
          <option value="negotiating" ${v.status === 'negotiating' ? 'selected' : ''}>Negotiating</option>
          <option value="booked" ${v.status === 'booked' ? 'selected' : ''}>Booked & Confirmed</option>
          <option value="paid_in_full" ${v.status === 'paid_in_full' ? 'selected' : ''}>Paid in Full</option>
        </select>
      </div>

      <div class="grid grid-cols-2 gap-3 text-xs bg-[var(--bg-card-subtle)] p-3 rounded-xl border border-[var(--border-main)]">
        <div>
          <span class="text-[var(--text-muted)]">Contracted:</span>
          <strong class="text-[var(--text-main)] ml-1">${cur}${v.estimated_cost.toLocaleString()}</strong>
        </div>
        <div>
          <span class="text-[var(--text-muted)]">Deposit Paid:</span>
          <strong class="text-emerald-600 ml-1">${cur}${v.deposit_paid.toLocaleString()}</strong>
        </div>
      </div>

      <div class="flex items-center justify-between text-xs pt-1">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="checkbox" class="w-4 h-4 rounded text-amber-600 border-[var(--border-main)] vendor-contract-check" data-index="${index}" ${v.contract_signed ? 'checked' : ''}>
          <span class="text-[var(--text-main)] font-medium">Contract Counter-Signed</span>
        </label>
        
        <div class="flex items-center gap-3 text-[var(--text-muted)]">
          ${v.contact_email ? `<a href="mailto:${v.contact_email}" class="hover:text-amber-500" title="Email partner">✉️</a>` : ''}
          ${v.contact_phone ? `<a href="tel:${v.contact_phone}" class="hover:text-amber-500" title="Call partner">📞</a>` : ''}
          <button class="text-[var(--text-subtle)] hover:text-rose-600 delete-vendor-btn" data-index="${index}" title="Remove vendor">✕</button>
        </div>
      </div>

      ${questionsHtml}
    `;

    vendorsGrid.appendChild(card);
  });

  // Attach vendor events
  vendorsGrid.querySelectorAll('.vendor-status-select').forEach(sel => {
    sel.addEventListener('change', (e) => {
      const idx = e.target.getAttribute('data-index');
      currentEvent.vendor_checklist[idx].status = e.target.value;
      saveCurrentEvent();
      showToast('Vendor status updated', '🤝');
    });
  });

  vendorsGrid.querySelectorAll('.vendor-contract-check').forEach(cb => {
    cb.addEventListener('change', (e) => {
      const idx = e.target.getAttribute('data-index');
      currentEvent.vendor_checklist[idx].contract_signed = e.target.checked;
      saveCurrentEvent();
      showToast(e.target.checked ? 'Contract marked as signed' : 'Contract marked unsigned', '✍️');
    });
  });

  vendorsGrid.querySelectorAll('.delete-vendor-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = btn.getAttribute('data-index');
      currentEvent.vendor_checklist.splice(idx, 1);
      saveCurrentEvent();
      renderVendors();
      showToast('Vendor removed from directory', '🗑️');
    });
  });
}

function handleAddVendor() {
  const name = prompt('Vendor / Artisan Name:');
  if (!name) return;
  const category = prompt('Category (e.g. Photography, Catering, Florals, Music):') || 'Partner';
  const cost = parseFloat(prompt('Estimated Cost ($):', '1500')) || 0;

  currentEvent.vendor_checklist.push({
    id: 'vnd-' + Math.random().toString(36).substring(2, 8),
    category,
    name,
    status: 'to_contact',
    estimated_cost: cost,
    contract_signed: false,
    deposit_paid: 0,
    balance_due: cost,
    contact_email: '',
    contact_phone: '',
    key_questions_to_ask: [
      'What are your exact load-in and teardown time boundaries?',
      'What are the overtime fees if speeches run 30 minutes over schedule?',
      'Do you carry active commercial general liability coverage?'
    ],
    notes: ''
  });

  saveCurrentEvent();
  renderVendors();
  showToast('Partner added to directory', '🤝');
}

// ----------------------
// PERSONALIZED IDEAS
// ----------------------
function renderIdeas() {
  const e = currentEvent;
  ideasGrid.innerHTML = '';

  e.personalized_ideas.forEach((idea, index) => {
    const card = document.createElement('div');
    card.className = 'classic-card rounded-2xl p-6 space-y-4 flex flex-col justify-between';

    card.innerHTML = `
      <div class="space-y-2.5">
        <div class="flex items-center justify-between gap-2">
          <span class="text-[10px] font-bold uppercase tracking-wider text-[var(--text-muted)]">${idea.category}</span>
          <div class="flex items-center gap-1.5">
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold border border-amber-500/30 bg-amber-500/10 text-amber-600 dark:text-amber-400">${idea.cost_level}</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full font-bold border border-pink-500/30 bg-pink-500/10 text-pink-600">${idea.impact_level}</span>
          </div>
        </div>
        <h4 class="font-serif-luxury font-bold text-base text-[var(--text-main)] leading-snug">${idea.title}</h4>
        <p class="text-xs text-[var(--text-muted)] leading-relaxed">${idea.description}</p>
      </div>

      <div class="pt-3 border-t border-[var(--border-main)] flex items-center justify-between text-xs text-[var(--text-subtle)]">
        <span class="font-serif-luxury italic">Atelier Concept</span>
        <button class="hover:text-rose-600 delete-idea-btn transition" data-index="${index}">✕</button>
      </div>
    `;

    ideasGrid.appendChild(card);
  });

  ideasGrid.querySelectorAll('.delete-idea-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = btn.getAttribute('data-index');
      currentEvent.personalized_ideas.splice(idx, 1);
      saveCurrentEvent();
      renderIdeas();
      showToast('Concept removed from moodboard', '🗑️');
    });
  });
}

// Brainstorm more ideas
async function handleGenerateCustomIdeas() {
  const prompt = customIdeaPrompt.value.trim();
  if (!prompt) return;

  btnGenerateCustomIdeas.disabled = true;
  btnGenerateCustomIdeas.textContent = 'Curating...';

  try {
    const res = await fetch(`/api/events/${currentEvent.id}/ideas/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_type: currentEvent.event_type,
        title: currentEvent.title,
        theme_vibe: currentEvent.theme_vibe,
        prompt: prompt,
        api_key: localStorage.getItem('gemini_api_key') || null
      })
    });

    const newIdeas = await res.json();
    currentEvent.personalized_ideas.push(...newIdeas);
    renderIdeas();
    customIdeaPrompt.value = '';
    showToast(`Curated ${newIdeas.length} fresh bespoke concepts!`, '✨');
  } catch (err) {
    alert('Failed to generate custom ideas: ' + err.message);
  } finally {
    btnGenerateCustomIdeas.disabled = false;
    btnGenerateCustomIdeas.innerHTML = `<span>✨</span> Brainstorm`;
  }
}

// ----------------------
// CREATE NEW EVENT
// ----------------------
async function handleCreateEvent(e) {
  e.preventDefault();

  const eventType = document.querySelector('input[name="newEventType"]:checked').value;
  const title = document.getElementById('newTitle').value.trim();
  const location = document.getElementById('newLocation').value.trim() || 'Local Setting';
  const guestCount = parseInt(document.getElementById('newGuestCount').value) || 50;
  const totalBudget = parseFloat(document.getElementById('newBudget').value) || 10000;
  const currency = document.getElementById('newCurrency').value;
  const themeVibe = document.getElementById('newThemeVibe').value.trim();
  const specialNotes = document.getElementById('newNotes').value.trim();

  modalNewEvent.classList.add('hidden');
  loadingOverlay.classList.remove('hidden');

  try {
    const res = await fetch('/api/events/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event_type: eventType,
        title: title,
        location: location,
        guest_count: guestCount,
        total_budget: totalBudget,
        currency: currency,
        theme_vibe: themeVibe,
        special_notes: specialNotes,
        api_key: localStorage.getItem('gemini_api_key') || null
      })
    });

    if (!res.ok) throw new Error('Generation failed');
    const newPlan = await res.json();

    allEvents.unshift(newPlan);
    populateEventSelector();
    selectEventById(newPlan.id);
    showToast(`Master blueprint for "${newPlan.title}" curated!`, '🍾');
  } catch (err) {
    alert('Error generating plan: ' + err.message);
  } finally {
    loadingOverlay.classList.add('hidden');
  }
}

// Save Current Event to Backend
async function saveCurrentEvent() {
  if (!currentEvent) return;
  try {
    await fetch(`/api/events/${currentEvent.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentEvent)
    });
  } catch (err) {
    console.error('Failed to save update:', err);
  }
}

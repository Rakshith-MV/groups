    // import * as THREE from 'three';
// import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// import { DragControls } from 'three/addons/controls/DragControls.js';

// Define styles before they're used
const styles = `
    .info-card {
        background: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        z-index: 1000;
    }

    .info-card-content {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        gap: 16px;
    }

    .info-label {
        font-weight: bold;
    }

    #tableView {
        height: 100%;
        position: relative;
    }

    #graphCanvas {
        position: absolute;
        top: 0;
        left: 0;
    }
`;


function showInfoCard(event, inverse, order) {
    // Remove any existing cards first
    const existingCard = document.querySelector('.info-card');
    if (existingCard) {
        existingCard.remove();
    }

    // Create card element
    const card = document.createElement('div');
    card.className = 'info-card';
    
    // Create content
    const content = `
        <div class="info-card-content">
            <div class="info-row">
                <span class="info-label">Inverse:</span>
                <span class="info-value">${inverse}</span>
            </div>
            <div class="info-row">
                <span class="info-label">Order:</span>
                <span class="info-value">${order}</span>
            </div>
        </div>
    `;
    card.innerHTML = content;

    // Position the card next to the clicked button
    const rect = event.target.getBoundingClientRect();
    card.style.position = 'absolute';
    card.style.top = `${rect.top + window.scrollY}px`;
    card.style.left = `${rect.right + window.scrollX + 5}px`; // 5px offset from button

    // Add to document
    document.body.appendChild(card);

    // Close card when clicking outside
    document.addEventListener('click', function closeCard(e) {
        if (!card.contains(e.target) && e.target !== event.target) {
            card.remove();
            document.removeEventListener('click', closeCard);
        }
    });
    }

const COSET_COLORS = [
    '#FFADAD', '#FFD6A5', '#FDFFB6', '#CAFFBF',
    '#9BF6FF', '#A0C4FF', '#BDB2FF', '#FFC6FF'
];

let tableOriginalState = null;

function captureOriginalTableState(table) {
    if (tableOriginalState) return;
    const rows = Array.from(table.querySelectorAll('tr'));
    tableOriginalState = rows.map(tr => {
        const cells = Array.from(tr.querySelectorAll('td'));
        return {
            tr: tr,
            rowEl: cells[0] && cells[0].querySelector('button.element') ? cells[0].querySelector('button.element').dataset.el : null,
            cells: cells.map(td => ({
                td: td,
                el: td.querySelector('button.element') ? td.querySelector('button.element').dataset.el : null
            }))
        };
    });
}

function restoreOriginalTable(table) {
    if (!tableOriginalState) return;
    const tbody = table.querySelector('tbody') || table;
    tableOriginalState.forEach(rowInfo => {
        tbody.appendChild(rowInfo.tr);
        rowInfo.tr.style.borderBottom = '';
        rowInfo.cells.forEach(cellInfo => {
            rowInfo.tr.appendChild(cellInfo.td);
            cellInfo.td.style.borderRight = '';
            cellInfo.td.style.borderBottom = '';
        });
    });
}

function reorderTableByCosets(table, subgroupData) {
    captureOriginalTableState(table);
    if (!subgroupData) {
        restoreOriginalTable(table);
        return;
    }

    const orderedElements = [];
    subgroupData.cosets.forEach(coset => {
        coset.forEach(el => orderedElements.push(el));
    });

    const m = subgroupData.order; // size of subgroup / coset block size
    const tbody = table.querySelector('tbody') || table;

    const rowMap = {};
    tableOriginalState.forEach(rowInfo => {
        if (rowInfo.rowEl) {
            rowMap[rowInfo.rowEl] = rowInfo;
        }
    });

    orderedElements.forEach((rEl, rIdx) => {
        const rowInfo = rowMap[rEl];
        if (!rowInfo) return;
        
        const tr = rowInfo.tr;
        tbody.appendChild(tr);

        if ((rIdx + 1) % m === 0 && rIdx < orderedElements.length - 1) {
            tr.style.borderBottom = '3px solid #333';
        } else {
            tr.style.borderBottom = '';
        }

        const cellMap = {};
        rowInfo.cells.forEach(c => {
            if (c.el) cellMap[c.el] = c.td;
        });

        orderedElements.forEach((cEl, cIdx) => {
            const td = cellMap[cEl];
            if (!td) return;
            tr.appendChild(td);

            if ((cIdx + 1) % m === 0 && cIdx < orderedElements.length - 1) {
                td.style.borderRight = '3px solid #333';
            } else {
                td.style.borderRight = '';
            }
        });
    });
}

function getCayleyProduct(a, b) {
    const table = document.querySelector('#tableView table');
    if (!table) return null;

    const rows = Array.from(table.querySelectorAll('tr'));
    if (rows.length === 0) return null;

    const firstRowButtons = Array.from(rows[0].querySelectorAll('button.element'));
    const colIdx = firstRowButtons.findIndex(btn => btn.dataset.el === b);
    if (colIdx === -1) return null;

    const targetRow = rows.find(tr => {
        const btn = tr.querySelector('button.element');
        return btn && btn.dataset.el === a;
    });
    if (!targetRow) return null;

    const rowButtons = Array.from(targetRow.querySelectorAll('button.element'));
    if (colIdx >= rowButtons.length) return null;
    return rowButtons[colIdx].dataset.el;
}

function renderQuotientTable(subgroupData) {
    const existingView = document.getElementById('quotientView');
    if (existingView) {
        existingView.remove();
    }

    if (!subgroupData || !subgroupData.normal || subgroupData.cosets.length <= 1) {
        return;
    }

    const cosets = subgroupData.cosets;
    const k = cosets.length;

    const elToCoset = {};
    cosets.forEach((c, idx) => {
        c.forEach(el => elToCoset[el] = idx);
    });

    const cosetLabels = cosets.map((c, idx) => {
        if (idx === 0) return 'N';
        return `${c[0]}N`;
    });

    const tableView = document.getElementById('tableView');
    if (!tableView) return;

    const container = document.createElement('div');
    container.id = 'quotientView';
    container.style.marginTop = '2rem';
    container.style.padding = '1.25rem';
    container.style.borderRadius = '12px';
    container.style.background = '#ffffff';
    container.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
    container.style.textAlign = 'center';
    container.style.maxWidth = '650px';
    container.style.marginLeft = 'auto';
    container.style.marginRight = 'auto';

    let html = `
        <h3 style="margin-top:0; color:#1DA1F2; font-family: sans-serif;">
            ✨ Quotient Group G / N &nbsp;<span style="font-weight:normal; font-size: 0.9em; color:#555;">(Order ${k})</span>
        </h3>
        <p style="font-size: 13px; color: #666; margin-bottom: 1rem;">
            Normal Subgroup N = { ${subgroupData.elements.join(', ')} }
        </p>
        <table style="margin:0 auto; border-collapse: separate; border-spacing: 4px;">
            <thead>
                <tr>
                    <th style="padding: 6px 12px; background: #eee; border-radius: 4px; font-family: sans-serif;">G/N</th>
    `;
    cosetLabels.forEach((label, idx) => {
        const color = COSET_COLORS[idx % COSET_COLORS.length];
        html += `<th style="padding: 6px 12px; background: ${color}; border-radius: 4px; font-weight: bold; font-family: sans-serif;">C<sub>${idx}</sub> (${label})</th>`;
    });
    html += `</tr></thead><tbody>`;

    for (let i = 0; i < k; i++) {
        const rowColor = COSET_COLORS[i % COSET_COLORS.length];
        const repA = cosets[i][0];
        html += `<tr>`;
        html += `<td style="padding: 6px 12px; background: ${rowColor}; border-radius: 4px; font-weight: bold; font-family: sans-serif;">C<sub>${i}</sub> (${cosetLabels[i]})</td>`;

        for (let j = 0; j < k; j++) {
            const repB = cosets[j][0];
            const prod = getCayleyProduct(repA, repB);
            const resCosetIdx = (prod !== null && elToCoset[prod] !== undefined) ? elToCoset[prod] : 0;
            const resColor = COSET_COLORS[resCosetIdx % COSET_COLORS.length];

            html += `
                <td style="padding: 6px 12px; background: ${resColor}; border-radius: 4px; font-weight: bold; font-family: sans-serif; cursor: default;" title="${cosetLabels[i]} · ${cosetLabels[j]} = C${resCosetIdx} (${cosetLabels[resCosetIdx]})">
                    C<sub>${resCosetIdx}</sub>
                </td>
            `;
        }
        html += `</tr>`;
    }

    html += `</tbody></table>`;
    container.innerHTML = html;
    tableView.appendChild(container);
}


function clearSubgroupHighlight() {
    const qView = document.getElementById('quotientView');
    if (qView) qView.remove();

    document.querySelectorAll('button.element').forEach(btn => {
        if (btn.dataset.color) {
            btn.style.backgroundColor = btn.dataset.color;
        }
    });
}

function highlightSubgroup(subgroupData) {
    clearSubgroupHighlight();
    if (!subgroupData) {
        return;
    }

    // Render quotient mini-table for normal subgroups
    renderQuotientTable(subgroupData);

    // Main table: keep original layout, color only subgroup elements, set rest to white
    const subgroupMembers = new Set(subgroupData.elements);
    document.querySelectorAll('#tableView button.element').forEach(btn => {
        if (subgroupMembers.has(btn.dataset.el)) {
            if (btn.dataset.color) {
                btn.style.backgroundColor = btn.dataset.color;
            }
        } else {
            btn.style.backgroundColor = 'white';
        }
    });
}

function onSubgroupSelectChange(selectEl, subgroupsJson) {
    const idx = selectEl.value;
    const subgroup = (idx === '' || !subgroupsJson) ? null : subgroupsJson[parseInt(idx, 10)];

    if (document.getElementById('tableView')) {
        if (!subgroup) {
            clearSubgroupHighlight();
        } else {
            highlightSubgroup(subgroup);
        }
    }

    if (window.currentGraphController) {
        window.currentGraphController.highlightSubgroup(subgroup);
    }
}

function drawSubgroupLattice(subgroups, covers) {
    const container = document.getElementById('subgroup_lattice_container');
    const svg = document.getElementById('subgroup_lattice_svg');
    const nodesContainer = document.getElementById('subgroup_lattice_nodes');
    if (!container || !svg || !nodesContainer) return;

    svg.innerHTML = '';
    nodesContainer.innerHTML = '';

    if (!subgroups || subgroups.length === 0) return;

    const orders = Array.from(new Set(subgroups.map(s => s.order))).sort((a, b) => a - b);
    const layers = {};
    orders.forEach((order, idx) => {
        layers[order] = {
            index: idx,
            nodes: []
        };
    });

    subgroups.forEach((sub, idx) => {
        sub.index = idx;
        layers[sub.order].nodes.push(sub);
    });

    const numLayers = orders.length;
    const height = Math.max(450, numLayers * 100);
    const width = container.clientWidth || 600;

    container.style.height = `${height}px`;
    svg.setAttribute('width', width);
    svg.setAttribute('height', height);

    const nodePositions = {};

    orders.forEach((order, layerIdx) => {
        const layerNodes = layers[order].nodes;
        const count = layerNodes.length;
        const y = height - 40 - (layerIdx * (height - 80) / Math.max(1, numLayers - 1));

        layerNodes.forEach((node, i) => {
            const x = (i + 0.5) * (width / count);
            nodePositions[node.index] = { x, y };

            const btn = document.createElement('button');
            const genStr = node.generators.join(', ');
            btn.innerHTML = node.order === 1 ? 'e' : `⟨${genStr}⟩`;
            btn.className = 'subgroup-node-btn';
            btn.style.position = 'absolute';
            btn.style.left = `${x}px`;
            btn.style.top = `${y}px`;
            btn.style.transform = 'translate(-50%, -50%)';
            btn.style.padding = '6px 12px';
            btn.style.border = '2px solid ' + (node.normal ? '#1DA1F2' : '#555');
            btn.style.borderRadius = '20px';
            btn.style.backgroundColor = node.normal ? '#e8f5fe' : '#ffffff';
            btn.style.color = '#333';
            btn.style.fontWeight = 'bold';
            btn.style.fontSize = '12px';
            btn.style.cursor = 'pointer';
            btn.style.zIndex = '10';
            btn.style.boxShadow = '0 2px 5px rgba(0,0,0,0.15)';
            btn.style.transition = 'all 0.15s ease';

            btn.onmouseover = () => {
                btn.style.transform = 'translate(-50%, -50%) scale(1.1)';
                btn.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
            };
            btn.onmouseout = () => {
                btn.style.transform = 'translate(-50%, -50%) scale(1)';
                btn.style.boxShadow = '0 2px 5px rgba(0,0,0,0.15)';
            };

            btn.onclick = (e) => {
                showSubgroupInfoCard(e, node);
            };

            nodesContainer.appendChild(btn);
        });
    });

    if (covers) {
        Object.entries(covers).forEach(([fromIdxStr, toIndices]) => {
            const fromIdx = parseInt(fromIdxStr, 10);
            const pFrom = nodePositions[fromIdx];
            if (!pFrom) return;

            toIndices.forEach(toIdx => {
                const pTo = nodePositions[toIdx];
                if (!pTo) return;

                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', pFrom.x);
                line.setAttribute('y1', pFrom.y);
                line.setAttribute('x2', pTo.x);
                line.setAttribute('y2', pTo.y);
                line.setAttribute('stroke', '#bbb');
                line.setAttribute('stroke-width', '2');
                svg.appendChild(line);
            });
        });
    }
}

function showSubgroupInfoCard(event, node) {
    const existingCard = document.querySelector('.info-card');
    if (existingCard) {
        existingCard.remove();
    }

    const card = document.createElement('div');
    card.className = 'info-card';
    card.style.position = 'absolute';
    
    const content = `
        <div class="info-card-content" style="font-family: sans-serif; min-width: 180px;">
            <div class="info-row" style="margin-bottom: 4px;">
                <span class="info-label" style="font-weight: bold; color: #555;">Order:</span>
                <span class="info-value" style="font-weight: bold;">${node.order}</span>
            </div>
            <div class="info-row" style="margin-bottom: 8px;">
                <span class="info-label" style="font-weight: bold; color: #555;">Normality:</span>
                <span class="info-value" style="color: ${node.normal ? '#1DA1F2' : '#d9534f'}; font-weight: bold;">
                    ${node.normal ? 'Normal' : 'Not Normal'}
                </span>
            </div>
            <div style="margin-bottom: 6px;">
                <div class="info-label" style="font-weight: bold; color: #555; margin-bottom: 2px;">Generators:</div>
                <div class="info-value" style="word-break: break-all; font-family: monospace; font-size: 12px; color: #333;">
                    { ${node.generators.join(', ')} }
                </div>
            </div>
            <div>
                <div class="info-label" style="font-weight: bold; color: #555; margin-bottom: 2px;">Elements:</div>
                <div class="info-value" style="word-break: break-all; font-family: monospace; font-size: 11px; color: #666; max-height: 100px; overflow-y: auto;">
                    { ${node.elements.join(', ')} }
                </div>
            </div>
        </div>
    `;
    card.innerHTML = content;

    const rect = event.target.getBoundingClientRect();
    card.style.top = `${rect.top + window.scrollY}px`;
    card.style.left = `${rect.right + window.scrollX + 5}px`;

    document.body.appendChild(card);

    document.addEventListener('click', function closeCard(e) {
        if (!card.contains(e.target) && e.target !== event.target) {
            card.remove();
            document.removeEventListener('click', closeCard);
        }
    });
}






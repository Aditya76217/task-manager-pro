/**
 * ═══════════════════════════════════════════════════════
 * TaskManager Pro — Kanban Board JavaScript
 *
 * Handles:
 * 1. Drag-and-drop between Kanban columns
 * 2. AJAX status updates (no page reload)
 * 3. Progress bar updates
 * 4. Toast notifications
 * 5. Smooth animations
 * ═══════════════════════════════════════════════════════
 */

// ── Global state ─────────────────────────────────────
let draggedCard = null;


// ═════════════════════════════════════════════════════
// DRAG & DROP
// ═════════════════════════════════════════════════════

/**
 * Called when a task card starts being dragged.
 * Stores the dragged element reference and sets transfer data.
 */
function dragStart(event) {
    draggedCard = event.target.closest('.task-card');
    event.dataTransfer.setData('text/plain', draggedCard.dataset.taskId);
    event.dataTransfer.effectAllowed = 'move';

    // Add visual feedback after a tiny delay (so the drag image captures properly)
    requestAnimationFrame(() => {
        draggedCard.classList.add('dragging');
    });
}

/**
 * Allows a drop target to accept dragged elements.
 * Highlights the column being dragged over.
 */
function allowDrop(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';

    // Add visual highlight to the column
    const dropZone = event.currentTarget;
    dropZone.classList.add('drag-over');
}

/**
 * Called when a task card is dropped into a column.
 * Moves the card in the DOM and sends an AJAX request
 * to update the task's status in the database.
 */
function dropTask(event) {
    event.preventDefault();

    const dropZone = event.currentTarget;
    dropZone.classList.remove('drag-over');

    if (!draggedCard) return;

    const taskId = event.dataTransfer.getData('text/plain');
    const newStatus = dropZone.dataset.status;

    // Remove dragging state
    draggedCard.classList.remove('dragging');

    // Remove empty state message if present
    const emptyMsg = dropZone.querySelector('.empty-column');
    if (emptyMsg) emptyMsg.remove();

    // Move the card to the new column
    dropZone.appendChild(draggedCard);

    // Add drop animation
    draggedCard.classList.add('just-dropped');
    setTimeout(() => {
        draggedCard.classList.remove('just-dropped');
    }, 300);

    // Handle "done" styling
    if (newStatus === 'done') {
        draggedCard.classList.add('task-done');
    } else {
        draggedCard.classList.remove('task-done');
    }

    // Update the status in the backend via AJAX
    updateTaskStatus(taskId, newStatus);

    // Update column counts in the UI
    updateColumnCounts();

    draggedCard = null;
}


// ═════════════════════════════════════════════════════
// AJAX — Update Task Status
// ═════════════════════════════════════════════════════

/**
 * Sends a POST request to update the task's status
 * in the database. On success, updates the progress bar.
 *
 * @param {string} taskId - The task's primary key
 * @param {string} newStatus - The new status value (todo, in_progress, done)
 */
async function updateTaskStatus(taskId, newStatus) {
    try {
        const response = await fetch(UPDATE_STATUS_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: JSON.stringify({
                task_id: parseInt(taskId),
                new_status: newStatus,
            }),
        });

        const data = await response.json();

        if (data.success) {
            // Update progress bar
            updateProgressBar(data.progress_percent, data.done_count, data.total_tasks);
            // Show success toast
            showToast('Task status updated!', 'success');
        } else {
            showToast(`Error: ${data.error}`, 'error');
            // Reload page on error to restore correct state
            setTimeout(() => location.reload(), 1500);
        }
    } catch (error) {
        console.error('Status update failed:', error);
        showToast('Network error. Please try again.', 'error');
        setTimeout(() => location.reload(), 1500);
    }
}


// ═════════════════════════════════════════════════════
// UI Updates
// ═════════════════════════════════════════════════════

/**
 * Updates the progress bar and text to reflect
 * the current completion state.
 */
function updateProgressBar(percent, doneCount, totalTasks) {
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    if (progressBar) {
        progressBar.style.width = `${percent}%`;
        progressBar.setAttribute('aria-valuenow', percent);
    }
    if (progressText) {
        progressText.textContent = `${doneCount}/${totalTasks} completed`;
    }
}

/**
 * Updates the task count badges on each column header.
 */
function updateColumnCounts() {
    const columns = {
        'todo': document.getElementById('column-todo'),
        'in_progress': document.getElementById('column-in_progress'),
        'done': document.getElementById('column-done'),
    };

    Object.entries(columns).forEach(([status, column]) => {
        if (!column) return;
        const body = column.querySelector('.kanban-body');
        const badge = column.querySelector('.kanban-header .badge');
        if (body && badge) {
            const count = body.querySelectorAll('.task-card').length;
            badge.textContent = count;

            // Add empty state if no tasks
            if (count === 0 && !body.querySelector('.empty-column')) {
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'empty-column text-center py-5';
                let icon, text;
                if (status === 'todo') {
                    icon = 'bi-inbox';
                    text = 'No tasks here yet';
                } else if (status === 'in_progress') {
                    icon = 'bi-hourglass-split';
                    text = 'Nothing in progress';
                } else {
                    icon = 'bi-trophy';
                    text = 'No completed tasks';
                }
                emptyDiv.innerHTML = `
                    <i class="bi ${icon} fs-1 text-muted"></i>
                    <p class="text-muted mt-2 mb-0">${text}</p>
                `;
                body.appendChild(emptyDiv);
            }
        }
    });
}


// ═════════════════════════════════════════════════════
// Toast Notifications
// ═════════════════════════════════════════════════════

/**
 * Shows a floating toast notification at the bottom-right
 * corner of the screen.
 *
 * @param {string} message - The message to display
 * @param {string} type - 'success' or 'error'
 */
function showToast(message, type = 'success') {
    // Create container if it doesn't exist
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;

    const icon = type === 'success'
        ? '<i class="bi bi-check-circle-fill text-success"></i>'
        : '<i class="bi bi-exclamation-circle-fill text-danger"></i>';

    toast.innerHTML = `${icon} <span>${message}</span>`;
    container.appendChild(toast);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


// ═════════════════════════════════════════════════════
// Event Listeners
// ═════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

    // ── Remove drag-over highlight when leaving a drop zone ──
    document.querySelectorAll('.kanban-body').forEach(zone => {
        zone.addEventListener('dragleave', (e) => {
            // Only remove if actually leaving the zone, not entering a child
            if (!zone.contains(e.relatedTarget)) {
                zone.classList.remove('drag-over');
            }
        });

        // Also remove on dragend (for cancelled drags)
        zone.addEventListener('dragend', () => {
            zone.classList.remove('drag-over');
        });
    });

    // ── Remove dragging class when drag ends ──
    document.addEventListener('dragend', () => {
        if (draggedCard) {
            draggedCard.classList.remove('dragging');
            draggedCard = null;
        }
        // Clean up all drag-over highlights
        document.querySelectorAll('.drag-over').forEach(el => {
            el.classList.remove('drag-over');
        });
    });

    // ── Auto-dismiss Django messages after 5 seconds ──
    document.querySelectorAll('.alert-dismissible').forEach(alert => {
        setTimeout(() => {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });
});

// Skibidi Toilet Community Hub JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚽 Skibidi Hub loaded! Sigma energy activated! ⚡');
    
    // Initialize brainrot features
    initializeSkibidiFeatures();
    setupFileUpload();
    addBrainrotInteractions();
});

function initializeSkibidiFeatures() {
    // Add sigma level indicators to posts
    const posts = document.querySelectorAll('.ohio-card');
    posts.forEach((post, index) => {
        // Add random brainrot badges
        const badges = ['Sigma', 'Ohio', 'Rizz', 'Gyatt', 'Bussin'];
        const randomBadge = badges[Math.floor(Math.random() * badges.length)];
        
        const badgeElement = document.createElement('span');
        badgeElement.className = 'brainrot-badge';
        badgeElement.textContent = randomBadge;
        
        const username = post.querySelector('.skibidi-username');
        if (username) {
            username.appendChild(badgeElement);
        }
    });
    
    // Add toilet/camera decorations
    const usernames = document.querySelectorAll('.skibidi-username');
    usernames.forEach((username, index) => {
        if (index % 2 === 0) {
            username.classList.add('toilet-decoration');
        } else {
            username.classList.add('camera-decoration');
        }
    });
}

function setupFileUpload() {
    const fileInput = document.getElementById('file');
    const fileUploadArea = document.querySelector('.file-upload-area');
    
    if (!fileInput || !fileUploadArea) return;
    
    // Drag and drop functionality
    fileUploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        fileUploadArea.style.borderColor = '#7c3aed';
        fileUploadArea.style.background = 'rgba(124, 58, 237, 0.1)';
    });
    
    fileUploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        fileUploadArea.style.borderColor = '#2563eb';
        fileUploadArea.style.background = '#f3f4f6';
    });
    
    fileUploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        fileUploadArea.style.borderColor = '#2563eb';
        fileUploadArea.style.background = '#f3f4f6';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFileDisplay(files[0]);
        }
    });
    
    // File input change handler
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            updateFileDisplay(e.target.files[0]);
        }
    });
    
    // Click to select file
    fileUploadArea.addEventListener('click', function() {
        fileInput.click();
    });
}

function updateFileDisplay(file) {
    const fileUploadArea = document.querySelector('.file-upload-area');
    const maxSize = 2.5 * 1024 * 1024; // 2.5MB
    
    if (file.size > maxSize) {
        fileUploadArea.innerHTML = `
            <div class="skibidi-emoji">💀</div>
            <p style="color: #dc2626; font-weight: bold;">File too chonky! Keep it under 2.5MB!</p>
            <p style="color: #6b7280;">Selected: ${file.name} (${formatFileSize(file.size)})</p>
        `;
        return;
    }
    
    fileUploadArea.innerHTML = `
        <div class="skibidi-emoji">✅</div>
        <p style="color: #16a34a; font-weight: bold;">Skibidi file ready to upload!</p>
        <p style="color: #6b7280;">${file.name} (${formatFileSize(file.size)})</p>
    `;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function addBrainrotInteractions() {
    // Add character counter for post content
    const contentTextarea = document.getElementById('content');
    if (contentTextarea) {
        const maxLength = 2048; // 2KB
        
        // Create character counter
        const counterDiv = document.createElement('div');
        counterDiv.className = 'character-counter';
        counterDiv.style.textAlign = 'right';
        counterDiv.style.marginTop = '0.5rem';
        counterDiv.style.fontSize = '0.9rem';
        
        contentTextarea.parentNode.insertBefore(counterDiv, contentTextarea.nextSibling);
        
        function updateCounter() {
            const currentLength = new Blob([contentTextarea.value]).size;
            const remaining = maxLength - currentLength;
            
            counterDiv.innerHTML = `
                <span style="color: ${remaining < 200 ? '#dc2626' : '#6b7280'};">
                    ${currentLength}/${maxLength} bytes 
                    ${remaining < 0 ? '(Too much brainrot! 💀)' : ''}
                </span>
            `;
            
            if (remaining < 0) {
                contentTextarea.style.borderColor = '#dc2626';
            } else {
                contentTextarea.style.borderColor = '#2563eb';
            }
        }
        
        contentTextarea.addEventListener('input', updateCounter);
        updateCounter(); // Initial update
    }
    
    // Add comment character counters
    const commentTextareas = document.querySelectorAll('textarea[name="comment"]');
    commentTextareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            const maxLength = 500;
            const currentLength = new Blob([this.value]).size;
            const remaining = maxLength - currentLength;
            
            // Create or update counter
            let counter = this.parentNode.querySelector('.comment-counter');
            if (!counter) {
                counter = document.createElement('small');
                counter.className = 'comment-counter text-muted';
                this.parentNode.appendChild(counter);
            }
            
            counter.textContent = `${currentLength}/${maxLength} bytes`;
            counter.style.color = remaining < 50 ? '#dc2626' : '#6b7280';
            
            if (remaining < 0) {
                this.style.borderColor = '#dc2626';
            } else {
                this.style.borderColor = '';
            }
        });
    });
    
    // Add skibidi sound effects (visual feedback)
    const buttons = document.querySelectorAll('.rizz-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    this.style.transform = '';
                }, 100);
            }, 100);
        });
    });
    
    // Copy to clipboard function
    window.copyToClipboard = function(text, type) {
        navigator.clipboard.writeText(text).then(function() {
            // Show success message
            const toast = document.createElement('div');
            toast.className = 'alert alert-success position-fixed';
            toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 200px;';
            toast.innerHTML = `<i class="fas fa-check"></i> ${type} copied to clipboard!`;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const toast = document.createElement('div');
            toast.className = 'alert alert-success position-fixed';
            toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 200px;';
            toast.innerHTML = `<i class="fas fa-check"></i> ${type} copied!`;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 3000);
        });
    };

    // Add brainrot quotes rotation
    const quotes = [
        "Only in Ohio! 🚽",
        "That's so sigma! ⚡",
        "Absolute rizz energy! 📸",
        "Skibidi bop bop yes yes! 🎵",
        "Gyatt damn! 💀",
        "Bussin fr fr! 🔥"
    ];
    
    const titleElement = document.querySelector('.brainrot-subtitle');
    if (titleElement) {
        let quoteIndex = 0;
        setInterval(() => {
            titleElement.textContent = quotes[quoteIndex];
            quoteIndex = (quoteIndex + 1) % quotes.length;
        }, 3000);
    }
}

// Add some easter eggs
function addSkibidiEasterEggs() {
    // Konami code for extra sigma energy
    let konamiCode = [];
    const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65]; // ↑↑↓↓←→←→BA
    
    document.addEventListener('keydown', function(e) {
        konamiCode.push(e.keyCode);
        if (konamiCode.length > konamiSequence.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.join(',') === konamiSequence.join(',')) {
            document.body.style.animation = 'rainbow 2s infinite';
            setTimeout(() => {
                document.body.style.animation = '';
            }, 5000);
        }
    });
    
    // Add rainbow animation for easter egg
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}

// Initialize easter eggs
addSkibidiEasterEggs();

// Expose functions to global window object for onclick handlers
window.toggleLikeForm = function toggleLikeForm(postId) {
    const likeForm = document.getElementById('like-form-' + postId);
    const commentForm = document.getElementById('comment-form-' + postId);
    
    // Hide comment form if open
    if (commentForm) {
        commentForm.style.display = 'none';
    }
    
    // Toggle like form
    if (likeForm) {
        if (likeForm.style.display === 'none' || likeForm.style.display === '') {
            likeForm.style.display = 'block';
            const usernameInput = likeForm.querySelector('input[name="username"]');
            if (usernameInput) {
                usernameInput.focus();
            }
        } else {
            likeForm.style.display = 'none';
        }
    }
}

window.toggleCommentForm = function toggleCommentForm(postId) {
    const commentForm = document.getElementById('comment-form-' + postId);
    const likeForm = document.getElementById('like-form-' + postId);
    
    // Hide like form if open
    if (likeForm) {
        likeForm.style.display = 'none';
    }
    
    // Toggle comment form
    if (commentForm) {
        if (commentForm.style.display === 'none' || commentForm.style.display === '') {
            commentForm.style.display = 'block';
            const usernameInput = commentForm.querySelector('input[name="username"]');
            if (usernameInput) {
                usernameInput.focus();
            }
        } else {
            commentForm.style.display = 'none';
        }
    }
}

window.toggleComments = function toggleComments(postId) {
    const commentsSection = document.getElementById('comments-section-' + postId);
    const toggleIcon = document.getElementById('toggle-icon-' + postId);
    const toggleText = document.getElementById('toggle-text-' + postId);
    
    if (commentsSection) {
        if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
            commentsSection.style.display = 'block';
            if (toggleIcon) toggleIcon.className = 'fas fa-eye-slash';
            if (toggleText) toggleText.textContent = 'Hide Comments';
            
            // Load comments if not already loaded
            loadComments(postId);
        } else {
            commentsSection.style.display = 'none';
            if (toggleIcon) toggleIcon.className = 'fas fa-eye';
            if (toggleText) toggleText.textContent = 'Show Comments';
        }
    }
}

function loadComments(postId) {
    const commentsContainer = document.getElementById('comments-container-' + postId);
    const loadingSpinner = document.getElementById('comments-loading-' + postId);
    
    if (!commentsContainer || commentsContainer.hasAttribute('data-loaded')) {
        return; // Already loaded
    }
    
    if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
    }
    
    // Fetch comments via AJAX
    fetch(`/comments/${postId}?page=1`)
        .then(response => response.json())
        .then(data => {
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }
            
            if (data.comments && data.comments.length > 0) {
                renderComments(postId, data.comments, data.pagination);
                commentsContainer.setAttribute('data-loaded', 'true');
            } else {
                commentsContainer.innerHTML = '<p class="text-muted text-center">No comments yet. Be the first to drop some sigma wisdom!</p>';
            }
        })
        .catch(error => {
            console.error('Error loading comments:', error);
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }
            commentsContainer.innerHTML = '<p class="text-danger text-center">Failed to load comments. Try again later!</p>';
        });
}

function renderComments(postId, comments, pagination) {
    const commentsContainer = document.getElementById('comments-container-' + postId);
    const paginationContainer = document.getElementById('comment-pagination-' + postId);
    
    if (!commentsContainer) return;
    
    // Render comments
    let commentsHTML = '';
    comments.forEach(comment => {
        commentsHTML += `
            <div class="comment-item border-start border-primary ps-3 mb-3">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong class="skibidi-username">${escapeHtml(comment.username)}</strong>
                        <small class="text-muted ms-2">${formatTimeAgo(comment.timestamp)}</small>
                    </div>
                </div>
                <div class="skibidi-content mt-1">${escapeHtml(comment.content)}</div>
            </div>
        `;
    });
    
    commentsContainer.innerHTML = commentsHTML;
    
    // Render pagination if needed
    if (paginationContainer && pagination && pagination.total_pages > 1) {
        renderCommentPagination(postId, pagination);
    }
}

function renderCommentPagination(postId, pagination) {
    const paginationContainer = document.getElementById('comment-pagination-' + postId);
    if (!paginationContainer) return;
    
    let paginationHTML = '<div class="btn-group btn-group-sm" role="group">';
    
    // Previous button
    if (pagination.has_prev) {
        paginationHTML += `<button type="button" class="btn btn-outline-secondary" onclick="loadCommentsPage('${postId}', ${pagination.prev_num})">‹</button>`;
    }
    
    // Page info
    paginationHTML += `<button type="button" class="btn btn-outline-primary" disabled>${pagination.page}/${pagination.total_pages}</button>`;
    
    // Next button
    if (pagination.has_next) {
        paginationHTML += `<button type="button" class="btn btn-outline-secondary" onclick="loadCommentsPage('${postId}', ${pagination.next_num})">›</button>`;
    }
    
    paginationHTML += '</div>';
    paginationContainer.innerHTML = paginationHTML;
}

function loadCommentsPage(postId, page) {
    const commentsContainer = document.getElementById('comments-container-' + postId);
    const loadingSpinner = document.getElementById('comments-loading-' + postId);
    
    if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
    }
    
    fetch(`/comments/${postId}?page=${page}`)
        .then(response => response.json())
        .then(data => {
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }
            renderComments(postId, data.comments, data.pagination);
        })
        .catch(error => {
            console.error('Error loading comments page:', error);
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }
        });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTimeAgo(timestamp) {
    const now = new Date();
    const commentTime = new Date(timestamp);
    const diffMs = now - commentTime;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return commentTime.toLocaleDateString();
}

// Enhanced form submissions with loading states
document.addEventListener('DOMContentLoaded', function() {
    // Add loading state to like forms
    const likeForms = document.querySelectorAll('form[action*="/like/"]');
    likeForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalContent = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading-spinner"></span>';
                submitBtn.disabled = true;
                
                // Re-enable after timeout (in case of errors)
                setTimeout(() => {
                    submitBtn.innerHTML = originalContent;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
    
    // Add loading state to comment forms
    const commentForms = document.querySelectorAll('form[action*="/comment/"]');
    commentForms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalContent = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading-spinner"></span>';
                submitBtn.disabled = true;
                
                // Re-enable after timeout (in case of errors)
                setTimeout(() => {
                    submitBtn.innerHTML = originalContent;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
    
    // Add search highlighting
    const searchQuery = new URLSearchParams(window.location.search).get('search');
    if (searchQuery && searchQuery.trim()) {
        highlightSearchTerms(searchQuery.trim());
    }
});

// Search term highlighting function
function highlightSearchTerms(query) {
    const posts = document.querySelectorAll('.skibidi-content, .skibidi-username');
    const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    
    posts.forEach(element => {
        if (element.textContent.toLowerCase().includes(query.toLowerCase())) {
            element.innerHTML = element.innerHTML.replace(regex, '<span class="search-highlight">$1</span>');
        }
    });
}

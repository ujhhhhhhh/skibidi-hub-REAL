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
    const maxSize = 25 * 1024 * 1024; // 25MB
    
    if (file.size > maxSize) {
        fileUploadArea.innerHTML = `
            <div class="skibidi-emoji">💀</div>
            <p style="color: #dc2626; font-weight: bold;">File too chonky! Keep it under 25MB!</p>
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

// Global functions for post interactions
function toggleLikeForm(postId) {
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

function toggleCommentForm(postId) {
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

document.addEventListener("DOMContentLoaded", function() {
    // Find all TOC list items in the main navigation
    const tocItems = document.querySelectorAll('.ltx_TOC .ltx_toclist li');
    
    tocItems.forEach(item => {
        // Check if this item has a nested list
        const nestedList = item.querySelector(':scope > ol.ltx_toclist');
        if (nestedList) {
            // Create a toggle button wrapper
            const toggleWrapper = document.createElement('span');
            toggleWrapper.style.cursor = 'pointer';
            toggleWrapper.style.marginRight = '8px';
            toggleWrapper.style.display = 'inline-flex';
            toggleWrapper.style.alignItems = 'center';
            toggleWrapper.style.justifyContent = 'center';
            toggleWrapper.style.width = '16px';
            toggleWrapper.style.height = '16px';
            toggleWrapper.style.userSelect = 'none';
            
            // The actual icon
            const toggleIcon = document.createElement('span');
            toggleIcon.innerHTML = '▶';
            toggleIcon.style.fontSize = '0.7em';
            toggleIcon.style.transition = 'transform 0.2s ease-in-out';
            toggleIcon.style.color = '#555';
            
            toggleWrapper.appendChild(toggleIcon);
            
            // Insert it at the beginning of the item
            item.insertBefore(toggleWrapper, item.firstChild);
            
            // Add custom class to the item for styling if needed
            item.classList.add('has-children');
            
            // Initially hide the nested list (unless it's the top level doc list)
            // If we want to hide by default:
            nestedList.style.display = 'none';
            
            // Add click event
            toggleWrapper.addEventListener('click', function(e) {
                e.stopPropagation(); // prevent triggering parent toggles
                if (nestedList.style.display === 'none') {
                    nestedList.style.display = 'block';
                    toggleIcon.style.transform = 'rotate(90deg)';
                } else {
                    nestedList.style.display = 'none';
                    toggleIcon.style.transform = 'rotate(0deg)';
                }
            });
        } else {
            // No nested list, add an empty placeholder to align text
            const spacer = document.createElement('span');
            spacer.style.display = 'inline-block';
            spacer.style.width = '24px'; // 16px icon + 8px margin
            item.insertBefore(spacer, item.firstChild);
        }
    });
    
    // Auto-expand the current page if it's in the TOC
    // (Optional enhancement to show where the user is)
    const currentUrl = window.location.pathname.split('/').pop() || 'index.html';
    const currentLink = document.querySelector(`.ltx_TOC a[href="${currentUrl}"]`);
    if (currentLink) {
        let parentLi = currentLink.closest('li');
        while (parentLi) {
            const nestedList = parentLi.querySelector(':scope > ol.ltx_toclist');
            if (nestedList) {
                nestedList.style.display = 'block';
                const icon = parentLi.querySelector('span > span');
                if (icon) icon.style.transform = 'rotate(90deg)';
            }
            parentLi = parentLi.parentElement.closest('li');
        }
    }
});

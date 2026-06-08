/**
 * SHADOW RUN: Endless Nightmare — Game Design Document
 * Interactive JavaScript for Navigation and Theme Toggle
 */

(function () {
  'use strict';

  // ==========================================================================
  // DOM Elements
  // ==========================================================================
  const sidebar = document.getElementById('sidebar');
  const navToggle = document.getElementById('navToggle');
  const themeToggle = document.getElementById('themeToggle');
  const navLinks = document.querySelectorAll('.nav-list a');
  const sections = document.querySelectorAll('.gdd-section, .cover-page, .toc');

  // ==========================================================================
  // Theme Management
  // ==========================================================================

  /**
   * Get the current theme from localStorage or system preference
   * @returns {string} 'light' or 'dark'
   */
  function getPreferredTheme() {
    const stored = localStorage.getItem('gdd-theme');
    if (stored) {
      return stored;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  /**
   * Apply theme to document
   * @param {string} theme - 'light' or 'dark'
   */
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('gdd-theme', theme);

    // Update toggle button text
    if (!themeToggle) {
      return;
    }

    const themeIcon = themeToggle.querySelector('.theme-icon');
    const themeText = themeToggle.querySelector('.theme-text');

    if (theme === 'dark') {
      themeIcon.textContent = '☀️';
      themeText.textContent = 'Light Mode';
    } else {
      themeIcon.textContent = '🌙';
      themeText.textContent = 'Dark Mode';
    }
  }

  /**
   * Toggle between light and dark themes
   */
  function toggleTheme() {
    const current =
      document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  }

  // ==========================================================================
  // Navigation
  // ==========================================================================

  /**
   * Toggle mobile sidebar visibility
   */
  function toggleSidebar() {
    if (!sidebar) {
      return;
    }

    sidebar.classList.toggle('open');
  }

  /**
   * Close sidebar on mobile
   */
  function closeSidebar() {
    if (!sidebar) {
      return;
    }

    sidebar.classList.remove('open');
  }

  /**
   * Update active navigation link based on scroll position
   */
  function updateActiveNavLink() {
    const scrollPosition = window.scrollY + 150;

    let activeSection = null;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionBottom = sectionTop + section.offsetHeight;

      if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
        activeSection = section;
      }
    });

    if (activeSection) {
      const activeId = activeSection.getAttribute('id');

      navLinks.forEach((link) => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${activeId}`) {
          link.classList.add('active');
        }
      });
    }
  }

  /**
   * Smooth scroll to section when nav link is clicked
   * @param {Event} event - Click event
   */
  function handleNavLinkClick(event) {
    const href = event.currentTarget.getAttribute('href');

    if (href.startsWith('#')) {
      event.preventDefault();

      const targetId = href.substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        const headerOffset = 20;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition =
          elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth',
        });

        // Update URL hash without jumping
        history.pushState(null, null, href);

        // Close mobile sidebar
        closeSidebar();

        // Update active state
        navLinks.forEach((link) => link.classList.remove('active'));
        event.currentTarget.classList.add('active');
      }
    }
  }

  // ==========================================================================
  // Collapsible Sections
  // ==========================================================================

  /**
   * Initialize collapsible subsections
   */
  function initCollapsibleSections() {
    const subsections = document.querySelectorAll('.subsection');

    subsections.forEach((subsection) => {
      const heading = subsection.querySelector('h3');

      if (heading) {
        // Add collapse indicator
        const indicator = document.createElement('span');
        indicator.className = 'collapse-indicator';
        indicator.innerHTML = '▼';
        indicator.style.cssText = `
                    float: right;
                    font-size: 0.75em;
                    opacity: 0.5;
                    transition: transform 0.2s ease;
                    cursor: pointer;
                    user-select: none;
                `;

        heading.style.cursor = 'pointer';
        heading.appendChild(indicator);

        // Create collapsible content wrapper
        const content = document.createElement('div');
        content.className = 'subsection-content';

        // Move all content after heading into wrapper
        const children = Array.from(subsection.children);
        let afterHeading = false;

        children.forEach((child) => {
          if (child === heading) {
            afterHeading = true;
          } else if (afterHeading) {
            content.appendChild(child);
          }
        });

        subsection.appendChild(content);

        // Add click handler
        heading.addEventListener('click', () => {
          const isCollapsed = subsection.classList.toggle('collapsed');
          indicator.style.transform = isCollapsed
            ? 'rotate(-90deg)'
            : 'rotate(0deg)';
          content.style.display = isCollapsed ? 'none' : 'block';
        });
      }
    });
  }

  // ==========================================================================
  // Scroll Progress Indicator
  // ==========================================================================

  /**
   * Create and update scroll progress bar
   */
  function initScrollProgress() {
    // Create progress bar element
    const progressBar = document.createElement('div');
    progressBar.id = 'scroll-progress';
    progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #6b2d5c, #c44569);
            z-index: 1000;
            transition: width 0.1s ease-out;
        `;
    document.body.appendChild(progressBar);

    // Update on scroll
    function updateProgress() {
      const scrollTop = window.scrollY;
      const docHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const progress = (scrollTop / docHeight) * 100;
      progressBar.style.width = `${Math.min(progress, 100)}%`;
    }

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  // ==========================================================================
  // Print Functionality
  // ==========================================================================

  /**
   * Prepare document for printing
   */
  function preparePrint() {
    // Expand all collapsed sections before printing
    const collapsedSections = document.querySelectorAll(
      '.subsection.collapsed',
    );
    collapsedSections.forEach((section) => {
      section.classList.remove('collapsed');
      const content = section.querySelector('.subsection-content');
      const indicator = section.querySelector('.collapse-indicator');
      if (content) content.style.display = 'block';
      if (indicator) indicator.style.transform = 'rotate(0deg)';
    });
  }

  // ==========================================================================
  // Back to Top Button
  // ==========================================================================

  /**
   * Create back to top button
   */
  function initBackToTop() {
    const button = document.createElement('button');
    button.id = 'back-to-top';
    button.innerHTML = '↑';
    button.setAttribute('aria-label', 'Back to top');
    button.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: var(--color-primary, #6b2d5c);
            color: white;
            border: none;
            font-size: 1.25rem;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.2s ease;
            z-index: 99;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        `;

    document.body.appendChild(button);

    // Show/hide based on scroll position
    function toggleButton() {
      if (window.scrollY > 500) {
        button.style.opacity = '1';
        button.style.visibility = 'visible';
      } else {
        button.style.opacity = '0';
        button.style.visibility = 'hidden';
      }
    }

    window.addEventListener('scroll', toggleButton, { passive: true });

    // Scroll to top on click
    button.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    });

    // Hover effect
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.1)';
    });

    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1)';
    });
  }

  // ==========================================================================
  // Keyboard Navigation
  // ==========================================================================

  /**
   * Handle keyboard shortcuts
   */
  function handleKeyboard(event) {
    // Escape closes mobile sidebar
    if (event.key === 'Escape') {
      closeSidebar();
    }

    // Ctrl/Cmd + P triggers print preparation
    if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
      preparePrint();
    }
  }

  // ==========================================================================
  // Initialization
  // ==========================================================================

  /**
   * Initialize all interactive features
   */
  function init() {
    // Apply saved/preferred theme
    applyTheme(getPreferredTheme());

    // Event listeners
    if (themeToggle) {
      themeToggle.addEventListener('click', toggleTheme);
    }

    if (navToggle) {
      navToggle.addEventListener('click', toggleSidebar);
    }

    navLinks.forEach((link) => {
      link.addEventListener('click', handleNavLinkClick);
    });

    // Scroll event for active nav link
    let scrollTimeout;
    window.addEventListener(
      'scroll',
      () => {
        if (scrollTimeout) {
          window.cancelAnimationFrame(scrollTimeout);
        }
        scrollTimeout = window.requestAnimationFrame(updateActiveNavLink);
      },
      { passive: true },
    );

    // Keyboard navigation
    document.addEventListener('keydown', handleKeyboard);

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (event) => {
      if (window.innerWidth <= 1024) {
        if (
          sidebar &&
          navToggle &&
          !sidebar.contains(event.target) &&
          !navToggle.contains(event.target)
        ) {
          closeSidebar();
        }
      }
    });

    // Print event listener
    window.addEventListener('beforeprint', preparePrint);

    // Initialize additional features
    initScrollProgress();
    initBackToTop();

    // Optional: Initialize collapsible sections (uncomment to enable)
    // initCollapsibleSections();

    // Initial active nav link update
    updateActiveNavLink();

    console.log('GDD Interactive Features Initialized');
  }

  // Run initialization when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ==========================================================================
  // Print Styles Injection for Edge Cases
  // ==========================================================================

  // Add print-specific styles dynamically for browsers that need it
  const printStyles = `
        @media print {
            #scroll-progress,
            #back-to-top,
            .collapse-indicator {
                display: none !important;
            }
        }
    `;

  const styleSheet = document.createElement('style');
  styleSheet.textContent = printStyles;
  document.head.appendChild(styleSheet);
})();

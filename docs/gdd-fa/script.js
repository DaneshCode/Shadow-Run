/**
 * SHADOW RUN: کابوس بی‌پایان — سند طراحی بازی
 * جاوااسکریپت تعاملی برای ناوبری و تغییر تم
 */

(function () {
  'use strict';

  // ==========================================================================
  // عناصر DOM
  // ==========================================================================
  const sidebar = document.getElementById('sidebar');
  const navToggle = document.getElementById('navToggle');
  const themeToggle = document.getElementById('themeToggle');
  const navLinks = document.querySelectorAll('.nav-list a');
  const sections = document.querySelectorAll('.gdd-section, .cover-page, .toc');

  // ==========================================================================
  // مدیریت تم
  // ==========================================================================

  /**
   * دریافت تم فعلی از localStorage یا ترجیح سیستم
   * @returns {string} 'light' یا 'dark'
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
   * اعمال تم به سند
   * @param {string} theme - 'light' یا 'dark'
   */
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('gdd-theme', theme);

    // به‌روزرسانی متن دکمه تغییر
    const themeIcon = themeToggle.querySelector('.theme-icon');
    const themeText = themeToggle.querySelector('.theme-text');

    if (theme === 'dark') {
      themeIcon.textContent = '☀️';
      themeText.textContent = 'حالت روشن';
    } else {
      themeIcon.textContent = '🌙';
      themeText.textContent = 'حالت تاریک';
    }
  }

  /**
   * تغییر بین تم‌های روشن و تاریک
   */
  function toggleTheme() {
    const current =
      document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  }

  // ==========================================================================
  // ناوبری
  // ==========================================================================

  /**
   * تغییر نمایش نوار کناری موبایل
   */
  function toggleSidebar() {
    sidebar.classList.toggle('open');
  }

  /**
   * بستن نوار کناری در موبایل
   */
  function closeSidebar() {
    sidebar.classList.remove('open');
  }

  /**
   * به‌روزرسانی لینک ناوبری فعال بر اساس موقعیت اسکرول
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
   * اسکرول نرم به بخش هنگام کلیک لینک ناوبری
   * @param {Event} event - رویداد کلیک
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

        // به‌روزرسانی هش URL بدون پرش
        history.pushState(null, null, href);

        // بستن نوار کناری موبایل
        closeSidebar();

        // به‌روزرسانی وضعیت فعال
        navLinks.forEach((link) => link.classList.remove('active'));
        event.currentTarget.classList.add('active');
      }
    }
  }

  // ==========================================================================
  // بخش‌های قابل جمع شدن
  // ==========================================================================

  /**
   * مقداردهی اولیه زیربخش‌های قابل جمع شدن
   */
  function initCollapsibleSections() {
    const subsections = document.querySelectorAll('.subsection');

    subsections.forEach((subsection) => {
      const heading = subsection.querySelector('h3');

      if (heading) {
        // اضافه کردن نشانگر جمع شدن
        const indicator = document.createElement('span');
        indicator.className = 'collapse-indicator';
        indicator.innerHTML = '▼';
        indicator.style.cssText = `
                    float: left;
                    font-size: 0.75em;
                    opacity: 0.5;
                    transition: transform 0.2s ease;
                    cursor: pointer;
                    user-select: none;
                `;

        heading.style.cursor = 'pointer';
        heading.appendChild(indicator);

        // ایجاد پوشش محتوای قابل جمع شدن
        const content = document.createElement('div');
        content.className = 'subsection-content';

        // انتقال تمام محتوا پس از عنوان به پوشش
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

        // اضافه کردن مدیریت کلیک
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
  // نشانگر پیشرفت اسکرول
  // ==========================================================================

  /**
   * ایجاد و به‌روزرسانی نوار پیشرفت اسکرول
   */
  function initScrollProgress() {
    // ایجاد عنصر نوار پیشرفت
    const progressBar = document.createElement('div');
    progressBar.id = 'scroll-progress';
    progressBar.style.cssText = `
            position: fixed;
            top: 0;
            right: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #6b2d5c, #c44569);
            z-index: 1000;
            transition: width 0.1s ease-out;
        `;
    document.body.appendChild(progressBar);

    // به‌روزرسانی هنگام اسکرول
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
  // عملکرد چاپ
  // ==========================================================================

  /**
   * آماده‌سازی سند برای چاپ
   */
  function preparePrint() {
    // باز کردن تمام بخش‌های جمع شده قبل از چاپ
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
  // دکمه بازگشت به بالا
  // ==========================================================================

  /**
   * ایجاد دکمه بازگشت به بالا
   */
  function initBackToTop() {
    const button = document.createElement('button');
    button.id = 'back-to-top';
    button.innerHTML = '↑';
    button.setAttribute('aria-label', 'بازگشت به بالا');
    button.style.cssText = `
            position: fixed;
            bottom: 2rem;
            left: 2rem;
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

    // نمایش/مخفی کردن بر اساس موقعیت اسکرول
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

    // اسکرول به بالا هنگام کلیک
    button.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    });

    // افکت هاور
    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.1)';
    });

    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1)';
    });
  }

  // ==========================================================================
  // ناوبری کیبورد
  // ==========================================================================

  /**
   * مدیریت میانبرهای کیبورد
   */
  function handleKeyboard(event) {
    // Escape نوار کناری موبایل را می‌بندد
    if (event.key === 'Escape') {
      closeSidebar();
    }

    // Ctrl/Cmd + P آماده‌سازی چاپ را فعال می‌کند
    if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
      preparePrint();
    }
  }

  // ==========================================================================
  // مقداردهی اولیه
  // ==========================================================================

  /**
   * مقداردهی اولیه تمام ویژگی‌های تعاملی
   */
  function init() {
    // اعمال تم ذخیره شده/ترجیحی
    applyTheme(getPreferredTheme());

    // شنوندگان رویداد
    if (themeToggle) {
      themeToggle.addEventListener('click', toggleTheme);
    }

    if (navToggle) {
      navToggle.addEventListener('click', toggleSidebar);
    }

    navLinks.forEach((link) => {
      link.addEventListener('click', handleNavLinkClick);
    });

    // رویداد اسکرول برای لینک ناوبری فعال
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

    // ناوبری کیبورد
    document.addEventListener('keydown', handleKeyboard);

    // بستن نوار کناری هنگام کلیک خارج در موبایل
    document.addEventListener('click', (event) => {
      if (window.innerWidth <= 1024) {
        if (
          !sidebar.contains(event.target) &&
          !navToggle.contains(event.target)
        ) {
          closeSidebar();
        }
      }
    });

    // شنونده رویداد چاپ
    window.addEventListener('beforeprint', preparePrint);

    // مقداردهی اولیه ویژگی‌های اضافی
    initScrollProgress();
    initBackToTop();

    // اختیاری: مقداردهی اولیه بخش‌های قابل جمع شدن (برای فعال‌سازی کامنت را بردارید)
    // initCollapsibleSections();

    // به‌روزرسانی اولیه لینک ناوبری فعال
    updateActiveNavLink();

    console.log('ویژگی‌های تعاملی GDD مقداردهی اولیه شدند');
  }

  // اجرای مقداردهی اولیه وقتی DOM آماده شد
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // ==========================================================================
  // تزریق استایل‌های چاپ برای موارد خاص
  // ==========================================================================

  // اضافه کردن استایل‌های خاص چاپ به صورت داینامیک برای مرورگرهایی که نیاز دارند
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

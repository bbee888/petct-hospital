/**
 * 可访问性工具函数
 * 提供键盘导航、焦点管理和ARIA辅助功能
 */

/**
 * 管理模态框的焦点陷阱
 * @param {HTMLElement} element - 模态框元素
 */
export function trapFocus(element) {
  if (!element) return null;

  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  return function(event) {
    if (event.key === 'Tab') {
      if (event.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstFocusable) {
          event.preventDefault();
          lastFocusable.focus();
        }
      } else {
        // Tab
        if (document.activeElement === lastFocusable) {
          event.preventDefault();
          firstFocusable.focus();
        }
      }
    }
    
    // Escape键关闭模态框
    if (event.key === 'Escape') {
      event.preventDefault();
      // 触发关闭事件
      const closeEvent = new Event('close');
      element.dispatchEvent(closeEvent);
    }
  };
}

/**
 * 设置页面标题和描述，帮助屏幕阅读器用户
 * @param {string} title - 页面标题
 * @param {string} description - 页面描述
 */
export function setPageTitle(title, description = '') {
  document.title = title;
  
  // 更新主要标题
  const mainHeading = document.querySelector('h1');
  if (mainHeading) {
    mainHeading.textContent = title;
  }
  
  // 更新页面描述
  if (description) {
    let pageDescription = document.querySelector('meta[name="description"]');
    if (!pageDescription) {
      pageDescription = document.createElement('meta');
      pageDescription.name = 'description';
      document.head.appendChild(pageDescription);
    }
    pageDescription.content = description;
  }
}

/**
 * 管理表单的键盘快捷键
 * @param {HTMLElement} formElement - 表单元素
 * @param {Object} callbacks - 回调函数
 * @param {Function} callbacks.onSubmit - 提交回调
 * @param {Function} callbacks.onCancel - 取消回调
 * @param {Function} callbacks.onHelp - 帮助回调
 */
export function setupFormShortcuts(formElement, callbacks = {}) {
  const handleKeyDown = (event) => {
    // Ctrl/Cmd + Enter 提交表单
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      event.preventDefault();
      if (callbacks.onSubmit) {
        callbacks.onSubmit();
      }
    }
    
    // Ctrl/Cmd + H 显示帮助
    if ((event.ctrlKey || event.metaKey) && event.key === 'h') {
      event.preventDefault();
      if (callbacks.onHelp) {
        callbacks.onHelp();
      }
    }
    
    // Escape 取消
    if (event.key === 'Escape') {
      if (callbacks.onCancel) {
        event.preventDefault();
        callbacks.onCancel();
      }
    }
    
    // F1 显示帮助
    if (event.key === 'F1') {
      event.preventDefault();
      if (callbacks.onHelp) {
        callbacks.onHelp();
      }
    }
  };

  formElement.addEventListener('keydown', handleKeyDown);
  
  return () => {
    formElement.removeEventListener('keydown', handleKeyDown);
  };
}

/**
 * 为按钮添加加载状态指示器
 * @param {HTMLElement} button - 按钮元素
 * @param {boolean} isLoading - 是否正在加载
 */
export function setButtonLoadingState(button, isLoading) {
  if (!button) return;
  
  if (isLoading) {
    button.setAttribute('aria-busy', 'true');
    button.setAttribute('disabled', 'true');
    
    const originalText = button.textContent;
    button.setAttribute('data-original-text', originalText);
    button.textContent = '加载中...';
  } else {
    button.removeAttribute('aria-busy');
    button.removeAttribute('disabled');
    
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
      button.textContent = originalText;
      button.removeAttribute('data-original-text');
    }
  }
}

/**
 * 显示屏幕阅读器可访问的通知
 * @param {string} message - 消息内容
 * @param {'info' | 'success' | 'warning' | 'error'} type - 消息类型
 */
export function announceToScreenReader(message, type = 'info') {
  // 创建隐藏的live区域
  let liveRegion = document.getElementById('screen-reader-announcements');
  
  if (!liveRegion) {
    liveRegion = document.createElement('div');
    liveRegion.id = 'screen-reader-announcements';
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.style.cssText = `
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    `;
    document.body.appendChild(liveRegion);
  }
  
  // 设置role属性根据类型
  let role = 'status';
  if (type === 'error') role = 'alert';
  if (type === 'warning') role = 'alert';
  
  liveRegion.setAttribute('role', role);
  
  // 更新内容
  liveRegion.textContent = message;
  
  // 清除内容以便下一次更新
  setTimeout(() => {
    liveRegion.textContent = '';
  }, 1000);
}

/**
 * 检查颜色对比度是否满足可访问性要求
 * @param {string} foreground - 前景色 (十六进制)
 * @param {string} background - 背景色 (十六进制)
 * @returns {Object} 对比度结果
 */
export function checkColorContrast(foreground, background) {
  // 将十六进制颜色转换为RGB
  const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  };

  // 计算相对亮度
  const getLuminance = (rgb) => {
    const sRGB = (channel) => {
      channel = channel / 255;
      return channel <= 0.03928
        ? channel / 12.92
        : Math.pow((channel + 0.055) / 1.055, 2.4);
    };
    
    const R = sRGB(rgb.r);
    const G = sRGB(rgb.g);
    const B = sRGB(rgb.b);
    
    return 0.2126 * R + 0.7152 * G + 0.0722 * B;
  };

  const fgRgb = hexToRgb(foreground);
  const bgRgb = hexToRgb(background);
  
  if (!fgRgb || !bgRgb) {
    return { valid: false, ratio: 0, message: '无效的颜色格式' };
  }

  const fgLuminance = getLuminance(fgRgb);
  const bgLuminance = getLuminance(bgRgb);
  
  const lighter = Math.max(fgLuminance, bgLuminance);
  const darker = Math.min(fgLuminance, bgLuminance);
  
  const ratio = (lighter + 0.05) / (darker + 0.05);
  
  let passesAA = false;
  let passesAAA = false;
  let message = '';
  
  // WCAG 2.1标准
  if (ratio >= 4.5) {
    passesAA = true;
    if (ratio >= 7) {
      passesAAA = true;
      message = `对比度 ${ratio.toFixed(2)}:1 满足AAA级标准`;
    } else {
      message = `对比度 ${ratio.toFixed(2)}:1 满足AA级标准`;
    }
  } else {
    message = `对比度 ${ratio.toFixed(2)}:1 不满足可访问性标准`;
  }
  
  return {
    valid: passesAA,
    ratio,
    passesAA,
    passesAAA,
    message
  };
}

/**
 * 生成可访问的ID
 * @param {string} prefix - ID前缀
 * @returns {string} 唯一的ID
 */
export function generateAccessibleId(prefix = 'id') {
  return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
}

export default {
  trapFocus,
  setPageTitle,
  setupFormShortcuts,
  setButtonLoadingState,
  announceToScreenReader,
  checkColorContrast,
  generateAccessibleId
};
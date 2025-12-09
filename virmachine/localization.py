"""
本地化模块 - 多语言支持
Localization Module - Multi-language support
"""

from typing import Dict, Any

# 当前语言设置
_current_language = 'zh_CN'

# 文本翻译字典
_translations: Dict[str, Dict[str, str]] = {
    'zh_CN': {
        'prototype_created': '虚拟样机已创建',
        'component_added': '组件已添加',
        'component_removed': '组件已移除',
        'simulation_started': '仿真已开始',
        'simulation_completed': '仿真已完成',
        'test_passed': '测试通过',
        'test_failed': '测试失败',
        'loading': '加载中...',
        'saving': '保存中...',
        'error': '错误',
        'success': '成功',
        'warning': '警告',
    },
    'en_US': {
        'prototype_created': 'Virtual prototype created',
        'component_added': 'Component added',
        'component_removed': 'Component removed',
        'simulation_started': 'Simulation started',
        'simulation_completed': 'Simulation completed',
        'test_passed': 'Test passed',
        'test_failed': 'Test failed',
        'loading': 'Loading...',
        'saving': 'Saving...',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
    }
}


def set_language(language: str) -> None:
    """
    设置当前语言
    Set current language
    
    Args:
        language: 语言代码 (zh_CN 或 en_US) / Language code (zh_CN or en_US)
    """
    global _current_language
    if language in _translations:
        _current_language = language
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_language() -> str:
    """
    获取当前语言
    Get current language
    
    Returns:
        str: 当前语言代码 / Current language code
    """
    return _current_language


def get_text(key: str, default: str = None) -> str:
    """
    获取本地化文本
    Get localized text
    
    Args:
        key: 文本键 / Text key
        default: 默认文本 / Default text
        
    Returns:
        str: 本地化文本 / Localized text
    """
    if _current_language in _translations:
        return _translations[_current_language].get(key, default or key)
    return default or key


def add_translation(language: str, key: str, value: str) -> None:
    """
    添加翻译文本
    Add translation text
    
    Args:
        language: 语言代码 / Language code
        key: 文本键 / Text key
        value: 翻译值 / Translation value
    """
    if language not in _translations:
        _translations[language] = {}
    _translations[language][key] = value

import os
import json

class I18n:
    _instance = None
    _translations = {}
    _current_language = 'zh_CN'  # 默认语言
    
    @classmethod
    def get_app_language(cls):
        """获取 ComfyUI 的当前语言设置"""
        try:
            # 尝试从 ComfyUI 配置文件获取语言设置
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '..', '..', 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('language', 'en_US')
        except:
            pass
        return 'en_US'

    @classmethod
    def get_text(cls, key, default_text="", app_language=False):
        """
        获取翻译文本
        :param key: 翻译键
        :param default_text: 默认文本
        :param app_language: 是否使用 ComfyUI 的语言设置
        :return: 翻译后的文本
        """
        if app_language:
            language = cls.get_app_language()
        else:
            language = cls._current_language

        # 如果语言不存在，加载对应的翻译文件
        if language not in cls._translations:
            cls.load_translations(language)

        # 获取翻译
        translations = cls._translations.get(language, {})
        return translations.get(key, default_text)

    @classmethod
    def load_translations(cls, language):
        """加载指定语言的翻译文件"""
        try:
            translation_file = os.path.join(
                os.path.dirname(__file__),
                'translations',
                f'{language}.json'
            )
            if os.path.exists(translation_file):
                with open(translation_file, 'r', encoding='utf-8') as f:
                    cls._translations[language] = json.load(f)
        except:
            cls._translations[language] = {} 
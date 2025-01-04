class I18n:
    _current_lang = 'zh'  # 默认中文
    
    translations = {
        'zh': {
            'regex_error': '正则表达式错误: {}',
            'waiting_input': '等待输入文本',
            'separator_placeholder': '支持正则表达式和转义字符，如: ,|\\n。使用特殊字符请关闭正则开关'
        },
        'en': {
            'regex_error': 'Regex Error: {}',
            'waiting_input': 'Waiting for input text',
            'separator_placeholder': 'Supports regex and escape chars, e.g.: ,|\\n. Turn off regex for special chars'
        }
    }
    
    @classmethod
    def set_language(cls, lang):
        if lang in cls.translations:
            cls._current_lang = lang
    
    @classmethod
    def get_text(cls, key, *args):
        lang_dict = cls.translations.get(cls._current_lang, cls.translations['en'])
        text = lang_dict.get(key, '')
        if args:
            return text.format(*args)
        return text 
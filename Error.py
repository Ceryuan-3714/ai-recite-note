class InitializationError(Exception):
    """自定义异常，用于处理初始化相关的错误"""

    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors  # 可以添加更多的自定义属性

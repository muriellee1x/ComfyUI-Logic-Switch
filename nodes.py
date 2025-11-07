"""
随机字符串选择节点
"""

import random


class RandomStringSelector:
    """
    随机字符串选择器
    可以输入最多6个字符串，每个都有一个开关控制是否参与随机选择
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        # 预定义6组输入
        return {
            "required": {},
            "optional": {
                "string1": ("STRING", {"default": "", "multiline": False}),
                "enable1": ("BOOLEAN", {"default": True}),
                "string2": ("STRING", {"default": "", "multiline": False}),
                "enable2": ("BOOLEAN", {"default": True}),
                "string3": ("STRING", {"default": "", "multiline": False}),
                "enable3": ("BOOLEAN", {"default": True}),
                "string4": ("STRING", {"default": "", "multiline": False}),
                "enable4": ("BOOLEAN", {"default": True}),
                "string5": ("STRING", {"default": "", "multiline": False}),
                "enable5": ("BOOLEAN", {"default": True}),
                "string6": ("STRING", {"default": "", "multiline": False}),
                "enable6": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_string",)
    FUNCTION = "select_random"
    CATEGORY = "logic"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 返回一个随机值，强制每次都重新执行
        return random.random()
    
    def select_random(self, **kwargs):
        """
        从启用的字符串中随机选择一个
        """
        # 收集所有启用的非空字符串
        enabled_strings = []
        
        # 检查所有6个输入
        for i in range(1, 7):
            string_key = f"string{i}"
            enable_key = f"enable{i}"
            
            string_value = kwargs.get(string_key, "")
            enable_value = kwargs.get(enable_key, True)  # 默认启用
            
            # 只添加启用的且非空的字符串
            if enable_value and string_value and string_value.strip():
                enabled_strings.append(string_value)
                print(f"[RandomStringSelector] 添加候选: string{i} = '{string_value}'")
        
        print(f"[RandomStringSelector] 总共有 {len(enabled_strings)} 个候选字符串: {enabled_strings}")
        
        # 如果没有启用的字符串，返回空字符串
        if not enabled_strings:
            print("[RandomStringSelector] 没有启用的字符串，返回空")
            return ("",)
        
        # 随机选择一个字符串
        selected = random.choice(enabled_strings)
        print(f"[RandomStringSelector] 随机选择了: '{selected}'")
        
        return (selected,)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "RandomStringSelector": RandomStringSelector,
}

# 显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomStringSelector": "random string selector",
}


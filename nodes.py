import random


class RandomStringSelector:
    """
    随机字符串选择器
    可以动态控制输入数量，每个字符串都有一个开关控制是否参与随机选择
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_nums": ("INT", {
                    "default": 3, 
                    "min": 1, 
                    "max": 20,
                    "step": 1,
                    "display": "number"
                }),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "comma_separated_string": ("STRING",),
                "enable_comma_separated": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("selected_string",)
    FUNCTION = "select_random"
    CATEGORY = "logic"
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 返回 NaN 强制每次都重新执行，即使前序节点没有变化
        return float("nan")
    
    def select_random(self, input_nums, seed, **kwargs):
        """
        从启用的字符串中随机选择一个
        支持两种输入方式：
        1. 逗号分隔的字符串（comma_separated_string）- 启用后会忽略其他输入
        2. 动态string输入（string1-N）
        """
        random.seed(seed)
        
        # 收集所有启用的非空字符串
        enabled_strings = []
        
        # 获取逗号分隔模式开关
        enable_comma_separated = kwargs.get("enable_comma_separated", False)
        comma_separated = kwargs.get("comma_separated_string", "")
        
        # 方式1：处理逗号分隔的字符串（如果启用）
        if enable_comma_separated and comma_separated and comma_separated.strip():
            # 按逗号分隔并清理空白
            parts = [part.strip() for part in comma_separated.split(",")]
            # 过滤掉空字符串
            parts = [part for part in parts if part]
            enabled_strings.extend(parts)
            print(f"[RandomStringSelector] 逗号分隔模式已启用，从字符串添加 {len(parts)} 个候选: {parts}")
            print(f"[RandomStringSelector] 忽略其他 string 输入")
        else:
            # 方式2：处理动态输入的string1-N（逗号分隔模式未启用时）
            if enable_comma_separated:
                print("[RandomStringSelector] 逗号分隔模式已启用，但输入为空，将使用 string 输入")
            
            for i in range(1, input_nums + 1):
                string_key = f"string{i}"
                enable_key = f"enable{i}"
                
                string_value = kwargs.get(string_key, "")
                enable_value = kwargs.get(enable_key, True)
                
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
    "RandomStringSelector": "Random String Selector",
}


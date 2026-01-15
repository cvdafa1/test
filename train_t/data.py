import random
from typing import Dict, List


def expand_samples(rules: Dict[str, List[str]],
                   expansion_factor: int = 5) -> tuple:
    """
    简单泛化样本扩展函数

    Args:
        rules: 原始规则字典
        expansion_factor: 扩展倍数（大约）

    Returns:
        扩展后的样本字典
    """
    expanded_rules = {}

    # 扩展变化模板
    variations = [
        lambda x: x,  # 保持原样
        lambda x: x + '？',  # 添加中文问号
        lambda x: x + '?',  # 添加英文问号
        lambda x: x + '呀',  # 添加语气词
        lambda x: x + '啊',
        lambda x: x + '呢',
        lambda x: '请' + x,  # 添加请求词
        lambda x: '我想' + x,
        lambda x: '可以' + x + '吗',
        lambda x: '请问' + x + '？',
        lambda x: '帮我' + x,
        lambda x: '我想知道' + x,
        lambda x: '告诉我' + x,
    ]

    # 添加简短语气
    short_modifiers = ['', '呀', '啊', '呢', '哈', '哦']

    for category, samples in rules.items():
        expanded_set = set(samples)  # 用set去重

        # 为每个原始样本生成多个变体
        for sample in samples:
            # 基本变体
            for var_func in variations:
                expanded_set.add(var_func(sample))

            # 添加带标点变化的简短形式
            for mod in short_modifiers:
                if mod:  # 避免重复添加原始样本
                    expanded_set.add(sample + mod)
                    expanded_set.add(sample + mod + '？')
                    expanded_set.add(sample + mod + '?')

        # 确保样本数量控制在合理范围
        expanded_list = list(expanded_set)
        target_size = min(len(samples) * expansion_factor, 200)  # 最多200条

        if len(expanded_list) > target_size:
            # 随机抽样
            expanded_list = random.sample(expanded_list, target_size)
        elif len(expanded_list) < len(samples) * 3:
            # 如果扩展不够，再添加一些组合
            for _ in range(min(20, target_size - len(expanded_list))):
                combo = random.choice(samples) + random.choice(short_modifiers)
                expanded_list.append(combo)

        expanded_rules[category] = expanded_list
    texts = []
    labels = []
    for k, v in expanded_rules.items():
        for sample in v:
            texts.append(sample)
            labels.append(k)
    return texts, labels


# 使用示例
if __name__ == "__main__":
    # 原始规则
    rules = {
        'greeting': ['你好', 'hello', 'hi', '您好', '早上好', '晚上好', '嗨'],
        'weather': ['天气', '下雨', '温度', '气温', '晴天', '阴天'],
        'time': ['时间', '几点', '日期', '星期', '钟点'],
        'joke': ['笑话', '搞笑', '幽默', '笑一笑', '段子'],
        'music': ['音乐', '歌曲', '听歌', '播放', '唱歌'],
        'farewell': ['再见', '拜拜', '再会', '走了', '告辞']
    }

    # 执行扩展
    text, labels = expand_samples(rules, expansion_factor=1000)
    print(text)
    print(labels)



# # 更简单的版本（如果只需要基本扩展）
# def simple_expand(rules: Dict[str, List[str]]) -> Dict[str, List[str]]:
#     """最简单直接的扩展函数"""
#     expanded = {}
#
#     for category, samples in rules.items():
#         new_samples = []
#
#         for sample in samples:
#             # 添加几种简单变化
#             new_samples.extend([
#                 sample,  # 原样
#                 sample + '？',  # 中文问号
#                 sample + '?',  # 英文问号
#                 '请' + sample,  # 加请
#                 '我想' + sample,  # 加我想
#                 sample + '呀',  # 加语气词
#                 sample + '啊',
#                 '可以' + sample + '吗',  # 变成问句
#                 '告诉我' + sample,  # 加告诉我
#                 sample + '怎么样',  # 加怎么样
#             ])
#
#         # 去重
#         expanded[category] = list(set(new_samples))
#
#     return expanded
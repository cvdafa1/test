class SimpleIntentRecognizer:
    """基于规则的简单意图识别器"""

    def __init__(self):
        # 定义意图规则
        self.rules = {
            'greeting': ['你好', 'hello', 'hi', '您好', '早上好', '晚上好', '嗨'],
            'weather': ['天气', '下雨', '温度', '气温', '晴天', '阴天'],
            'time': ['时间', '几点', '日期', '星期', '钟点'],
            'joke': ['笑话', '搞笑', '幽默', '笑一笑', '段子'],
            'music': ['音乐', '歌曲', '听歌', '播放', '唱歌'],
            'farewell': ['再见', '拜拜', '再会', '走了', '告辞']
        }

    def recognize(self, text):
        """基于规则识别意图"""
        text = text.lower()

        # 计算每个意图的匹配分数
        scores = {}
        for intent, keywords in self.rules.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1

            # 计算匹配度（匹配关键词数/关键词总数）
            match_ratio = score / len(keywords) if keywords else 0
            scores[intent] = match_ratio

        # 找到最佳匹配意图
        best_intent = max(scores.items(), key=lambda x: x[1])

        if best_intent[1] > 0:  # 如果有匹配
            return best_intent[0], best_intent[1]
        else:
            return 'unknown', 0.0

if __name__ == '__main__':

    print("=== 基于规则的意图识别 ===")
    simple_recognizer = SimpleIntentRecognizer()

    test_inputs = [
        "你好，今天天气好吗？",
        "我想听周杰伦的歌",
        "现在几点了？",
        "说个笑话听听",
        "再见啦"
    ]

    for text in test_inputs:
        intent, score = simple_recognizer.recognize(text)
        print(f"输入: {text}")
        print(f"识别结果: {intent} (置信度: {score})")
        print()
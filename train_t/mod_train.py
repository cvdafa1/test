import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

from train_t.data import expand_samples


class MLIntentRecognizer:
    # 基于训练的意图识别
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = LogisticRegression(max_iter=1000)
        self.intent_labels = {}

    def create_training_data(self):
        """
        创建训练数据
        实际应用中应该从数据库或文件加载
        """
        rules = {
            'greeting': ['你好', 'hello', 'hi', '您好', '早上好', '晚上好', '嗨'],
            'weather': ['天气', '下雨', '温度', '气温', '晴天', '阴天'],
            'time': ['时间', '几点', '日期', '星期', '钟点'],
            'joke': ['笑话', '搞笑', '幽默', '笑一笑', '段子'],
            'music': ['音乐', '歌曲', '听歌', '播放', '唱歌'],
            'farewell': ['再见', '拜拜', '再会', '走了', '告辞']
        }
        # 训练数据：文本和对应的意图标签
        texts, labels = expand_samples(rules, expansion_factor=100000)

        return texts, labels

    def train(self):
        """训练模型"""
        print("开始训练意图识别模型...")

        # 获取训练数据
        texts, labels = self.create_training_data()

        # 创建标签映射
        unique_labels = list(set(labels))
        self.intent_labels = {i: label for i, label in enumerate(unique_labels)}
        self.label_to_idx = {label: i for i, label in enumerate(unique_labels)}

        # 将标签转换为数字
        y = np.array([self.label_to_idx[label] for label in labels])

        # 特征提取
        X = self.vectorizer.fit_transform(texts)

        # 训练分类器
        self.classifier.fit(X, y)

        print(f"模型训练完成，共有 {len(unique_labels)} 个意图类别")
        return self

    def predict(self, text):
        """预测意图"""
        # 特征转换
        features = self.vectorizer.transform([text])

        # 预测
        proba = self.classifier.predict_proba(features)[0]
        pred_idx = np.argmax(proba)
        confidence = proba[pred_idx]

        # 获取意图标签
        intent = self.intent_labels.get(pred_idx, 'unknown')

        return intent, confidence

    def save_model(self, filename="intent_model.pkl"):
        """保存模型"""
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'intent_labels': self.intent_labels,
            'label_to_idx': self.label_to_idx
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"模型已保存到 {filename}")

    def load_model(self, filename="intent_model.pkl"):
        """加载模型"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)

        self.vectorizer = model_data['vectorizer']
        self.classifier = model_data['classifier']
        self.intent_labels = model_data['intent_labels']
        self.label_to_idx = model_data['label_to_idx']
        print(f"模型已从 {filename} 加载")


# 使用示例
if __name__ == "__main__":
    # 方法2：使用机器学习方法
    print("\n=== 基于机器学习的意图识别 ===")

    # 训练模型
    ml_recognizer = MLIntentRecognizer()
    ml_recognizer.train()

    # 测试预测
    test_texts = [
        "你好啊朋友",
        "明天会下雨吗",
        "现在的时间是多少",
        "播放一首音乐",
        "我要走了再见"
    ]

    for text in test_texts:
        intent, confidence = ml_recognizer.predict(text)
        print(f"输入: '{text}'")
        print(f"预测意图: {intent}, 置信度: {confidence:.2f}")
        print()

    # 保存模型
    ml_recognizer.save_model()

    # 测试加载模型
    print("\n=== 测试加载保存的模型 ===")
    new_recognizer = MLIntentRecognizer()
    new_recognizer.load_model("intent_model.pkl")

    test_text = "你好，现在几点了？"
    intent, confidence = new_recognizer.predict(test_text)
    print(f"加载模型测试 - 输入: '{test_text}'")
    print(f"预测意图: {intent}, 置信度: {confidence:.2f}")
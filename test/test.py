import re
from collections import Counter
import sys


def clean_word(word):
    """清洗单词：转换为小写并移除非字母字符"""
    return re.sub(r'[^a-zA-Z]', '', word).lower()


def count_word_frequency(file_path):
    """统计文件中的词频"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"❌ 错误：找不到文件 '{file_path}'")
        return None
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as file:
                text = file.read()
        except Exception as e:
            print(f"❌ 读取文件时出错：{e}")
            return None
    except Exception as e:
        print(f"❌ 读取文件时出错：{e}")
        return None

    # 使用正则表达式分割单词（包括连字符连接的单词）
    words = re.findall(r"[a-zA-Z'-]+", text)

    # 清洗单词并过滤掉空字符串和纯标点符号
    cleaned_words = []
    print(words)
    for word in words:
        cleaned = clean_word(word)
        if cleaned:  # 只保留非空的清洗后单词
            cleaned_words.append(cleaned)

    # 统计词频
    word_counts = Counter(cleaned_words)

    return word_counts


def display_word_frequency(word_counts, top_n=20):
    """显示词频统计结果"""
    if not word_counts:
        print("❌ 没有可显示的词频数据")
        return

    total_words = sum(word_counts.values())
    unique_words = len(word_counts)

    print("\n" + "=" * 60)
    print("                    📊 词频统计结果")
    print("=" * 60)
    print(f"📝 总单词数：{total_words}")
    print(f"🌐 不同单词数：{unique_words}")
    print(f"🔝 显示前 {top_n} 个最常见单词")
    print("-" * 60)

    # 显示前N个最常见的单词
    for i, (word, count) in enumerate(word_counts.most_common(top_n), 1):
        percentage = (count / total_words) * 100
        print(f"{i:2d}. {word:<15} {count:>4} 次 ({percentage:.1f}%)")

    print("-" * 60)

    # 如果有更多单词，显示统计信息
    if unique_words > top_n:
        print(f"ℹ️  还有 {unique_words - top_n} 个单词未显示（出现次数较少）")


def save_word_frequency(word_counts, output_file=None):
    """将词频统计结果保存到文件"""
    if not word_counts:
        print("❌ 没有可保存的词频数据")
        return

    if output_file is None:
        output_file = "word_frequency_result.txt"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("词频统计结果\n")
            f.write("=" * 50 + "\n\n")

            total_words = sum(word_counts.values())
            unique_words = len(word_counts)

            f.write(f"总单词数：{total_words}\n")
            f.write(f"不同单词数：{unique_words}\n\n")

            f.write("单词频率排名：\n")
            f.write("-" * 30 + "\n")

            for i, (word, count) in enumerate(word_counts.most_common(), 1):
                f.write(f"{i:2d}. {word:<15} {count:>4} 次\n")

        print(f"✅ 词频统计结果已保存到文件：{output_file}")

    except Exception as e:
        print(f"❌ 保存文件时出错：{e}")


def interactive_mode():
    """交互模式"""
    clear_screen()
    print("=" * 50)
    print("           📖 文件词频统计工具")
    print("=" * 50)

    while True:
        file_path = input("\n📂 请输入要分析的文件路径: ").strip()

        if not file_path:
            print("❌ 文件路径不能为空！")
            continue

        word_counts = count_word_frequency(file_path)

        if word_counts is None:
            retry = input("是否重新输入文件路径？(y/n): ").strip().lower()
            if retry not in ['y', 'yes', '是']:
                break
            continue

        # 显示统计结果
        display_word_frequency(word_counts)

        # 询问是否保存结果
        save_choice = input("\n💾 是否保存统计结果到文件？(y/n): ").strip().lower()
        if save_choice in ['y', 'yes', '是']:
            output_file = input("请输入保存文件名（直接回车使用默认名 word_frequency_result.txt）: ").strip()
            if not output_file:
                output_file = "word_frequency_result.txt"
            save_word_frequency(word_counts, output_file)

        # 询问是否继续
        continue_choice = input("\n🔄 是否分析其他文件？(y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes', '是']:
            break

    print("\n👋 感谢使用词频统计工具！")


def command_line_mode():
    """命令行模式（支持参数）"""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        word_counts = count_word_frequency(file_path)

        if word_counts is not None:
            print("\n" + "=" * 60)
            print("                    📊 词频统计结果")
            print("=" * 60)
            display_word_frequency(word_counts)

            if len(sys.argv) > 2 and sys.argv[2] == '--save':
                output_file = sys.argv[3] if len(sys.argv) > 3 else "word_frequency_result.txt"
                save_word_frequency(word_counts, output_file)


def clear_screen():
    """清屏函数"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """主函数"""
    print("📖 文件词频统计工具")
    print("请选择运行模式：")
    print("1. 交互模式（推荐，逐步引导）")
    print("2. 命令行模式（直接传入文件路径参数）")

    while True:
        choice = input("\n请输入选择 (1 或 2，直接回车默认为1): ").strip()

        if not choice:
            choice = '1'

        if choice == '1':
            interactive_mode()
            break
        elif choice == '2':
            command_line_mode()
            break
        else:
            print("❌ 无效选择，请输入 1 或 2")


if __name__ == "__main__":
    # 如果直接在命令行中传入了文件路径参数，则使用命令行模式
    if len(sys.argv) > 1 and not sys.argv[1].isdigit():
        command_line_mode()
    else:
        main()
import pandas as pd
from datetime import datetime, timedelta
import os


def validate_mold_change_data(csv_file_path, mold_change_date):
    """
    验证CSV文件是否满足换模后至少三个月以上的数据要求

    参数:
    csv_file_path (str): CSV文件路径
    mold_change_date (str): 换模时间，格式为 "YYYY-MM-DD"
    """
    try:
        # 2. 读取CSV文件
        df = pd.read_csv(csv_file_path)
        first_row = df.iloc[0]
        # 1. 需要检查的列名
        for col in df.columns:
            if not isinstance(col, str) or not isinstance(first_row[col], str):
                raise ValueError(f"第1或第2行中列'{col}'不是位号名或描述")
        required_columns = ['电流', '槽温', '碱浓度', '单元槽电压']
        missing_columns = [col for col in required_columns if col not in first_row.to_list()]
        if missing_columns:
            raise ValueError(f"数据框缺少以下列: {missing_columns}")
        # 2. 取出除前1行之外的数据
        data_part = df.iloc[2:].reset_index(drop=True)
        if data_part.empty:
            raise ValueError("数据部分为空")
        # 3. 检查第一列是否可以转换为时间类型
        try:
            pd.to_datetime(data_part.iloc[:, 0])
        except Exception as e:
            raise ValueError("数据部分的第一列无法解析为时间") from e

        # 4. 检查其余列是否为浮点数
        for col in data_part.columns[1:]:
            try:
                # 尝试将每列转为 float 类型
                pd.to_numeric(data_part[col], errors='raise')
            except Exception as e:
                raise ValueError(f"列 '{col}' 数据格式有问题") from e

        date_column_name = df.columns[0]
        df[date_column_name] = pd.to_datetime(df[date_column_name], errors='coerce')
        df = df.dropna(subset=[date_column_name])
        # 5. 获取数据的日期范围
        max_date = df[date_column_name].max()
        # 6. 解析换模日期
        mold_change_dt = datetime.strptime(mold_change_date, '%Y-%m-%d')
        # 7. 计算最小要求的结束日期（换模日期+3个月）
        min_required_end_date = mold_change_dt + timedelta(days=90)  # 近似3个月
        # 8. 验证数据是否满足条件
        if max_date < mold_change_dt:
            return f"数据结束日期({max_date.strftime('%Y-%m-%d')})早于换模日期({mold_change_date})"

        # 计算换模后的数据天数
        post_mold_data = df[df[date_column_name] >= mold_change_dt]
        if len(post_mold_data) == 0:
            return "没有换模日期之后的数据"

        post_mold_start = post_mold_data[date_column_name].min()
        post_mold_end = post_mold_data[date_column_name].max()

        # 新增验证：检查换模后的数据是否保证每个月至少有一条记录
        def validate_monthly_data_coverage(start_date, end_date, data_df, date_col):
            """验证在指定时间范围内每个月是否至少有一条数据"""
            # 创建从开始到结束的所有月份
            months_required = []
            current = start_date.replace(day=1)  # 从开始月份的第一天算起

            while current <= end_date:
                months_required.append(current)
                # 移动到下一个月
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)

            # 检查每个月是否有数据
            missing_months = []
            for month_start in months_required:
                # 计算该月的结束日期（下个月第一天减一天）
                if month_start.month == 12:
                    next_month = month_start.replace(year=month_start.year + 1, month=1)
                else:
                    next_month = month_start.replace(month=month_start.month + 1)
                month_end = next_month - timedelta(days=1)

                # 检查该月是否有数据
                month_data = data_df[
                    (data_df[date_col] >= month_start) &
                    (data_df[date_col] <= month_end)
                    ]

                if len(month_data) == 0:
                    missing_months.append(month_start.strftime('%Y-%m'))

            return missing_months

        # 执行月度数据覆盖验证
        missing_months = validate_monthly_data_coverage(post_mold_start, post_mold_end, post_mold_data,
                                                        date_column_name)

        # 9. 计算与3个月要求的差距
        days_short = (min_required_end_date - post_mold_end).days
        if days_short <= 0:
            # 满足条件
            if missing_months:
                return f"数据验证通过！换模后数据，满足至少90天的要求。但以下月份缺少数据：{', '.join(missing_months)}"
            else:
                return f"数据验证通过！满足至少90天的要求，且每月都有数据覆盖"
        else:
            result_msg = f"数据不足：需要至少90天，还差{days_short}天"
            if missing_months:
                result_msg += f"。另外以下月份缺少数据：{', '.join(missing_months)}"
            return result_msg
    except Exception as e:
        return f"验证过程中发生错误: {str(e)}"




# 使用示例
if __name__ == "__main__":
    # 示例用法
    csv_file = ("im.csv")  # 替换为您的CSV文件路径
    mold_change_date = "2025-7-10"

    # 执行验证
    validation_result = validate_mold_change_data(csv_file, mold_change_date)
    print(validation_result)


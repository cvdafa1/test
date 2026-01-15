def try_parse_datetime(val):
    """
    尝试将纳秒级时间戳转化为正常日期时间
    """
    if isinstance(val, int) and 1e15 < val < 2e20:
        try:
            # 转换为日期时间格式
            return pd.to_datetime(val).isoformat()
        except Exception:
            return val  # 转换失败时返回原值
    return val  # 非时间戳时返回原值
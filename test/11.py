def dict_to_markdown_table(data):
    if not data:
        return ""

    max_length = max(len(value) if isinstance(value, list) else 1 for value in data.values())
    expanded_data = {}
    for key, value in data.items():
        if isinstance(value, list):
            expanded_value = value + [''] * (max_length - len(value))
        else:
            expanded_value = [value] * max_length
        expanded_data[key] = expanded_value

    keys = list(expanded_data.keys())
    column_widths = {key: max(len(str(key)), max(len(str(item)) for item in expanded_data[key])) for key in keys}

    headers = "| " + " | ".join(f"{key:<{column_widths[key]}}" for key in keys) + " |"
    separators = "| " + " | ".join(["-" * column_widths[key] for key in keys]) + " |"

    table_rows = []
    for i in range(max_length):
        row = "| " + " | ".join(f"{str(expanded_data[key][i]):<{column_widths[key]}}" for key in keys) + " |"
        table_rows.append(row)

    markdown_table = f"{headers}\n{separators}\n" + "\n".join(table_rows)

    return markdown_table



dictionary = {'目标位号': "HGLZM01.AIC2104.DACA.PV",
                    '控制位号': "HGLZM01.AIC2104.DACA.PV",
                    '数据得分': "10",
                    '数据长度（天）': "18",
                    '缺失值': "0",
                    'PV&MV相关性': "-1"}

md_table = dict_to_markdown_table(dictionary)




str =  """
根据提供的数据质量分析结果，目标变量为 HGLZM01.AIC2104.DACA.PV，控制变量为 HGLZM01.AIC2104.PIDA.OP。数据分析显示，该数据集的质量评分为 9分（满分100），评分较低，主要原因为 数据量较少，仅覆盖8天的时间范围，这在评估数据质量时是一个关键限制因素，可能导致模型训练或分析结果的稳定性不足。此外，数据质量评分标志（tag）为 1，表明当前问题的核心是 数据数量太少，而非缺失值或异常值问题。数据集中无缺失值（max_nan=0），且异常值比例为 0.0，说明数据在完整性和准确性方面表现良好。

从控制效果分析角度看，PV与MV之间的相关性为 -1，表明控制变量与被控变量之间存在 完全负相关关系，即控制变量的变化与目标变量的变化方向完全相反。这在理论上可能是合理的，但在实际工业控制系统中，完全负相关的情况较为少见，建议进一步核查控制逻辑是否正常，是否存在数据处理或采样过程中的偏差。

总结建议：

当前数据质量整体较差（评分9），主要受限于数据长度不足（8天），建议延长数据采集周期，获取更长时间范围内的数据以提升分析的可信度和稳定性。同时，尽管控制变量与目标变量之间呈现完全负相关，但需结合工艺背景进一步验证控制逻辑的合理性，确保数据与实际控制行为一致。"""

str2 = """
AI可控性分析结果显示：该系统处于“长时滞、非时变”场景，适合采用超级控制方案。数据漂移检测结果表明存在数据漂移现象，而特征漂移检测则发现特征重要性发生了显著变化。这提示系统输入输出关系可能存在偏移，需对模型进行重新校准或更新。整体来看，系统当前的负相关性较强（系数为-1），表明控制变量与目标变量之间存在明确但可能需要优化的反向响应关系。建议优先考虑数据漂移的补偿机制，并结合特征重要性变化趋势，对AI控制策略进行动态调整和优化，以提升系统稳定性和控制精度。
"""

md_table1 = """| 长时滞 | 短时滞 | 时变 | 非时变 | 推荐方法   |\n| — | — | – | — | ------ |\n| 是   | 否   | 否  | 是   | <超级控制> |"""
md_table2 = """| 数据漂移检测 | 特征漂移检测         |\n| ------ | -------------- |\n| 数据漂移   | 检测到特征重要性发生显著变化 |"""
str5 = """关键影响因素分析结果显示：从提供的12个候选特征中，筛选出了与目标过程密切相关的关键影响因素。其中，特征 LIC_XD141.PID1.PV 的重要度最高（1），表明该变量在过程中具有核心影响力；其次是 PI_XD141B.AI1.PV（2）和 FIQ_XE142A.INTEGX1.OUT（3），显示出较高的相关性。整体来看，前5个特征的重要度均在5以内，集中体现了对系统行为的主导作用。其余特征虽然重要度逐步下降，但仍在模型构建中具有一定参考价值。综上所述，关键变量分布较为集中，前5位特征可作为重点监控与优化对象，有助于提升过程控制精度和系统响应效率。"""
md_table3 = """| 特征位号                   | 重要度 |\n| ---------------------- | — |\n| LIC_XD141.PID1.PV      | 1   |\n| PI_XD141B.AI1.PV       | 2   |\n| FIQ_XE142A.INTEGX1.OUT | 3   |\n| LIC_XT141.PID1.PV      | 4   |\n| PIC_XE141.PID1.SV      | 5   |\n| TT_XD142B.AI1.PV       | 6   |\n| TI_6003.AI1.PV         | 7   |\n| LIC_XT141.PID1.MV      | 8   |\n| TT_XD141A.AI1.PV       | 9   |\n| LIC_XD140.PID1.MV      | 10  |\n| FIC_XE142A.PID1.PV     | 11  |"""

markdown1 = f"""
## 数据质量分析

### 分析结果评估：
{str}

{md_table}


## AI可控性评估

### 评估结果：
{str2}

### 场景判断结果：
{md_table1}

### 数据检测结果：
{md_table2}


## 关键影响因素分析

### 分析结果：
{str5}

{md_table3}

"""

markdown1 = markdown1.format(str=str, md_table=md_table, str2=str2, md_table1=md_table1, md_table2=md_table2, str5=str5, md_table3=md_table3)
print(markdown1)





# AIMETA P=JSON工具_JSON解析和修复|R=安全解析_格式修复|NR=不含业务逻辑|E=parse_json_safely|X=internal|A=工具函数|D=json|S=none|RD=./README.ai
import re


def remove_think_tags(raw_text: str) -> str:
    """移除 <think></think> 标签，避免污染结果。"""
    if not raw_text:
        return raw_text
    return re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()


def unwrap_markdown_json(raw_text: str) -> str:
    """从 Markdown 或普通文本中提取 JSON 字符串。"""
    if not raw_text:
        return raw_text

    trimmed = raw_text.strip()

    fence_match = re.search(r"```(?:json|JSON)?\s*(.*?)\s*```", trimmed, re.DOTALL)
    if fence_match:
        candidate = fence_match.group(1).strip()
        if candidate:
            return candidate

    json_start_candidates = [idx for idx in (trimmed.find("{"), trimmed.find("[")) if idx != -1]
    if json_start_candidates:
        start_idx = min(json_start_candidates)
        closing_brace = trimmed.rfind("}")
        closing_bracket = trimmed.rfind("]")
        end_idx = max(closing_brace, closing_bracket)
        if end_idx != -1 and end_idx > start_idx:
            candidate = trimmed[start_idx : end_idx + 1].strip()
            if candidate:
                return candidate

    return trimmed


def sanitize_json_like_text(raw_text: str) -> str:
    """对可能含有未转义换行/引号的 JSON 文本进行清洗。"""
    if not raw_text:
        return raw_text

    result = []
    in_string = False
    escape_next = False
    length = len(raw_text)
    i = 0
    while i < length:
        ch = raw_text[i]
        if in_string:
            if escape_next:
                result.append(ch)
                escape_next = False
            elif ch == "\\":
                result.append(ch)
                escape_next = True
            elif ch == '"':
                j = i + 1
                while j < length and raw_text[j] in " \t\r\n":
                    j += 1

                if j >= length or raw_text[j] in "}]":
                    in_string = False
                    result.append(ch)
                elif raw_text[j] in ",:":
                    in_string = False
                    result.append(ch)
                else:
                    result.extend(["\\", '"'])
            elif ch == "\n":
                result.extend(["\\", "n"])
            elif ch == "\r":
                result.extend(["\\", "r"])
            elif ch == "\t":
                result.extend(["\\", "t"])
            else:
                result.append(ch)
        else:
            if ch == '"':
                in_string = True
            result.append(ch)
        i += 1

    return "".join(result)

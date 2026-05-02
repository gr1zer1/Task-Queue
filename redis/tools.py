from typing import Any


def encode_command(*args) -> bytes:
    commands = args
    len_command = f"*{len(commands)}\r\n"
    main_line:str = ""

    for command in commands:
        line = f"${len(command.encode())}\r\n{command}\r\n"
        main_line += line
    
    return (len_command + main_line).encode()

def _parse(lines: list[str], i: int) -> tuple[Any, int]:
    if not lines[i]:
        return None, i + 1
    
    match lines[i][0]:
        case "+":
            return lines[i][1:], i + 1
        case ":":
            return int(lines[i][1:]), i + 1
        case "-":
            raise Exception(lines[i][1:])
        case "$":
            return lines[i + 1], i + 2
        case "*":
            count = int(lines[i][1:])
            i += 1
            result = []
            for _ in range(count):
                val, i = _parse(lines, i)
                result.append(val)
            return result, i


def decode_response(data: bytes) -> Any:
    lines = data.decode().split("\r\n")
    value, _ = _parse(lines, 0)
    return value
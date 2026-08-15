import json
import os

log_file = r'C:\Users\legion-5pro\.gemini\antigravity-ide\brain\3a6d699f-d51c-4b1c-9008-3b3d21c7ccc8\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

recovered_account = False
for line in reversed(lines):
    data = json.loads(line)
    if 'tool_calls' in data:
        for tc in data['tool_calls']:
            if tc.get('name') == 'default_api:write_to_file':
                args = tc.get('arguments', tc.get('args', {}))
                if isinstance(args, str):
                    args = json.loads(args)
                if 'account.html' in args.get('TargetFile', '') and not recovered_account:
                    with open(args['TargetFile'], 'w', encoding='utf-8') as out:
                        out.write(args['CodeContent'])
                    print("Recovered", args['TargetFile'])
                    recovered_account = True
                    break
        if recovered_account:
            break

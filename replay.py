import json
import os

log_file = r'C:\Users\legion-5pro\.gemini\antigravity-ide\brain\3a6d699f-d51c-4b1c-9008-3b3d21c7ccc8\.system_generated\logs\transcript_full.jsonl'
with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines:
    data = json.loads(line)
    if 'tool_calls' in data:
        for tc in data['tool_calls']:
            name = tc.get('name') or tc.get('function', {}).get('name')
            if name == 'write_to_file' or name == 'default_api:write_to_file':
                args = tc.get('arguments', tc.get('args', {}))
                if isinstance(args, str): args = json.loads(args)
                target = args.get('TargetFile', '')
                if 'recover.py' in target or 'update_account_links.py' in target:
                    continue
                if target.endswith('.md'):
                    continue
                with open(target, 'w', encoding='utf-8') as out:
                    out.write(args['CodeContent'])
                print("Applied write_to_file on", target)

            elif name == 'multi_replace_file_content' or name == 'default_api:multi_replace_file_content':
                args = tc.get('arguments', tc.get('args', {}))
                if isinstance(args, str): args = json.loads(args)
                target = args.get('TargetFile', '')
                if 'recover.py' in target or 'update_account_links.py' in target:
                    continue
                if target.endswith('.md'):
                    continue
                
                try:
                    with open(target, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                except FileNotFoundError:
                    continue
                
                # Apply chunks from bottom to top
                chunks = args.get('ReplacementChunks', [])
                for chunk in chunks:
                    old_text = chunk['TargetContent']
                    new_text = chunk['ReplacementContent']
                    content = content.replace(old_text, new_text)
                
                with open(target, 'w', encoding='utf-8') as out:
                    out.write(content)
                print("Applied multi_replace_file_content on", target)

            elif name == 'replace_file_content' or name == 'default_api:replace_file_content':
                args = tc.get('arguments', tc.get('args', {}))
                if isinstance(args, str): args = json.loads(args)
                target = args.get('TargetFile', '')
                if 'recover.py' in target or 'update_account_links.py' in target:
                    continue
                if target.endswith('.md'):
                    continue
                
                try:
                    with open(target, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                except FileNotFoundError:
                    continue
                
                old_text = args['TargetContent']
                new_text = args['ReplacementContent']
                content = content.replace(old_text, new_text)
                
                with open(target, 'w', encoding='utf-8') as out:
                    out.write(content)
                print("Applied replace_file_content on", target)

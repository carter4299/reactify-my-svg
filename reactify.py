import re
import os
import argparse

def camel_case_replacer(match):
    word = match.group(0)
    parts = word.split('-')
    return parts[0] + ''.join(part.capitalize() for part in parts[1:])

def replace_hyphenated_words(svg_content):
    pattern = r'\b\w+(?:-\w+)+\b'
    return re.sub(pattern, camel_case_replacer, svg_content)

def insert_props(svg_string):
    insert_index = svg_string.find('<svg ') + len('<svg ')
    return svg_string[:insert_index] + '{...props} ' + svg_string[insert_index:]

def process_svg_file(args):
    input_svg = args.input
    output_js = args.output
    props = args.props

    if not os.path.exists(input_svg):
        print(f"Error: {input_svg} does not exist.")
        return
    if not input_svg.endswith('.svg'):
        print("Error: Input file must be an SVG file.")
        return
    if not output_js.endswith(('.js', '.ts', '.tsx', '.jsx')):
        print("Error: Output file must be a JS/TS/JSX/TSX file.")
        return

    try:
        with open(input_svg, 'r') as file:
            svg_content = file.read()
    except Exception as e:
        print(f"Error: {e}")
        return

    header = f"export function {output_js.split(".")[0]}() {"{"}\n\treturn (\n"

    updated_svg_content = replace_hyphenated_words(svg_content)
    updated_svg_content = [f"\t\t{line.strip()}" for line in updated_svg_content.split("\n") if line.strip()]

    if props:
        if output_js.endswith('.ts'):
            output_js = output_js.replace('.ts', '.tsx')
        if output_js.endswith(('.ts', '.tsx')):
            header = f"export function {output_js.split(".")[0]}(props: any) {"{"}\n\treturn (\n"
        else:
            header = f"export function {output_js.split(".")[0]}(props) {"{"}\n\treturn (\n"
        updated_svg_content[0] = insert_props(updated_svg_content[0])

    updated_svg_content = "\n".join(updated_svg_content)

    try:
        with open(output_js, 'w') as file:
            file.write(header)
            file.write(updated_svg_content)
            file.write("\n\t);\n}")
    except Exception as e:
        print(f"Error: {e}")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace hyphens with camelCase in an SVG file.")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input SVG file")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output JS/TS file")
    parser.add_argument('-p', '--props', action='store_true', help="Add props to the output file")

    args = parser.parse_args()

    process_svg_file(args)

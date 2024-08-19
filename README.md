# Reactify my SVG
* Turn SVG files into React components.
* Replace hyphens with camelCase in an SVG file.

## Installation
```sh
git clone https://github.com/carter4299/reactify-my-svg.git
cd reactify-my-svg
chmod +x install.sh
./install.sh
```

## Usage
```sh
reactify [-h] -i INPUT -o OUTPUT [-p]
Replace hyphens with camelCase in an SVG file.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input SVG file
  -o OUTPUT, --output OUTPUT
                        Output JS/TS file
  -p, --props           Add props to the output file
```

## Examples
### JS/JSX

```sh
reactify -i test.svg -o main.js
```

```js
export function main() {
	return (
		<svg version="1.1" width="300" height="200" xmlns="http://www.w3.org/2000/svg">
		<rect width="100%" height="100%" fill="red" />
		<circle cx="150" cy="100" r="80" fill="green" />
		<text x="150" y="125" fontSize="60" textAnchor="middle" fill="white">SVG</text>
		</svg>
	);
}
```

### TS/TSX with props
```sh
reactify -i test.svg -o main.tsx -p
```

```tsx
export function main(props:any) {
	return (
		<svg {...props} version="1.1" width="300" height="200" xmlns="http://www.w3.org/2000/svg">
		<rect width="100%" height="100%" fill="red" />
		<circle cx="150" cy="100" r="80" fill="green" />
		<text x="150" y="125" fontSize="60" textAnchor="middle" fill="white">SVG</text>
		</svg>
	);
}
```

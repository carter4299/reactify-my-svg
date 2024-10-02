# /bin/bash

INSTALL_PATH="dist/reactify"
USER_BIN_FOLDER="$HOME/.local/bin/"

FISH_FUNC=$(cat <<'EOF'
function reactify
    if test -n "$argv"
        ~/.local/bin/reactify $argv
    else
        ~/.local/bin/reactify -h
    end
end
EOF
)

setup_venv() {
    echo "Creating tmp venv and installing pyinstaller"
    python3 -m venv tmp
    source tmp/bin/activate
    pip install pyinstaller
}

compile() {
    echo "Compiling reactify"
    pyinstaller --onefile --noconsole --name=reactify reactify.py --optimize=2
}

copy_bin() {
    echo "Copying reactify to $USER_BIN_FOLDER"
    mkdir -p $USER_BIN_FOLDER
    cp $INSTALL_PATH $USER_BIN_FOLDER
}

set_path() {
    echo "Setting path"

    USER_SHELL=$(basename "$SHELL")

    if [ "$USER_SHELL" = "bash" ]; then
        echo "export PATH=$USER_BIN_FOLDER:\$PATH" >> ~/.bashrc
    elif [ "$USER_SHELL" = "zsh" ]; then
        echo "export PATH=$USER_BIN_FOLDER:\$PATH" >> ~/.zshrc
    elif [ "$USER_SHELL" = "fish" ]; then
        printf "%s\n" "$FISH_FUNC" >> ~/.config/fish/config.fish
    else
        echo "Unknown shell: $USER_SHELL"
    fi
}


if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installer for Linux"
    setup_venv
    compile
    copy_bin
    set_path
    deactivate
    rm -rf tmp
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installer for MacOS"
    setup_venv
    compile
    copy_bin
    set_path
    deactivate
    rm -rf tmp
else
    echo "OS not supported"
fi

echo "Installation complete... Please source your shell config file or restart your shell."

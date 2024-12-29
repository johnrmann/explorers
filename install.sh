echo "Installing Explorers.";
echo "-----------------------------------";
echo "";

echo "Installing Python modules.";
pip install -r requirements.txt;

echo "Compiling compiled libraries.";
./compile.sh;

echo "Testing code."
./test.sh;

echo "Installation complete.";

LIGHT_GREEN='\033[1;32m'
LIGHT_PURPLE='\033[1;35m'
LIGHT_BLUE='\033[1;34m'
NC='\033[0m'

APP_DIR="/usr/sbin/vert"

sudo mkdir $APP_DIR
echo "1/5: Directory in /user/sbin/vert successfully created"
sudo cp --force ./dist/app.bin $APP_DIR
echo "2/5: ${LIGHT_GREEN}app.bin${NC} binary file successfully copied to ${LIGHT_BLUE}${APP_DIR}${NC}"
sudo cp --force ./dist/tasker $APP_DIR
echo "3/5: ${LIGHT_GREEN}tasker${NC} binary file successfully copied to ${LIGHT_BLUE}${APP_DIR}${NC}"
sudo cp --force ./dist/assets/command-line.png $APP_DIR
echo "4/5: ${LIGHT_GREEN}command-line.png${NC} image successfully copied to ${LIGHT_BLUE}${APP_DIR}${NC}"
sudo echo "alias vert='${APP_DIR}/app.bin'" | sudo tee -a ~/.zshrc > /dev/null
echo "5/5: ${LIGHT_GREEN}vert${NC} environment variable successfully appended to ${LIGHT_PURPLE}~/.zshrc${NC} file"
source ~/.zshrc

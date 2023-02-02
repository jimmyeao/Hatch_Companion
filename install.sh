# Raspberrypi set up dependencies script
sudo apt-get update
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz
tar zxvf bcm2835-1.71.tar.gz 
cd bcm2835-1.71/
sudo ./configure && sudo make && sudo make check && sudo make install
# For more information, please refer to the official website: http://www.airspayce.com/mikem/bcm2835/
cd ~/
sudo apt install git -y
git clone https://github.com/WiringPi/WiringPi
cd WiringPi
./build
cd ~/
sudo apt-get install python3-pip -y
sudo apt-get install python3-pil -y
sudo apt-get install python3-numpy -y
sudo pip3 install RPi.GPIO -y
sudo pip3 install spidev -y
wget https://github.com/jimmyeao/Hatch_Companion/blob/main/Hatch.py
python3 Hatch.py

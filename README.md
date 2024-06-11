# scripts


## github-org-scrape.py

### Setup
```
sudo apt install git
mkdir src
cd src
git clone https://github.com/hazey420/scripts.git
cd scripts
pip install -r requirements.txt
cp github-org-scrape.py ~/.local/bin
export PATH=$PATH:~/.local/bin
```

### clone an org
```
mkdir ~/src/mirrors
cd ~/src/mirrors
github-org-scrape.py Archive-Samourai-Wallet -c -b all
```

You will see output like this
```
hazey@server:mirrors$ github-org-scrape.py Archive-Samourai-Wallet -c -b all                                           
Archive-Samourai-Wallet/soroban                                                                                         
Archive-Samourai-Wallet/Tor_Onion_Proxy_Library                                                                         
Archive-Samourai-Wallet/samourai-wallet-android                                                                         
Archive-Samourai-Wallet/whirlpool-client-cli                                                                            
Archive-Samourai-Wallet/xmanager-server                                                                                 
Archive-Samourai-Wallet/xmanager-protocol                                                                               
Archive-Samourai-Wallet/whirlpool-server                                                                                
Archive-Samourai-Wallet/whirlpool-runtimes                                                                              
Archive-Samourai-Wallet/whirlpool-protocol                                                                              
Archive-Samourai-Wallet/whirlpool-gui                                                                                   
Archive-Samourai-Wallet/whirlpool-client                                                                                
Archive-Samourai-Wallet/Whirlpool                                                                                       
Archive-Samourai-Wallet/soroban-client-java                                                                             
Archive-Samourai-Wallet/java-websocket-server                                                                           
Archive-Samourai-Wallet/java-server                                                                                     
Archive-Samourai-Wallet/java-http-client                                                                                
Archive-Samourai-Wallet/extlibj                                                                                         
Archive-Samourai-Wallet/boltzmann-java                                                                                  
Clone? y/N: y                                                                                                           
##### Cloning repo Archive-Samourai-Wallet/soroban                                                                      
##### Cloning repo Archive-Samourai-Wallet/Tor_Onion_Proxy_Library                       
##### Cloning repo Archive-Samourai-Wallet/samourai-wallet-android                           
##### Cloning repo Archive-Samourai-Wallet/whirlpool-client-cli                                    
##### Cloning repo Archive-Samourai-Wallet/xmanager-server
##### Cloning repo Archive-Samourai-Wallet/xmanager-protocol 
##### Cloning repo Archive-Samourai-Wallet/whirlpool-server
##### Cloning repo Archive-Samourai-Wallet/whirlpool-runtimes
##### Cloning repo Archive-Samourai-Wallet/whirlpool-protocol
##### Cloning repo Archive-Samourai-Wallet/whirlpool-gui
##### Cloning repo Archive-Samourai-Wallet/whirlpool-client
##### Cloning repo Archive-Samourai-Wallet/Whirlpool
##### Cloning repo Archive-Samourai-Wallet/soroban-client-java
##### Cloning repo Archive-Samourai-Wallet/java-websocket-server
##### Cloning repo Archive-Samourai-Wallet/java-server
##### Cloning repo Archive-Samourai-Wallet/java-http-client
##### Cloning repo Archive-Samourai-Wallet/extlibj
##### Cloning repo Archive-Samourai-Wallet/boltzmann-java
Log is at "/home/hazey/src/mirrors/clone-Archive-Samourai-Wallet.log"
hazey@server:mirrors$
```

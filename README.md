# Rittal_Power_Monitoring
Power Monitoring system for Rittal PDU systems

## Contents
1. Introduction
2. Setup
3. Usage
4. Flags
5. Prerequisites
6. Notes

## 1. Introduction 

Rittal PDU systems have an HTML interface which allows for administrators to access and make changes, or view parts of the system.
The PDU interface allows for adminstrators to view the live power, voltage and current readings of the phases. The aim of this project is to be used for individual socket monitoring, though at the time of writing this, I do not have access to a "Metered Plus" PDU and only a "Metered" PDU, so as a result this can only record Phases, though it should be easy to adapt this code to work on the "Metered Plus" with minor changes.

At present the script can monitor one phase at a time

![Setup Diagram](https://user-images.githubusercontent.com/50869390/232887333-dfe6700d-36d0-4591-a074-5dfbd3e99045.jpg)

The script works by scraping the live values off the interface below
<img width="736" alt="PDU Screen" src="https://user-images.githubusercontent.com/50869390/232888681-37b75760-a527-4cab-98ef-8839fe92bc32.PNG">


## 2. Setup

### Dependencies
```
pip install selenium
```
```
pip install beautifulsoup4
```
```
sudo apt-get install chromium-browser
```
### Hardware
There must be a device that is connected via ethernet to the Rittal system, in order to connect to the device, your machine must 
have an IP begining with 192.168.0.xxx, the Rittal webpage is accessible on 192.168.0.200.

*** For the above to work, the machine will need two means of connecting to the internet, one via ethernet(PDU), and the other for ssh.

In the case of our setup, there are two ethernet connections to the "Host" machine, 1 to the PDU, 1 to the internet for ssh.


## 3. Usage

### Enable port forwarding (Automatically) 
** If your system is connected directly to the Rittal PDU, you can skip this step

This can be done from the root directory by running the below command, which will prompt you for credentials and automatically connect.
** Note that this is designed to work on Mac

```
 ./network/make_connection.sh 
```
You may need to give permission to the make_connection.sh file
```
chmod +x make_connection.sh
```

### Enable port forwarding (Manually) 
If you want to set it up manually you can by running the following commands:
On your Local machine:
```
ssh -L 8080:<host_ip_A>:80 <user>@<machine_ip_C> ## For most rittal systems, host ip is: 192.168.0.200
```
On Host machine:
```
ssh -R 8080:localhost:80 <user>@localhost
```

### Run Script
#### MAC
```
python3 rittal.py
```
#### Ubuntu LTS
```
python3 rittal.py -n http://192.168.0.200 -s LTS
```

Output will be stored in a log file: "log.out"
Format: Time | N | Phase | Voltage | Current | Power | Energy

## 4. Flags
There are a combination of flags that can be passed in to alter certain parts of the script

#### Interval
Adjust Interval beween measurements of script in seconds(Default 2)
```
python3 rittal.py -i 1
```
#### Timeout
Adjust duration of script in seconds
```
python3 rittal.py -t 100 
```
#### Output File
Change the name of the output file
```
python3 rittal.py -o beautifullog.out
```
#### Network
Change the source of the Rittal interface
```
python3 rittal.py -n http://192.168.0.200 
```
#### System
Change the settings in the file based on the host system (MACOS|LTS)
```
python3 rittal.py -s LTS
```
#### headless
Display chromebrowser (Only possible on Mac) True = not visible 
```
python3 rittal.py -d False
```

#### Phase
Select which phase to record from (Default L1)
```
python3 rittal.py -p L2
```


## 5. Prerequisites 
Must have Chrome installed on Mac
** In the case of ubuntu the above steps should be sufficient.

## 6. Notes 

If scripts don't run, permissions may need to be adjusted 

```
chmod +x make_connection.sh
```
```
chmod +x chromedriveramd
```

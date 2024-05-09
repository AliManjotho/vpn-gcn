@echo off

set dataset_path=D:/SH/TrafficClassification/dataset/ISCX/
set splitcap_path=D:/SH/TrafficClassification/code-gcn/PCAP processing/SplitCap.exe

set cmd1=cd "%dataset_path%NonVPN/"
set cmd2="%splitcap_path%" -r %dataset_path%NonVPN/ -recursive -s session
set cmd3=cd "%dataset_path%VPN/"
set cmd4="%splitcap_path%" -r %dataset_path%VPN/ -recursive -s session


%cmd4%


pause
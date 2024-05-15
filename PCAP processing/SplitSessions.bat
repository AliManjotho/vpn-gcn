@echo off

set dataset_path=D:/SH/TrafficClassification/dataset/ISCX/
set splitcap_path=D:/SH/TrafficClassification/code-gcn/PCAP processing/SplitCap.exe

set output_dir_nonvpn="%dataset_path%NonVPN-Splitted"
set output_dir_vpn="%dataset_path%VPN-Splitted"
set nonvpn_dir_path="%dataset_path%NonVPN"
set vpn_dir_path="%dataset_path%VPN"


set cmd1="%splitcap_path%" -r %nonvpn_dir_path% -o %output_dir_nonvpn% -recursive -s session
set cmd2="%splitcap_path%" -r %vpn_dir_path% -o %output_dir_vpn% -recursive -s session
set cmd3=rmdir /s /Q %nonvpn_dir_path%
set cmd4=rmdir /s /Q %vpn_dir_path%
set cmd5=move %output_dir_nonvpn% %nonvpn_dir_path%
set cmd6=move %output_dir_vpn% %vpn_dir_path%


%cmd1%
%cmd2%
%cmd3%
%cmd4%
%cmd5%
%cmd6%



pause

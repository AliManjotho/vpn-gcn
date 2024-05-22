from pathlib import Path
from enum import Enum

class DATASET(Enum):
    ISCX=0
    VNAT=1

iscx_map = {
            'email': ['email'],
            'chat': ['aim_chat', 'AIMchat', 'facebook_chat', 'facebookchat', 'hangout_chat', 'hangouts_chat', 'icq_chat', 'ICQchat', 'gmailchat', 'gmail_chat', 'skype_chat'],
            'streaming': ['netflix', 'spotify', 'vimeo', 'youtube', 'youtubeHTML5'],
            'file_transfer': ['ftps_down', 'ftps_up','sftp_up', 'sftpUp', 'sftp_down', 'sftpDown', 'sftp', 'skype_file', 'scpUp', 'scpDown', 'scp'],
            'voip': ['voipbuster', 'facebook_audio', 'hangout_audio', 'hangouts_audio', 'skype_audio'],
            'p2p': ['skype_video', 'facebook_video', 'hangout_video', 'hangouts_video'],

            'vpn_email': ['vpn_email'],
            'vpn_chat': ['vpn_aim_chat', 'vpn_facebook_chat', 'vpn_hangouts_chat', 'vpn_icq_chat', 'vpn_skype_chat'],
            'vpn_streaming': ['vpn_netflix', 'vpn_spotify', 'vpn_vimeo', 'vpn_youtube'],
            'vpn_file_transfer': ['vpn_ftps', 'vpn_sftp', 'vpn_skype_files'],
            'vpn_voip': ['vpn_facebook_audio', 'vpn_skype_audio', 'vpn_voipbuster'],
            'vpn_p2p': ['vpn_bittorrent']   
}

vnat_map = {
            'streaming': ['nonvpn_netflix', 'nonvpn_youtube', 'nonvpn_vimeo'],
            'voip': ['nonvpn_voip', 'nonvpn_skype'],
            'file_transfer': ['nonvpn_rsync', 'nonvpn_sftp', 'nonvpn_scp'],
            'p2p': ['nonvpn_ssh', 'nonvpn_rdp'],

            'vpn_streaming': ['vpn_netflix', 'vpn_youtube', 'vpn_vimeo'],
            'vpn_voip': ['vpn_voip', 'vpn_skype'],
            'vpn_file_transfer': ['vpn_rsync', 'vpn_sftp', 'vpn_scp'],
            'vpn_p2p': ['vpn_ssh', 'vpn_rdp']
}


def iscx_get_unique_labels(): 
    return list(iscx_map.keys())

def vnat_get_unique_labels(): 
    return list(vnat_map.keys())




def iscx_get_class_label(file): 
    cls = ''   
    label = file.split('.')[0]
    for m_key, m_values in iscx_map.items():
        for value in m_values:
            if label[:len(value)] == value:
                cls = m_key
                break
    return cls


def vnat_get_class_label(file): 
    cls = ''   
    label = file.split('.')[0]
    for m_key, m_values in vnat_map.items():
        for value in m_values:
            if label[:len(value)] == value:
                cls = m_key
                break
    return cls





def iscx_get_one_hot(cls):
    clss = iscx_get_unique_labels()
    index = clss.index(cls)

    one_hot = [0 for _ in range(len(clss))]
    one_hot[index] = 1

    return one_hot


def vnat_get_one_hot(cls):
    clss = vnat_get_unique_labels()
    index = clss.index(cls)

    one_hot = [0 for _ in range(len(clss))]
    one_hot[index] = 1

    return one_hot


def filenumber_to_id(file_num, length=8):
    file_num_str = str(file_num)
    file_num_str_len = len(file_num_str)
    return '0' * (length - file_num_str_len) + file_num_str

def num_packets_to_edge_indices(num_packets):
    return [list(range(0,num_packets-1)), list(range(1,num_packets))]
    


        


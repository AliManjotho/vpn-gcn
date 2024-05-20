from pathlib import Path

iscx_map = {
            'aim_chat': ['aim_chat', 'AIMchat'],
            'email': ['email'],
            'facebook_audio': ['facebook_audio'],
            'facebook_chat': ['facebook_chat', 'facebookchat'],
            'facebook_video': ['facebook_video'],
            'ftps_down': ['ftps_down'],
            'ftps_up': ['ftps_up'],
            'gmail': ['gmailchat', 'gmail_chat'],
            'hangout_chat': ['hangout_chat', 'hangouts_chat'],
            'hangout_audio': ['hangout_audio', 'hangouts_audio'],
            'hangout_video': ['hangout_video', 'hangouts_video'],
            'icq_chat': ['icq_chat', 'ICQchat'],
            'netflix': ['netflix'],
            'scp_up': ['scpUp'],
            'scp_down': ['scpDown', 'scp'],
            'sftp_up': ['sftp_up', 'sftpUp'],
            'sftp_down': ['sftp_down', 'sftpDown', 'sftp'],
            'skype_audio': ['skype_audio'],
            'skype_chat': ['skype_chat'],
            'skype_video': ['skype_video'],
            'skype_file': ['skype_file'],
            'spotify': ['spotify'],
            'vimeo': ['vimeo'],
            'voipbuster': ['voipbuster'],
            'youtube': ['youtube'],
            'youtube_html5': ['youtubeHTML5'],
            'vpn_aim_chat': ['vpn_aim_chat'],
            'vpn_bittorrent': ['vpn_bittorrent'],
            'vpn_email': ['vpn_email'],
            'vpn_facebook_audio': ['vpn_facebook_audio'],
            'vpn_facebook_chat': ['vpn_facebook_chat'],
            'vpn_ftps': ['vpn_ftps'],
            'vpn_hangouts_chat': ['vpn_hangouts_chat'],
            'vpn_icq_chat': ['vpn_icq_chat'],
            'vpn_netflix': ['vpn_netflix'],
            'vpn_sftp': ['vpn_sftp'],
            'vpn_skype_audio': ['vpn_skype_audio'],
            'vpn_skype_chat': ['vpn_skype_chat'],
            'vpn_skype_files': ['vpn_skype_files'],
            'vpn_spotify': ['vpn_spotify'],
            'vpn_vimeo': ['vpn_vimeo'],
            'vpn_voipbuster': ['vpn_voipbuster'],
            'vpn_youtube': ['vpn_youtube']      
}

vnat_map = {
            'nonvpn_netflix': ['nonvpn_netflix'],
            'nonvpn_rdp': ['nonvpn_rdp'],
            'nonvpn_rsync': ['nonvpn_rsync'],
            'nonvpn_scp': ['nonvpn_scp'],
            'nonvpn_sftp': ['nonvpn_sftp'],
            'nonvpn_skype': ['nonvpn_skype'],
            'nonvpn_ssh': ['nonvpn_ssh'],
            'nonvpn_vimeo': ['nonvpn_vimeo'],
            'nonvpn_voip': ['nonvpn_voip'],
            'nonvpn_youtube': ['nonvpn_youtube'],
            'vpn_netflix': ['vpn_netflix'],
            'vpn_rdp': ['vpn_rdp'],
            'vpn_rsync': ['vpn_rsync'],
            'vpn_scp': ['vpn_scp'],
            'vpn_sftp': ['vpn_sftp'],
            'vpn_skype': ['vpn_skype'],
            'vpn_ssh': ['vpn_ssh'],
            'vpn_vimeo': ['vpn_vimeo'],
            'vpn_voip': ['vpn_voip'],
            'vpn_youtube': ['vpn_youtube']
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

if __name__=='__main__':

    print(num_packets_to_edge_indices(4))
    
    


        


